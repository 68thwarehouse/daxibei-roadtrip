# 大西北环线工作台 · 多人实时共享版 — 部署说明

本目录是一个**零依赖**的全栈小应用：

- `server.js`：原生 Node `http` 服务，托管前端 + 提供共享状态接口
  - `GET  /api/state` 读取共享状态（落盘 `data/state.json`）
  - `POST /api/state` 保存共享状态（带版本号）
  - `GET  /api/stream` SSE 实时推送，任何一端保存后其他人**秒级刷新**
- `public/index.html`：工作台前端（由 `build_html_v2.py` 生成，已内置共享同步逻辑）
- `data/state.json`：运行时自动生成的共享数据文件

## 本地运行 / 自测

```bash
node server.js
# 打开 http://localhost:3000
```

打开两个浏览器标签访问同一地址，在 A 标签里改行程/勾选，B 标签会**自动同步**。

## 部署到「支持 Node 的云平台」（让所有人都能访问）

CloudStudio 仅支持纯静态站点，无法运行后端，因此本应用需部署到支持 Node 的平台。
本项目已附带通用配置，任选其一即可：

### 方案 A：Render（最省事，免费额度可用）
1. 把本目录推到 GitHub 仓库。
2. 打开 https://render.com → New → Web Service → 关联仓库。
3. 关键设置：
   - Runtime: `Node`
   - Build Command: `echo no-build`
   - Start Command: `node server.js`
   - 免费版需勾选 "Deploy a new instance" 或保持免费计划。
4. 部署完成后会得到一个 `https://xxx.onrender.com` 公开链接，发给群里所有人即可。

> 持久化：免费实例休眠/重启可能清空 `./data`。如需数据长期不丢，在 Render
> 控制台为该服务挂载一个 Disk（mountPath `/data`）即可，代码无需改动。

### 方案 B：Railway / Fly.io
同样上传本目录，`start` 命令 `node server.js`，平台会读取 `package.json` 的 start 脚本。

### 方案 C：自有 VPS
```bash
git clone <仓库> && cd <目录>
node server.js        # 生产建议用 pm2: npm i -g pm2 && pm2 start server.js
# 用 Nginx 反代 3000 端口并配 HTTPS
```

## 降级说明
若前端访问不到 `/api/state`（例如仍用 CloudStudio 静态托管或本地双击打开），
页面会自动进入「📱 本地模式」——改动只存本机浏览器，不影响他人。只要通过本后端服务访问，就是「🌐 云端共享」模式。
