# VCT CN Player Atlas: sources and scope

Snapshot: **2026-11-02**. Scope: the 12 teams participating in the 2026 VCT CN season. This is a fan-made collection, not an official league product or a live transfer tracker.

The source snapshot contains **73 players**: 62 listed roster players, 7 substitutes and 4 inactive players. Coaching, managerial, analyst and other staff entries are excluded. The directory can include or hide substitutes/inactive players. These statuses follow the current VLR team roster at retrieval time; official team pages sometimes retain a different seasonal lineup. Portrait matching does not override roster membership.

## Attribution

- [Riot's 2026 league handbook](https://valorantesports.com/en-US/season/115571062868511862/handbook): the VCT CN team field.
- Team roster URLs, Riot team pages and portrait URLs: `data/vctcn-rosters.json`.
- Each player's own VLR profile: identity, all-time agent rows and recent matches. Original numeric cells are retained beside normalized fields in `data/vctcn-players.json`; `validate-atlas.cjs` verifies map counts, ACS, K/D, kills and first kills against these cells.
- Portraits: **68 matched Riot official portraits**, **2 other public VLR portraits**, and **3 VLR generic silhouettes** where a verified portrait was unavailable. Missing portraits are visibly labelled. Those players are 77even, kodeth and Toosy. `nothing` currently has no VLR agent or match rows; the page explicitly shows that state.
- Character art: Riot Games, delivered via [Valorant-API](https://valorant-api.com/). The localized names, roles and original image URLs are retained in `data/vctcn-agents.json`.
- The original ZmjjKK website, verified signature photograph and existing dated gallery remain at the original root URL. Its detailed credits remain in `ASSETS-V4.md` and its in-page source dialog.

## Gallery limitation

Public searches on Riot's Flickr account returned photo descriptions and CDN URLs, but downloads of newly requested photos returned HTTP 403. Retrying outside the sandbox, alternate sizes, the original photo page and alternate Flickr domains did not resolve that response. Broken photo files are not included in the new pages. Each populated player page instead has a horizontal **portrait and match-data poster reel**, linking directly to the source match and clearly labelled as a data poster. This is not presented as an original event photograph. The collection contains no newly generated player photos or invented autographs.

## Maintenance

The publication is static and has no runtime package dependencies or API keys.

```sh
# Generate all pages from the reviewed source snapshot (standard Python library only).
python scripts/build-atlas.py
node validate-atlas.cjs

# Data collection only: requires beautifulsoup4 and Pillow, and network access.
python scripts/collect-vctcn.py
python scripts/collect-players.py
```

The collection scripts cache original responses outside the repository at `../output/vctcn-cache/`; the reviewed snapshot JSON is what is committed. Review the snapshot date, seasonal scope, roster changes, portrait matches and any unavailable image source before accepting a refreshed dataset. Do not publish the raw HTML cache. Missing values remain missing; no fallback borrows another player's achievements or signature.
