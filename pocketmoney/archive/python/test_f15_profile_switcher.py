import os
import sys
from playwright.sync_api import sync_playwright

def test_f15_profile_switcher():
    current_file = os.path.abspath(__file__)
    # current_file is: .../wiskinglin.github.io/pocketmoney/archive/python/test_f15_profile_switcher.py
    # 4 levels up to repo root: python -> archive -> pocketmoney -> repo root
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    html_path = os.path.join(repo_root, 'pocketmoney', 'prototypes', 'F15-integrated-dashboard', 'index.html')
    file_url = 'file:///' + html_path.replace('\\', '/')

    print(f"Testing URL: {file_url}")

    errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.on('console', lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: errors.append(f"Page Error: {exc}"))

        page.goto(file_url)
        page.wait_for_load_state('networkidle')

        # 1. 檢查預設帳本狀態
        current_name = page.locator('#currentProfileName').inner_text()
        print(f"Initial profile name: {current_name}")
        assert "我的真實帳本" in current_name, f"Expected '我的真實帳本', got '{current_name}'"

        banner = page.locator('#demoSandboxBanner')
        assert not banner.is_visible(), "demoSandboxBanner should be hidden in default profile"

        # 2. 開啟下拉選單
        page.click('#profileSwitcherBtn')
        dropdown = page.locator('#profileDropdownMenu')
        assert dropdown.is_visible(), "profileDropdownMenu should be visible after click"

        # 3. 切換至展示沙盒
        print("Switching to demo_sandbox...")
        page.evaluate("switchProfile('demo_sandbox')")
        page.wait_for_timeout(300)

        current_name = page.locator('#currentProfileName').inner_text()
        print(f"Profile after switch to demo: {current_name}")
        assert "展示沙盒 (Demo)" in current_name, f"Expected demo profile, got '{current_name}'"
        assert banner.is_visible(), "demoSandboxBanner should be visible in demo_sandbox"

        # 4. 點擊重置沙盒
        print("Testing resetDemoSandbox()...")
        page.evaluate("resetDemoSandbox()")
        page.wait_for_timeout(300)

        # 5. 測試新增自訂帳本
        print("Testing openCreateProfileModal and submitCreateProfile...")
        page.evaluate("openCreateProfileModal()")
        page.wait_for_timeout(200)

        modal = page.locator('#profileModal')
        assert modal.is_visible(), "profileModal should be visible"
        create_view = page.locator('#profileModalCreateView')
        assert create_view.is_visible(), "profileModalCreateView should be visible"

        page.fill('#createProfileNameInput', '旅遊基金專戶')
        page.click("button:has-text('確認建立')")
        page.wait_for_timeout(300)

        current_name = page.locator('#currentProfileName').inner_text()
        print(f"Profile after create: {current_name}")
        assert current_name == '旅遊基金專戶', f"Expected '旅遊基金專戶', got '{current_name}'"
        assert not banner.is_visible(), "demoSandboxBanner should be hidden in custom profile"

        # 6. 測試重新命名
        print("Testing openRenameProfileModal and submitRenameProfile...")
        current_id = page.evaluate("currentProfileId")
        page.evaluate(f"openRenameProfileModal('{current_id}')")
        page.wait_for_timeout(200)

        rename_view = page.locator('#profileModalRenameView')
        assert rename_view.is_visible(), "profileModalRenameView should be visible"

        page.fill('#renameProfileNameInput', '年度旅遊基金帳')
        page.click("button:has-text('儲存變更')")
        page.wait_for_timeout(300)

        current_name = page.locator('#currentProfileName').inner_text()
        print(f"Profile after rename: {current_name}")
        assert current_name == '年度旅遊基金帳', f"Expected '年度旅遊基金帳', got '{current_name}'"

        # 7. 測試刪除自訂帳本
        print("Testing openDeleteProfileModal and submitDeleteProfile...")
        page.evaluate(f"openDeleteProfileModal('{current_id}')")
        page.wait_for_timeout(200)

        delete_view = page.locator('#profileModalDeleteView')
        assert delete_view.is_visible(), "profileModalDeleteView should be visible"
        target_name = page.locator('#deleteProfileTargetName').inner_text()
        assert target_name == '年度旅遊基金帳'

        page.click("button:has-text('確認刪除')")
        page.wait_for_timeout(300)

        # 刪除後應自動回到 default
        current_name = page.locator('#currentProfileName').inner_text()
        current_id_after = page.evaluate("currentProfileId")
        print(f"Profile after delete: {current_name} (id={current_id_after})")
        assert current_id_after == 'default'
        assert "我的真實帳本" in current_name

        # 8. 驗證資料隔離相容性
        print("Verifying localStorage key isolation...")
        storage_keys = page.evaluate("""() => {
            return {
                default_key: localStorage.getItem('PocketMoney_tw_finance_v3') ? true : false,
                demo_key: localStorage.getItem('PocketMoney_profile_demo_sandbox_v3') ? true : false,
                meta: JSON.parse(localStorage.getItem('PocketMoney_profiles_meta_v1'))
            };
        }""")
        print(f"Storage keys status: {storage_keys}")
        assert storage_keys['meta'] is not None, "Profiles meta should be stored"
        assert any(p['id'] == 'default' for p in storage_keys['meta']['profiles']), "Default profile in meta"
        assert any(p['id'] == 'demo_sandbox' for p in storage_keys['meta']['profiles']), "Demo sandbox in meta"

        browser.close()

    if errors:
        print(f"FAILED with {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("SUCCESS! All profile switcher tests passed with 0 console/page errors.")
        sys.exit(0)

if __name__ == '__main__':
    test_f15_profile_switcher()
