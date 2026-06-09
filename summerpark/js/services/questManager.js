// 每日任務管理器與成就系統
import { gameState, saveGame } from '../store/gameState.js';
import { DAILY_QUEST_POOL, ACHIEVEMENTS } from '../data/quests.js';
import { playSFX } from './audio.js';
import { spawnFloatingText } from '../ui/effects.js';

// 確保 gameState 有任務相關欄位
function ensureQuestFields() {
  if (!gameState.quests) {
    gameState.quests = {
      dailyQuests: [],
      lastRefreshDate: null
    };
  }
  if (!gameState.achievements) {
    gameState.achievements = [];
  }
  if (!gameState.questCounters) {
    gameState.questCounters = {
      pet: 0,
      feed: 0,
      bath: 0,
      train: 0,
      gacha: 0,
      equip: 0,
      walk_complete: 0,
      totalBonesEarned: 0,
      mapsVisited: {}
    };
  }
}

// 取得今天的日期字串 (YYYY-MM-DD)
function getTodayString() {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

// 隨機抽取 N 個不重複的每日任務
function pickDailyQuests(count = 3) {
  const pool = [...DAILY_QUEST_POOL];
  const picked = [];
  for (let i = 0; i < Math.min(count, pool.length); i++) {
    const idx = Math.floor(Math.random() * pool.length);
    const quest = pool.splice(idx, 1)[0];
    picked.push({
      ...quest,
      progress: 0,
      completed: false,
      claimed: false
    });
  }
  return picked;
}

// 檢查並刷新每日任務 (每日 00:00 重置)
export function refreshDailyQuests() {
  ensureQuestFields();
  const today = getTodayString();
  
  if (gameState.quests.lastRefreshDate !== today) {
    // 重置每日計數器
    gameState.questCounters.pet = 0;
    gameState.questCounters.feed = 0;
    gameState.questCounters.bath = 0;
    gameState.questCounters.train = 0;
    gameState.questCounters.gacha = 0;
    gameState.questCounters.equip = 0;
    gameState.questCounters.walk_complete = 0;
    
    // 抽新任務
    gameState.quests.dailyQuests = pickDailyQuests(3);
    gameState.quests.lastRefreshDate = today;
    saveGame();
  }
}

// 記錄動作 (由各 service 呼叫)
export function recordAction(actionType, extra = {}) {
  ensureQuestFields();
  
  if (gameState.questCounters[actionType] !== undefined) {
    gameState.questCounters[actionType]++;
  }
  
  // 散步地圖記錄
  if (actionType === 'walk_complete' && extra.mapId) {
    if (!gameState.questCounters.mapsVisited) {
      gameState.questCounters.mapsVisited = {};
    }
    gameState.questCounters.mapsVisited[extra.mapId] = true;
  }
  
  // 骨頭累計
  if (extra.bonesEarned) {
    gameState.questCounters.totalBonesEarned = 
      (gameState.questCounters.totalBonesEarned || 0) + extra.bonesEarned;
  }
  
  // 檢查每日任務進度
  updateDailyQuestProgress(actionType);
  
  // 檢查成就
  checkAchievements();
  
  saveGame();
}

// 更新每日任務進度
function updateDailyQuestProgress(actionType) {
  if (!gameState.quests?.dailyQuests) return;
  
  gameState.quests.dailyQuests.forEach(quest => {
    if (quest.completed || quest.action !== actionType) return;
    
    quest.progress = gameState.questCounters[actionType] || 0;
    
    if (quest.progress >= quest.target) {
      quest.completed = true;
      // 派發完成事件讓 UI 更新
      window.dispatchEvent(new CustomEvent('quest-completed', { 
        detail: { quest } 
      }));
    }
  });
}

// 領取每日任務獎勵
export function claimQuestReward(questId) {
  ensureQuestFields();
  const quest = gameState.quests.dailyQuests.find(q => q.id === questId);
  if (!quest || !quest.completed || quest.claimed) return false;
  
  quest.claimed = true;
  
  // 發放獎勵
  if (quest.reward.bones) {
    gameState.bones += quest.reward.bones;
    spawnFloatingText('./assets/item-bone.png', ` +${quest.reward.bones}`);
  }
  if (quest.reward.goldBones) {
    gameState.goldBones += quest.reward.goldBones;
    spawnFloatingText('./assets/item-gold-bone.png', ` +${quest.reward.goldBones}`);
  }
  
  playSFX('quest');
  saveGame();
  window.dispatchEvent(new CustomEvent('state-updated'));
  return true;
}

// 檢查成就解鎖
function checkAchievements() {
  ensureQuestFields();
  
  ACHIEVEMENTS.forEach(achievement => {
    if (gameState.achievements.includes(achievement.id)) return;
    
    if (achievement.condition(gameState)) {
      gameState.achievements.push(achievement.id);
      
      // 發放獎勵
      if (achievement.reward.bones) {
        gameState.bones += achievement.reward.bones;
      }
      if (achievement.reward.goldBones) {
        gameState.goldBones += achievement.reward.goldBones;
      }
      
      // 派發成就解鎖事件
      window.dispatchEvent(new CustomEvent('achievement-unlocked', {
        detail: { achievement }
      }));
      window.dispatchEvent(new CustomEvent('state-updated'));
    }
  });
}

// 取得每日任務列表
export function getDailyQuests() {
  ensureQuestFields();
  return gameState.quests.dailyQuests || [];
}

// 取得已解鎖成就列表
export function getUnlockedAchievements() {
  ensureQuestFields();
  return gameState.achievements || [];
}

// 取得所有成就定義
export function getAllAchievements() {
  return ACHIEVEMENTS;
}

// 初始化任務系統 (在遊戲載入後呼叫)
export function initQuestSystem() {
  ensureQuestFields();
  refreshDailyQuests();
  
  // 首次登入成就
  checkAchievements();
}
