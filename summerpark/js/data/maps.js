export const EXPLORATION_MAPS = {
  park: {
    name: '陽光綠地',
    bg: './assets/background-park.png',
    duration: 60, // 60 秒 (開發利於測試)
    cost: 15,     // 消耗心情
    goldCost: 0,
    drops: ['strawhat', 'backpack'],
    events: [
      '柯基在公園草皮上跟一隻金毛大狗搶飛盤，跑得氣喘吁吁，【速度】增加了！',
      '柯基把頭埋進消防栓底下的草叢，雖然吃了一嘴草，但也意外刨出了幾根骨頭！',
      '柯基在草地上瘋狂用大屁股蹭草地蹭了十分鐘，吸引了旁邊小女孩的拍照，【魅力】提升！',
      '柯基在消防栓旁留下了自己的地盤記號，感覺非常神氣！'
    ]
  },
  beach: {
    name: '夏日海灘',
    bg: './assets/background-beach.png',
    duration: 180, // 3 分鐘
    cost: 30,
    goldCost: 0,
    drops: ['sunglasses', 'hawaiian', 'duck_ring'],
    events: [
      '柯基在沙灘上跟著海浪玩起你追我跑的遊戲，被海浪潑濕了屁股，但【速度】增加了！',
      '柯基認真地在沙灘上刨出了一個沙堡，惹得路人連連讚嘆並紛紛投餵！',
      '柯基在日光浴躺椅旁對著曬太陽的遊客瘋狂搖尾巴撒嬌，獲得了亮晶晶的貝殼裝飾！',
      '柯基海灘狂奔，耳朵被鹹鹹的海風吹成飛天狀態，笑得合不攏嘴！'
    ]
  },
  camp: {
    name: '森林營地',
    bg: './assets/background-camp.png',
    duration: 300, // 5 分鐘
    cost: 50,
    goldCost: 0,
    drops: ['sunflower', 'watermelon', 'raincoat', 'bee', 'propeller'],
    events: [
      '深夜的營火晚會上，柯基圍著營火跳起了小碎步舞蹈，烤棉花糖的香味讓牠【智商】大增！',
      '柯基一頭鑽進大樹洞裡想抓松鼠，結果屁股太大卡在樹洞口，掙扎著爬出來時帶出了一枚黃金寶箱！',
      '柯基在螢火蟲飛舞的林間小徑上漫步，月光灑在牠圓滾滾的身軀上，散發出夢幻的【魅力】！',
      '森林裡突然下起了小雨，幸好柯基躲在松樹下避雨，還意外撿到了林間小矮人的餽贈！'
    ]
  }
};
