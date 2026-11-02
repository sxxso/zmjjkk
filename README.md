# ZmjjKK × Jett

以康康 ZmjjKK 为主角的非官方 VALORANT 粉丝网站。参考 Lando Norris 官网的画面组织与滚动节奏，使用瓦洛兰特红、冷白、深蓝黑。

## 浏览

- GitHub Pages：https://sxxso.github.io/zmjjkk-player-site/
- 本地：双击 `START.cmd` 或打开 `dist/index.html`。无需安装依赖，页面素材、字体和脚本均可离线加载；外部来源和视频链接需要联网。

## 内容与交互

- 康康与捷风近景肖像，鼠标/触摸触发连续流动显影，并可完整切换人物。
- 首屏随滚动缩为中央画幅，叠加本人真实签名；返回首页时复位。
- 捷风与康康面对面镜头，连接英雄池和赛场影像。
- 2023—2026 年共 10 张照片，包含 2025、2026 年各三张官方照片；支持年份跳转、放大、原始来源查看。
- 捷风、雷兹、尚勃勒、霓虹的职业出场地图数和战绩，以及 2024 冠军章节。
- 响应式布局、键盘操作及减少动态模式。

## 维护与部署

直接编辑 `dist/index.html`、`dist/style.css`、`dist/app.js`。英雄数据位于 `dist/agent-data.js`，统计口径和日期显示在页面上。

```sh
node --check dist/app.js
node check-source.cjs
```

推送至 GitHub 的 `main` 后，Actions 会检查数据和本地素材引用，再把 `dist` 部署到 GitHub Pages。工作流见 `.github/workflows/pages.yml`。

## 素材与验证

真实签名取自记者丹尼二狗原文与摄影师一村的照片；保留完整原照片及原有笔迹。页面用 SVG 分离紫色墨迹并按主题着色，未生成或重画签名。

面对面侧脸和首屏捷风为 AI 辅助概念素材，已在页面标注；图库使用真实赛事照片。具体来源见 `ASSETS-V4.md`、`photo-sources-v4.json` 和 `photo-research-v4.json`。

桌面、手机、离线模式、人物切换、缩放复位、图库、菜单和减少动态模式已检查，记录见 `VALIDATION-V4.json`。采用 Canvas 2D，并非原站 WebGL 扭曲的一比一复制；未实测低端设备帧率。

照片、角色、赛事影像与商标归各自权利人所有。本项目不代表选手、EDG 或 Riot Games。
