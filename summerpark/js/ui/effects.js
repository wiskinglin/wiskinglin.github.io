export function spawnFloatingText(assetOrEmoji, text = '') {
  const container = document.getElementById('effect-container');
  if (!container) return;
  const el = document.createElement('div');
  el.className = 'float-effect';
  
  if (assetOrEmoji.startsWith('./assets/') || assetOrEmoji.startsWith('assets/')) {
    const img = document.createElement('img');
    img.src = assetOrEmoji;
    img.style.width = '24px';
    img.style.height = '24px';
    img.style.verticalAlign = 'middle';
    img.style.marginRight = '4px';
    el.appendChild(img);
    const span = document.createElement('span');
    span.textContent = text;
    el.appendChild(span);
  } else {
    el.textContent = assetOrEmoji + text;
  }
  
  // 隨機在柯基附近的位置
  const randomX = 40 + Math.random() * 20; // 50% 左右
  el.style.left = `${randomX}%`;
  el.style.top = `60%`;
  
  container.appendChild(el);
  
  // 動畫結束後移除
  setTimeout(() => {
    el.remove();
  }, 1000);
}

export function spawnBubbles() {
  const fxContainer = document.getElementById('corgi-fx-bubbles');
  if (!fxContainer) return;
  fxContainer.innerHTML = '';
  
  for (let i = 0; i < 15; i++) {
    const b = document.createElement('div');
    b.className = 'bubble-fx';
    
    // 隨機泡泡大小與飄動位移
    const size = 10 + Math.random() * 15;
    const dx = -50 + Math.random() * 100;
    const dxEnd = dx * 1.5;
    
    b.style.width = `${size}px`;
    b.style.height = `${size}px`;
    b.style.left = `${30 + Math.random() * 40}%`;
    b.style.bottom = `${10 + Math.random() * 30}%`;
    b.style.setProperty('--dx', `${dx}px`);
    b.style.setProperty('--dx-end', `${dxEnd}px`);
    
    fxContainer.appendChild(b);
  }
  
  setTimeout(() => {
    fxContainer.innerHTML = '';
  }, 1200);
}

// 暫時觸發特定動畫 class，過後切回 idle
export function triggerTemporaryAnimation(animClass, durationMs, isWalkingCheck = false) {
  const container = document.getElementById('corgi-character');
  if (!container) return;
  container.className = `corgi-container ${animClass}`;
  
  setTimeout(() => {
    // 若中途未開始散步或被其他狀態覆蓋，切回 idle
    if (!isWalkingCheck && container.className.includes(animClass)) {
      container.className = 'corgi-container status-idle';
    }
  }, durationMs);
}
