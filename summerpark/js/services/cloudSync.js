import { gameState } from '../store/gameState.js';

export async function syncToCloud() {
  const statusEl = document.getElementById('sync-status-text');
  if (!gameState.config.apiUrl) return;
  
  try {
    const response = await fetch(`${gameState.config.apiUrl}/api/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(gameState)
    });
    
    if (response.ok) {
      if (statusEl) {
        statusEl.textContent = '當前模式：雲端同步中 (Cloudflare)';
        statusEl.className = 'sync-status status-online';
      }
    } else {
      throw new Error('Sync failed');
    }
  } catch (err) {
    if (statusEl) {
      statusEl.textContent = '當前模式：雲端同步失敗 (已切回本地)';
      statusEl.className = 'sync-status status-offline';
    }
    console.error('Cloud sync failed:', err);
  }
}

// 監聽來自 store 的同步事件
window.addEventListener('sync-to-cloud', () => {
  syncToCloud();
});
