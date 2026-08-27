import datetime

date_str = datetime.datetime.now().strftime("%Y-%m-%d")
new_html_path = 'c:\\Playground26\\wiskinglin.github.io\\new.html'

with open(new_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_section = f'''
            <!-- {date_str} Update: Fix formatting -->
            <section class="section-card">
                <div class="flex items-center gap-4 mb-6 pb-6 border-b border-slate-100">
                    <span class="tag-badge tag-optimization">Optimization</span>
                    <h2 class="text-xl font-bold text-slate-800">版面細節修復</h2>
                </div>
                <div class="space-y-6">
                    <div class="flex gap-4">
                        <div class="w-1.5 rounded-full bg-blue-500 shrink-0"></div>
                        <div>
                            <h3 class="font-bold text-slate-800 mb-2">移除多餘的換行符號</h3>
                            <p class="text-slate-600 leading-relaxed mb-4">全面修復了近期更新中，文章與頁面結尾意外產生的字面 \\n 換行符號問題。受影響並已修復的頁面包含首頁、最新消息，以及 ManagerToday 系列深讀報告。</p>
                        </div>
                    </div>
                </div>
            </section>
'''

content = content.replace('<main>', '<main>\\n' + new_section)

with open(new_html_path, 'w', encoding='utf-8') as f:
    f.write(content)
