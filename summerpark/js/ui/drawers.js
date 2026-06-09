import { renderClosetItems } from './render.js';
import { playSFX } from '../services/audio.js';

export function setupDrawers() {
  const overlay = document.getElementById('drawer-overlay');
  const drawers = document.querySelectorAll('.drawer');
  
  // 所有選單按鈕與對應抽屜 ID 的對照表
  const navMap = {
    'nav-train': 'drawer-train',
    'nav-walk': 'drawer-walk',
    'nav-gacha': 'drawer-gacha',
    'nav-quests': 'drawer-quests',
    'nav-closet': 'drawer-closet',
    'nav-settings': 'drawer-settings'
  };
  
  Object.keys(navMap).forEach(btnId => {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.addEventListener('click', () => {
      const drawerId = navMap[btnId];
      openDrawer(drawerId);
      playSFX('click');
      
      // 更新選單 active 狀態
      document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
      btn.classList.add('active');
    });
  });
  
  // 關閉按鈕事件
  document.querySelectorAll('.btn-close').forEach(btn => {
    btn.addEventListener('click', closeAllDrawers);
  });
  
  // 遮罩層點擊事件
  if (overlay) {
    overlay.addEventListener('click', closeAllDrawers);
  }

  // 監聽外部關閉所有抽屜的事件
  window.addEventListener('close-all-drawers', closeAllDrawers);
}

export function openDrawer(drawerId) {
  closeAllDrawersWithoutOverlay();
  
  const drawer = document.getElementById(drawerId);
  const overlay = document.getElementById('drawer-overlay');
  
  if (drawer) drawer.classList.add('active');
  if (overlay) overlay.classList.add('active');
  
  // 如果是打開更衣室，渲染最新的裝扮清單
  if (drawerId === 'drawer-closet') {
    // 重設分頁狀態
    document.querySelectorAll('.closet-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    const firstTab = document.querySelector('.closet-tabs .tab-btn[data-category="head"]');
    if (firstTab) firstTab.classList.add('active');
    
    renderClosetItems('head');
  }
}

export function closeAllDrawers() {
  document.querySelectorAll('.drawer').forEach(d => d.classList.remove('active'));
  const overlay = document.getElementById('drawer-overlay');
  if (overlay) overlay.classList.remove('active');
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
}

export function closeAllDrawersWithoutOverlay() {
  document.querySelectorAll('.drawer').forEach(d => d.classList.remove('active'));
}
