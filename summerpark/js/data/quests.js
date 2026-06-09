// 每日任務池與成就定義

export const DAILY_QUEST_POOL = [
  {
    id: 'pet_3',
    name: '早安問候',
    desc: '撫摸柯基 3 次',
    icon: '👋',
    action: 'pet',
    target: 3,
    reward: { bones: 30 }
  },
  {
    id: 'feed_2',
    name: '美食家',
    desc: '餵食柯基 2 次',
    icon: '🍖',
    action: 'feed',
    target: 2,
    reward: { bones: 20 }
  },
  {
    id: 'walk_1',
    name: '探險王',
    desc: '完成 1 次散步冒險',
    icon: '🗺️',
    action: 'walk_complete',
    target: 1,
    reward: { bones: 50, goldBones: 1 }
  },
  {
    id: 'bath_2',
    name: '清潔達人',
    desc: '幫柯基洗澡 2 次',
    icon: '🧼',
    action: 'bath',
    target: 2,
    reward: { bones: 25 }
  },
  {
    id: 'equip_1',
    name: '時尚大師',
    desc: '更換 1 次裝扮',
    icon: '👔',
    action: 'equip',
    target: 1,
    reward: { bones: 15 }
  },
  {
    id: 'train_2',
    name: '努力特訓',
    desc: '完成 2 次特訓',
    icon: '💪',
    action: 'train',
    target: 2,
    reward: { bones: 35 }
  },
  {
    id: 'gacha_1',
    name: '幸運挖寶',
    desc: '進行 1 次扭蛋挖寶',
    icon: '🎁',
    action: 'gacha',
    target: 1,
    reward: { bones: 20 }
  }
];

export const ACHIEVEMENTS = [
  {
    id: 'first_login',
    name: '初來乍到',
    desc: '首次開啟遊戲',
    icon: '🌟',
    condition: (state) => true,  // 永遠成立，首次載入即解鎖
    reward: { bones: 50 }
  },
  {
    id: 'fashion_3',
    name: '時尚柯基',
    desc: '收集 3 件裝扮',
    icon: '👗',
    condition: (state) => state.inventory.length >= 3,
    reward: { goldBones: 2 }
  },
  {
    id: 'world_tour',
    name: '環遊世界',
    desc: '完成所有地圖各至少 1 次散步',
    icon: '🌍',
    condition: (state) => {
      const visited = state.questCounters?.mapsVisited || {};
      return visited.park && visited.beach && visited.camp;
    },
    reward: { goldBones: 5 }
  },
  {
    id: 'rich_dog',
    name: '百萬富狗',
    desc: '累計獲得 1000 骨頭',
    icon: '💰',
    condition: (state) => (state.questCounters?.totalBonesEarned || 0) >= 1000,
    reward: { goldBones: 3 }
  },
  {
    id: 'collector',
    name: '全裝扮收藏家',
    desc: '收集全部 10 件裝扮',
    icon: '🏆',
    condition: (state) => state.inventory.length >= 10,
    reward: { goldBones: 10 }
  },
  {
    id: 'speed_50',
    name: '閃電飛毛腿',
    desc: '速度達到 50',
    icon: '⚡',
    condition: (state) => state.attributes.speed >= 50,
    reward: { bones: 80 }
  },
  {
    id: 'charm_50',
    name: '萬人迷',
    desc: '魅力達到 50',
    icon: '💖',
    condition: (state) => state.attributes.charm >= 50,
    reward: { bones: 80 }
  },
  {
    id: 'iq_50',
    name: '天才柯基',
    desc: '智商達到 50',
    icon: '🧠',
    condition: (state) => state.attributes.iq >= 50,
    reward: { bones: 80 }
  }
];
