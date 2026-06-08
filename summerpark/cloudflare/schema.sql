-- Cloudflare D1 資料庫結構

-- 使用者表格
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,          -- 使用者唯一 ID (例如 uuid 或 登入 token)
  name TEXT NOT NULL,           -- 柯基名字
  created_at INTEGER DEFAULT (strftime('%s', 'now') * 1000)
);

-- 存檔備份表格
CREATE TABLE IF NOT EXISTS saves (
  user_id TEXT PRIMARY KEY,     -- 外鍵關聯 users(id)
  save_data TEXT NOT NULL,      -- JSON 序列化存檔字串 (包含 bones, attributes, inventory, equipped 等)
  updated_at INTEGER DEFAULT (strftime('%s', 'now') * 1000),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
