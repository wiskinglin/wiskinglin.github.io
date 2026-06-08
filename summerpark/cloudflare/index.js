// Cloudflare Workers API 同步網關程式

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 處理 CORS 預檢請求
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, X-User-Id",
          "Access-Control-Max-Age": "86400",
        }
      });
    }

    // CORS 頭資訊
    const corsHeaders = {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json"
    };

    // 路由 1: POST /api/sync - 上傳並備份遊戲存檔
    if (url.pathname === "/api/sync" && request.method === "POST") {
      try {
        const body = await request.json();
        
        // 獲取使用者 ID (通常自自定義 Header 或存檔內部，這裡自 header 讀取，預設取遊戲自帶的存檔屬性)
        const userId = request.headers.get("X-User-Id") || "default_player";
        
        const saveDataStr = JSON.stringify(body);
        const corgiName = body.name || "小薯條";

        // 使用 D1 寫入數據 (使用 INSERT OR REPLACE 簡化語法)
        await env.DB.prepare(
          "INSERT OR REPLACE INTO users (id, name) VALUES (?, ?)"
        ).bind(userId, corgiName).run();

        await env.DB.prepare(
          "INSERT OR REPLACE INTO saves (user_id, save_data, updated_at) VALUES (?, ?, ?)"
        ).bind(userId, saveDataStr, Date.now()).run();

        return new Response(JSON.stringify({ success: true, message: "存檔同步成功！" }), {
          status: 200,
          headers: corsHeaders
        });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 路由 2: GET /api/sync - 下載並恢復遊戲存檔
    if (url.pathname === "/api/sync" && request.method === "GET") {
      try {
        const userId = url.searchParams.get("userId") || "default_player";

        const row = await env.DB.prepare(
          "SELECT save_data FROM saves WHERE user_id = ?"
        ).bind(userId).first();

        if (!row) {
          return new Response(JSON.stringify({ success: false, message: "無此玩家存檔記錄" }), {
            status: 404,
            headers: corsHeaders
          });
        }

        return new Response(row.save_data, {
          status: 200,
          headers: corsHeaders
        });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 404
    return new Response(JSON.stringify({ error: "路徑未找到" }), {
      status: 404,
      headers: corsHeaders
    });
  }
};
