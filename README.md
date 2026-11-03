# VCT CN Player Atlas

VCT CN 选手个人站合集，沿用 ZmjjKK × Jett 的人物显影、滚动缩放和影像长卷语言。首批覆盖 **12 支战队、73 位选手**：62 位公开阵容选手、7 位替补、4 位非活跃选手。

- [打开选手合集](https://zmjjkk.jxznai.cc.cd/cn/)
- [原版 ZmjjKK × Jett](https://zmjjkk.jxznai.cc.cd/)

## 浏览

双击 `START.cmd` 打开合集。原版康康页面保留在 `dist/index.html`。所有运行用的图片、字体和脚本均在本地；外部来源与比赛链接需联网。

合集支持选手 ID / 中英文姓名搜索、12 战队筛选、主要英雄定位、地图数 / 击杀数排序，以及画廊 / 列表切换。筛选条件保存在链接中，方便分享。

每位选手均有独立静态页面，展示个人肖像、主要英雄显影、滚动缩放、选手与英雄组合画面、分层影像长卷、最多四位英雄的联动统计，以及可展开的最近比赛。主题配色跟随战队。数据是 2026-11-02 的公开快照，不是实时转会信息。

## 构建与部署

```sh
python scripts/build-atlas.py
node --check dist/app.js
node --check dist/cn/atlas.js
node --check dist/cn/profile.js
node check-source.cjs
node validate-atlas.cjs
```

构建脚本只使用 Python 标准库。数据采集脚本单独需要 BeautifulSoup 和 Pillow；可选的肖像测量脚本需要 OpenCV；发布的网站没有运行依赖、后端或 API Key。

- `data/`：经过整理的阵容、个人统计及素材来源。
- `scripts/build-atlas.py`：统一生成合集与 73 个个人站。
- `dist/cn/atlas.*`：合集的布局与筛选交互。
- `dist/cn/profile.*`：全部个人站共享的版式与动效。
- `.github/workflows/pages.yml`：推送到 main 后校验并部署 dist。

## 资料和限制

人物肖像来自 Riot 官方或 VLR 公开资料。3 位选手暂无公开肖像，1 位暂无英雄统计，均有明确说明。2026-11-03 视觉更新重新使用原版的动画编排和样式，校准人物与英雄近景，补入 42 位选手的 320 张 Riot 官方赛场照片。其余 31 位的长卷使用明确标注的肖像、英雄原画和比赛档案。合集中的康康直接进入原版。原康康站的真实签名和已有赛事图库继续保留。

详见 `ATLAS-SOURCES.md`；设计说明见 `ATLAS-DESIGN.md`。原康康站的素材说明和验证记录见 `ASSETS-V4.md`、`VALIDATION-V4.json`。

已检查桌面、手机、搜索与组合筛选、直达链接、人物显影、英雄切换、减少动态和无统计状态。静态校验覆盖全部 73 个页面和引用素材。Canvas 2D 动效未实测低端设备帧率。

非官方粉丝项目。照片、角色、赛事影像和商标归各自权利人所有，不代表选手、俱乐部或 Riot Games。
