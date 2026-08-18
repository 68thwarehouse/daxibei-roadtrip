/**
 * 大西北环线工作台 · 共享后端服务（零依赖 Node 原生 http）
 *
 * 职责：
 *   1. 托管 public/ 下的静态前端（index.html 等）
 *   2. GET  /api/state   -> 读取共享状态（落盘 data/state.json）
 *   3. POST /api/state   -> 保存共享状态并广播给所有在线用户
 *   4. GET  /api/stream  -> SSE 实时推送，任何一端保存后其他人即时刷新
 *
 * 运行： node server.js   （端口取 process.env.PORT 或 3000）
 * 部署： 直接把这个目录推到支持 Node 的平台（Render / Railway / Fly / VPS）即可，
 *        平台会自动执行 package.json 的 start 脚本。无需 npm install。
 */
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');

const __dirname0 = __dirname;
const PUBLIC_DIR = path.join(__dirname0, 'public');
const DATA_DIR = path.join(__dirname0, 'data');
const STATE_FILE = path.join(DATA_DIR, 'state.json');
const PORT = process.env.PORT || 3000;
const MAX_BODY = 6 * 1024 * 1024; // 6MB 上限，防滥用

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

// SSE 客户端集合
const clients = new Set();

// ---------- 状态读写（带版本号，便于前端判断回声） ----------
function readState() {
  try {
    const raw = fs.readFileSync(STATE_FILE, 'utf8');
    const obj = JSON.parse(raw);
    if (typeof obj.version !== 'number') obj.version = 1;
    return obj;
  } catch (e) {
    return { state: null, version: 0, updatedAt: null };
  }
}

function writeState(newState, from) {
  const cur = readState();
  const next = {
    state: newState,
    version: (cur.version || 0) + 1,
    updatedAt: Date.now(),
    from: from || null, // 发起者 clientId，用于客户端忽略自身回声
  };
  // 原子写入：先写临时文件再 rename，避免并发读到半截
  const tmp = STATE_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(next), 'utf8');
  fs.renameSync(tmp, STATE_FILE);
  broadcast(next);
  return next;
}

function broadcast(obj) {
  const payload = 'event: update\ndata: ' + JSON.stringify(obj) + '\n\n';
  clients.forEach((res) => {
    try { res.write(payload); } catch (e) { clients.delete(res); }
  });
}

// ---------- 静态文件服务 ----------
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};

function serveStatic(req, res, pathname) {
  let rel = pathname === '/' ? '/index.html' : pathname;
  // 防目录穿越
  const filePath = path.normalize(path.join(PUBLIC_DIR, rel));
  if (!filePath.startsWith(PUBLIC_DIR)) { res.writeHead(403); return res.end('Forbidden'); }
  fs.readFile(filePath, (err, buf) => {
    if (err) {
      // SPA 兜底：找不到的非资源路径回退到 index.html
      if (!path.extname(filePath)) {
        return fs.readFile(path.join(PUBLIC_DIR, 'index.html'), (e2, b2) => {
          if (e2) { res.writeHead(404); return res.end('Not found'); }
          res.writeHead(200, { 'Content-Type': MIME['.html'] });
          res.end(b2);
        });
      }
      res.writeHead(404); return res.end('Not found');
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(buf);
  });
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > MAX_BODY) { reject(new Error('body too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

// ---------- 请求路由 ----------
const server = http.createServer(async (req, res) => {
  const u = new URL(req.url, 'http://localhost');
  const p = u.pathname;
  // CORS：同源即可，放行 * 以便本地 file 调试
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

  // ---- SSE 实时流 ----
  if (p === '/api/stream' && req.method === 'GET') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
    });
    res.write('retry: 3000\n\n');
    // 新连接立即推送当前状态（迟到者也能同步）
    const cur = readState();
    res.write('event: update\ndata: ' + JSON.stringify(cur) + '\n\n');
    clients.add(res);
    // 保活
    const ka = setInterval(() => { try { res.write(': ping\n\n'); } catch (e) {} }, 25000);
    req.on('close', () => { clearInterval(ka); clients.delete(res); });
    return;
  }

  // ---- 读取共享状态 ----
  if (p === '/api/state' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': MIME['.json'] });
    return res.end(JSON.stringify(readState()));
  }

  // ---- 保存共享状态 ----
  if (p === '/api/state' && req.method === 'POST') {
    try {
      const body = await readBody(req);
      let parsed;
      try { parsed = JSON.parse(body); } catch (e) { res.writeHead(400); return res.end('bad json'); }
      if (!parsed || typeof parsed.state !== 'object' || parsed.state === null) {
        res.writeHead(400); return res.end('state required');
      }
      const next = writeState(parsed.state, parsed.clientId);
      res.writeHead(200, { 'Content-Type': MIME['.json'] });
      return res.end(JSON.stringify({ ok: true, version: next.version, updatedAt: next.updatedAt }));
    } catch (e) {
      res.writeHead(413); return res.end('body too large');
    }
  }

  // ---- 静态资源 ----
  if (req.method === 'GET' || req.method === 'HEAD') {
    return serveStatic(req, res, p);
  }

  res.writeHead(405); res.end('Method Not Allowed');
});

server.listen(PORT, () => {
  console.log('大西北环线工作台 · 共享服务已启动: http://localhost:' + PORT);
  console.log('  静态目录:', PUBLIC_DIR);
  console.log('  共享状态:', STATE_FILE);
});
