export const CLOSET_ITEMS = {
  // --- 頭部裝飾 ---
  head: {
    strawhat: {
      id: 'strawhat',
      name: '夏日草帽',
      rarity: 'N',
      icon: '👒',
      desc: '一頂編織精緻的遮陽草帽，戴上後特別有夏日渡假風情。',
      svg: `
        <ellipse cx="0" cy="-15" rx="35" ry="8" fill="#E9C46A" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-18" y="-30" width="36" height="16" fill="#E9C46A" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-18" y="-18" width="36" height="4" fill="#E76F51"/>
      `
    },
    sunglasses: {
      id: 'sunglasses',
      name: '飛行員墨鏡',
      rarity: 'SR',
      icon: '🕶️',
      desc: '戴上它，柯基瞬間變成街上最酷、最拉風的仔！魅力加倍！',
      svg: `
        <path d="M-22 0 L-8 0 Q-15 8 -22 0 M8 0 L22 0 Q15 8 8 0 Z" fill="#2B2D42" stroke="#FFFFFF" stroke-width="1.5"/>
        <line x1="-8" y1="0" x2="8" y2="0" stroke="#2B2D42" stroke-width="2.5"/>
      `
    },
    sunflower: {
      id: 'sunflower',
      name: '向日葵頭套',
      rarity: 'SR',
      icon: '🌻',
      desc: '軟綿綿的黃色花瓣圍繞著臉蛋，柯基秒變治癒系小太陽。',
      svg: `
        <g transform="scale(0.95) translate(0, 5)">
          <path d="M0 -38 Q-12 -25 0 -12 Q12 -25 0 -38 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M0 38 Q-12 25 0 12 Q12 25 0 38 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-38 0 Q-25 -12 -12 0 Q-25 12 -38 0 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M38 0 Q25 -12 12 0 Q25 12 38 0 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-27 -27 Q-15 -15 -10 -10 Q-15 -15 -27 -27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M27 27 Q15 15 10 10 Q15 15 27 27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-27 27 Q-15 15 -10 10 Q-15 15 -27 27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M27 -27 Q15 -15 10 -10 Q15 -15 27 -27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
        </g>
      `
    },
    watermelon: {
      id: 'watermelon',
      name: '西瓜皮安全帽',
      rarity: 'SSR',
      icon: '🍉',
      desc: '極具迷因感的翠綠西瓜皮安全帽，防護力滿分，搞笑度爆表！',
      svg: `
        <path d="M-28 -5 A28 28 0 0 1 28 -5 Z" fill="#2A9D8F" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-18 -5 Q0 -25 18 -5 M-9 -5 Q0 -20 9 -5 M-25 -5 Q0 -28 25 -5" fill="none" stroke="#1D3557" stroke-width="2" stroke-dasharray="3,3"/>
        <circle cx="0" cy="-28" r="4" fill="#EF476F" stroke="#2B2D42" stroke-width="1"/>
      `
    }
  },
  // --- 身體裝飾 ---
  body: {
    hawaiian: {
      id: 'hawaiian',
      name: '夏威夷花襯衫',
      rarity: 'SR',
      icon: '🌺',
      desc: '鮮豔的熱帶風情襯衫，穿上後柯基走起路來都帶有椰風浪花的氣息。',
      svg: `
        <rect x="-35" y="-12" width="70" height="42" rx="10" fill="#EF476F" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-35 0 Q-25 -8 -15 0 M15 0 Q25 -8 35 0" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
        <circle cx="-15" cy="15" r="3" fill="#FFFFFF"/>
        <circle cx="15" cy="15" r="3" fill="#FFFFFF"/>
      `
    },
    raincoat: {
      id: 'raincoat',
      name: '小黃雨衣',
      rarity: 'SR',
      icon: '🧥',
      desc: '雨天出門散步的必備防護裝！亮黃色讓柯基安全又可愛。',
      svg: `
        <rect x="-36" y="-12" width="72" height="45" rx="8" fill="#FFD166" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-18 -12 L0 -24 L18 -12" fill="none" stroke="#FFD166" stroke-width="8" stroke-linecap="round"/>
        <circle cx="0" cy="5" r="4" fill="#2B2D42"/>
      `
    },
    bee: {
      id: 'bee',
      name: '勤勞蜜蜂裝',
      rarity: 'SSR',
      icon: '🐝',
      desc: '黃黑相間的小蜜蜂套裝，背後還附帶一對小翅膀喔！',
      svg: `
        <!-- 蜜蜂翅膀 -->
        <ellipse cx="-15" cy="-22" rx="12" ry="7" fill="#E0F2FE" stroke="#2B2D42" stroke-width="1.5" transform="rotate(-30, -15, -22)"/>
        <ellipse cx="15" cy="-22" rx="12" ry="7" fill="#E0F2FE" stroke="#2B2D42" stroke-width="1.5" transform="rotate(30, 15, -22)"/>
        
        <!-- 蜜蜂身體 -->
        <rect x="-34" y="-12" width="68" height="42" rx="10" fill="#FFD166" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-22" y="-12" width="8" height="42" fill="#2B2D42"/>
        <rect x="0" y="-12" width="8" height="42" fill="#2B2D42"/>
        <rect x="14" y="-12" width="8" height="42" fill="#2B2D42"/>
      `
    }
  },
  // --- 背部裝飾 ---
  back: {
    backpack: {
      id: 'backpack',
      name: '小學生書包',
      rarity: 'N',
      icon: '🎒',
      desc: '藍色的雙肩小書包，裡面裝著美味的骨頭點心，去散步囉！',
      svg: `
        <rect x="-16" y="-28" width="32" height="28" rx="6" fill="#118AB2" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-10" y="-20" width="20" height="15" rx="3" fill="#06D6A0" stroke="#2B2D42" stroke-width="1.5"/>
        <circle cx="0" cy="-6" r="3" fill="#EF476F"/>
      `
    },
    duck_ring: {
      id: 'duck_ring',
      name: '小鴨游泳圈',
      rarity: 'SR',
      icon: '🦆',
      desc: '去海灘探險的必備法寶！自帶一隻神氣的黃色小鴨鴨。',
      svg: `
        <ellipse cx="0" cy="-4" rx="44" ry="11" fill="#FFD166" stroke="#2B2D42" stroke-width="2" />
        <g transform="translate(30, -15)">
          <circle cx="0" cy="0" r="7" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <polygon points="3,-2 9,1 3,4" fill="#EF476F"/>
          <circle cx="-1.5" cy="-2" r="1.2" fill="#2B2D42"/>
        </g>
      `
    },
    propeller: {
      id: 'propeller',
      name: '竹蜻蜓',
      rarity: 'SSR',
      icon: '🛸',
      desc: '綁在背上的竹蜻蜓，真的會呼呼旋轉！聽說能帶柯基飛天。',
      svg: `
        <line x1="0" y1="-22" x2="0" y2="0" stroke="#2B2D42" stroke-width="2.5"/>
        <g class="propeller-blade-group">
          <ellipse cx="0" cy="-22" rx="26" ry="4" fill="#06D6A0" stroke="#2B2D42" stroke-width="1.5" />
          <circle cx="0" cy="-22" r="2.5" fill="#FFD166"/>
        </g>
        <style>
          .propeller-blade-group {
            animation: spin-propeller 0.15s linear infinite;
            transform-origin: 0px -22px;
          }
          @keyframes spin-propeller {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        </style>
      `
    }
  }
};
