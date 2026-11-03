# VCT CN Player Atlas

Extend the existing ZmjjKK motion language into a collection, preserving the original URL. Publish the collection at `/cn/` and standalone player pages at `/cn/players/<id>/`.

Palette: cold paper #eef1ef, ink #182b34, navy #101c23, VALORANT red #ff4655, cyan #a6e4e7. Each team's accent and paper tone personalize the same layout. Manrope carries player handles and navigation; Georgia is limited to the existing oversized display rhythm.

The directory opens with a cast of actual player cutouts and oversized “CN / ALL STARS” typography, then a searchable roster arranged by team. The key visual is a portrait wall, not a metrics dashboard. Filters and page changes respond visibly to user action; only the visible hero scene renders a continuous mask.

Individual pages retain a full-viewport portrait / agent reveal, a scroll-shrinking central frame and oversized ID wordmark, an opposing player/agent composition, a horizontal match-story reel, interactive agent pool and recent results. Official player portraits and Riot character art are shared locally. A wordmark must never be described as an autograph. Only the preserved ZmjjKK page has verified handwriting. Dates, photos, statistics and links must come from that player's data; do not copy ZmjjKK's achievements into other pages.

Roster scope: 2026 VCT CN's 12 participants, current VLR roster snapshot, with substitutes and inactive players clearly identified and staff excluded. Official team pages provide primary portrait sources; discrepancies and unmatched aliases use the VLR portrait with explicit attribution. Keep sources with each player.

The static generator is the source of all pages. Shared CSS, animation JS and character artwork prevent duplicated downloads. Every player has a direct link and works on GitHub Pages under a repository subpath, and local file URLs. No server or key is required at runtime.

## Original-site alignment: 2026-11-03

The first batch was visually weaker than the original. The shared profile now ports the actual original ZmjjKK CSS and animation sequence rather than approximating it: contour backdrop, large face-aligned organic reveal, pointer displacement, 0.34 desktop / 0.70 mobile hero reduction, oversized fitted ID, paired portraits, a full-screen typographic section, independently moving photo layers, agent display and an expanding feature photograph. `atlas_profile.py`, `atlas_styles.py`, `profile-layout.css` and `profile-structure.css` own the shared output. The original site remains the reference source of its visual rules; layout adapters handle the generated content.

Portrait framing coordinates are saved in `data/vctcn-framing.json`. The paired scene uses actual frontal player portraits and clearly credited frontal agent concepts. It does not claim to reproduce a photographic side-profile scene for every player. Only the original Kangkang page includes the verified handwriting and its labelled AI concept profiles.

42 players now have 320 real official photographs. The remaining 31 profiles have varied, truthfully labelled editorial chapters. They keep the same motion sequence without repeating a player cutout four times. The directory's Kangkang card and featured link open the original root page.

## Portrait clarity and reveal registration: 2026-11-03

Restore all 70 real player portraits from their native sources and encode them losslessly, without regenerating faces or inventing extra photographic detail. Render the hero, offscreen composites and paired canvases at the device pixel ratio, capped at 3x / 8.3 million pixels per canvas. Eye spacing controls the face size so low-resolution originals are no longer aggressively enlarged by a bounding-box crop.

Save measured iris centers for all 70 real portraits. The 13 most-used agent identities have 1024 x 1536 transparent frontal concepts made with imagegen from their official artwork. Their pupil or visor anchors are reviewed manually in `data/vctcn-agent-portraits.json`. Uniform scaling, translation and rotation put both subjects on the same eye line and eye spacing. No face warp or generated player face is used.

The reveal uses one connected, softly feathered contour that follows the pointer. Only its boundary moves slightly. Complementary premultiplied layers prevent a translucent seam; portrait bodies and faces receive no blur. The fully revealed agent remains available through the explicit toggle, including reduced-motion and touch use. Waist-edge fading follows the portrait's rotation. Official full-body art remains in agent statistics and editorial sections.
