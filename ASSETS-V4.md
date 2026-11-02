# V4 asset provenance

The dated photo gallery uses original event photographs. See `photo-sources-v4.json` for the 10 displayed items, and `photo-research-v4.json` for the retrieved Riot Flickr captions and image URLs.

## Authentic handwriting

Original report: https://www.bilibili.com/opus/977975778598715408 . Author: 丹尼二狗; photography: 一村 (Liu Yicun). Section five describes obtaining ZmjjKK's signature on official manga after the June 20, 2023 Tokyo match. The photograph immediately after that paragraph contains his handwritten ID and `6.20` date.

Original image: https://i0.hdslb.com/bfs/new_dyn/c19a8b7f3e3873b7d62e5cf2f1182dfc3891857.jpg . Saved intact as `dist/assets/kk-signature-source.jpg` (5000 × 3333). The page uses SVG clipping and a color matrix to isolate the purple ink and display it in VALORANT red. It does not generate or redraw the signature. The source button opens the complete original image with a link to the article. Texture and imperfections in the original pen strokes remain visible.

## Face-to-face concept scene

Created with the built-in imagegen tool. These are AI-assisted concept portraits, labelled in the scene and source dialog; they are not presented as original event photos.

- Kangkang references: [Riot London Features 2026](https://www.flickr.com/photos/valorantesports/55332417994/) and [Riot Bangkok Playoffs 2025](https://www.flickr.com/photos/valorantesports/54356393075/).
- Jett reference: original Riot character illustration served by [Valorant-API](https://valorant-api.com/).
- Final assets: `dist/assets/kk-profile-v4.webp` and `dist/assets/jett-profile-v4.webp`, with transparency preserved. Unused working images and duplicate PNG/JPEG files were removed from the release.

Kangkang prompt:

> 制作网页里的康康 ZmjjKK 侧面头肩肖像，透明背景，竖向3:4。两张参考都是同一个人：图一用于准确保留他2026年的脸型、较长黑发、黑框眼镜和白红EDG队服；图二用于理解真实侧脸轮廓。输出一位真人康康的严格左向侧脸，鼻尖朝画面左边，目光水平向左，眼镜清晰，头部不抬不低。构图只到肩膀及上胸，头顶完整，肩部下缘自然被画布底部裁切。用于网页右侧与另一个角色面对面。去掉原背景、举起的手、耳机、座椅和电脑，双手不入画。保留真实脸型、圆润下颌、肤质、发型，不美颜瘦脸，不变成另一个人。真实体育人物摄影，柔和自然光，无夸张彩色灯光。只输出一个人物抠图，清晰透明alpha背景，没有文字，没有图形和阴影底板。

Jett prompt:

> 制作《VALORANT》捷风 Jett 的右向侧面头肩立绘，透明背景，竖向3:4。参考图是角色身份与原作美术依据。只画一个捷风，鼻尖严格朝画面右边，目光水平向右，适用于网页左侧与真人选手面对面的镜头。银白发、高马尾、蓝灰眼睛，原作深海军蓝高领和浅青战术服。完整头顶和发髻，裁到肩膀及上胸，肩部下缘自然到画布底部。原版VALORANT切面笔触、准确脸型与衣领结构，不要卡通Q版，不要真人cosplay，不要手臂手掌，不要武器和风效。正侧面，克制自信的表情。清晰透明alpha背景，没有文字、没有场景、没有阴影底板。
