# VCT CN Player Atlas

Extend the existing ZmjjKK motion language into a collection, preserving the original URL. Publish the collection at `/cn/` and standalone player pages at `/cn/players/<id>/`.

Palette: cold paper #eef1ef, ink #182b34, navy #101c23, VALORANT red #ff4655, cyan #a6e4e7. Each team's accent and paper tone personalize the same layout. Manrope carries player handles and navigation; Georgia is limited to the existing oversized display rhythm.

The directory opens with a cast of actual player cutouts and oversized “CN / ALL STARS” typography, then a searchable roster arranged by team. The key visual is a portrait wall, not a metrics dashboard. Filters and page changes respond visibly to user action; only the visible hero scene renders a continuous mask.

Individual pages retain a full-viewport portrait / agent reveal, a scroll-shrinking central frame and oversized ID wordmark, an opposing player/agent composition, a horizontal match-story reel, interactive agent pool and recent results. Official player portraits and Riot character art are shared locally. A wordmark must never be described as an autograph. Only the preserved ZmjjKK page has verified handwriting. Dates, photos, statistics and links must come from that player's data; do not copy ZmjjKK's achievements into other pages.

Roster scope: 2026 VCT CN's 12 participants, current VLR roster snapshot, with substitutes and inactive players clearly identified and staff excluded. Official team pages provide primary portrait sources; discrepancies and unmatched aliases use the VLR portrait with explicit attribution. Keep sources with each player.

The static generator is the source of all pages. Shared CSS, animation JS and character artwork prevent duplicated downloads. Every player has a direct link and works on GitHub Pages under a repository subpath, and local file URLs. No server or key is required at runtime.

## Original-site alignment: 2026-11-03

The first batch was visually weaker than the original. The shared profile now ports the actual original ZmjjKK CSS and animation sequence rather than approximating it: contour backdrop, large face-aligned organic reveal, pointer displacement, 0.34 desktop / 0.70 mobile hero reduction, oversized fitted ID, paired portraits, a full-screen typographic section, independently moving photo layers, agent display and an expanding feature photograph. `atlas_profile.py`, `atlas_styles.py`, `profile-layout.css` and `profile-structure.css` own the shared output. The original site remains the reference source of its visual rules; layout adapters handle the generated content.

Portrait framing coordinates are saved in `data/vctcn-framing.json`; agent face positions are calibrated against the official artwork. The paired scene uses actual frontal player portraits and official hero artwork. It does not claim to reproduce a photographic side-profile scene for every player. Only the original Kangkang page includes the verified handwriting and its labelled AI concept profiles.

42 players now have 320 real official photographs. The remaining 31 profiles have varied, truthfully labelled editorial chapters. They keep the same motion sequence without repeating a player cutout four times. The directory's Kangkang card and featured link open the original root page.
