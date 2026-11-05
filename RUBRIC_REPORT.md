# Prompt Kit PH — OSP fidelity rubric report

**Audit date:** 2026-11-05 (Asia/Manila)  
**Repo:** `/workspace/prompt-kit-ph`  
**Live site:** https://mjd.johnnybodegas.com  
**OSP source:** https://opensourcepromptph.com (fresh `wp-json` + PDF downloads via curl)  
**Commit after fixes:** `dd91134b1912b29c9517e66d0cd1bfa5fda83501`  
**Pages build:** `built` (verified after push)  
**Tests:** `python3 tests/test_site.py` → **0 failures**

## Method

- Re-downloaded all candidate OSP PDFs with curl; sha256 vs `site/pdfs/`, `docs/downloads/`, and live `/downloads/<slug>.pdf`.
- Compared `#p-package` (HTML-unescaped) to `pdftotext -layout` line-for-line; page counts via `pdfinfo`; raw-word presence check.
- Playwright (clipboard permissions) Copy all on local `python3 -m http.server 8842 -d docs`.
- Mobile: Playwright 390×844 and 360×740 (`is_mobile`, touch) on home, `/kits/`, all 13 kits, `/guides/`, `/builder/`, `/about/`; screenshots reviewed.
- Live re-check after Pages deploy for R2/R3/R4/R9 samples.

## Mapping used (newest OSP homepage posts)

| Kit slug | OSP post (newest) | OSP PDF file | Post date |
|---|---|---|---|
| science-legend-explainer | Science legend-Advance Prompt Creator Kit-AI Prompt Framework.pdf | Science-legend-Advance-Prompt-Creator-Kit.pdf | 2026-11-03 |
| logo-history-explainer | Logo History -Advance Prompt Creator Kit-AI Prompt Framework.pdf | Logo-History-Advance-Prompt-Creator-Kit.pdf | 2026-11-03 |
| drink-history-explainer | Liquor History -Advance Prompt Creator Kit-AI Prompt Framework.pdf (`…-pdf-2/`) | Liquor-History-Advance-Prompt-Creator-Kit.pdf | 2026-11-03 |
| dog-breed-explainer | Dog Breed -Advance Prompt Creator Kit-AI Prompt Framework.pdf (`…-pdf-2/`) | Dog-Breed-Advance-Prompt-Creator-Kit.pdf | 2026-11-03 |
| cat-breed-explainer | Cat Breed-Advance Prompt Creator Kit-AI Prompt Framework.pdf (`…-pdf-2/`) | Cat-Breed-Advance-Prompt-Creator-Kit.pdf | 2026-11-03 |
| gadget-explainer | 2D_ZackStyle Gadget Explainer Creator Kit- AI Prompt Framework.pdf | 2D_ZackStyle-Gadget-Explainer.pdf | 2026-11-03 |
| what-if-map-cartoon | WHATIF MAP CARTOON EXPLAINER Creator Kit- AI Prompt Framework.pdf | WHATIF_MAP_CARTOON_EXPLAINER_V1.pdf | 2026-11-02 |
| dwarf-planet-origin-map | ERIS ORIGIN MAP EXPLAINER Creator Kit- AI Prompt Framework.pdf | claude_Eris_Cosmic_Origin_Map_Reels.pdf | 2026-11-01 |
| cosmic-origin-map | COSMIC ORIGIN MAP EXPLAINER Creator Kit- AI Prompt Framework.pdf | COSMIC-ORIGIN-MAP-EXPLAINER.pdf | 2026-10-31 |
| unusual-jobs-explainer | Dark Job Creator Kit- AI Prompt Framework.pdf | Dark-Job-Creator-Kit.pdf | 2026-10-31 |

## Duplicate OSP posts (R1)

| Kit | Candidates | PDF sha256 new vs old |
|---|---|---|
| drink-history | Nov 3 `…-pdf-2/` + Oct 31 non-`-2` | **identical** |
| dog-breed | Nov 3 `…-pdf-2/` + Oct 31 Advance + Dog Breed-v1/v2 (different kits) | Advance Oct/Nov **identical**; v1/v2 are other PDFs (not used) |
| cat-breed | Nov 3 `…-pdf-2/` + Oct 31 Advance + Cat Breeds-v1/v2 | Advance Oct/Nov **identical**; v1/v2 other PDFs (not used) |

**Johnny decision:** none required for content — older Advance duplicates are byte-identical to the newest. Site correctly uses newest homepage posts. Older WP URLs remain published on OSP but same file bytes for the three Advance pairs.

## Kit title mismatches (R2 — not renamed)

Kit page H1 kept; visible `Original title:` / `Original: <title> (<filename>)` added in Full package block.

| Kit H1 | Exact OSP post title |
|---|---|
| Drink History Explainer Kit | Liquor History -Advance Prompt Creator Kit-AI Prompt Framework.pdf |
| Unusual Jobs Explainer Kit | Dark Job Creator Kit- AI Prompt Framework.pdf |
| Dwarf Planet Origin Map Kit | ERIS ORIGIN MAP EXPLAINER Creator Kit- AI Prompt Framework.pdf |
| Gadget Explainer Kit | 2D_ZackStyle Gadget Explainer Creator Kit- AI Prompt Framework.pdf |
| What If Map Cartoon Kit | WHATIF MAP CARTOON EXPLAINER Creator Kit- AI Prompt Framework.pdf |
| (others) | similarly shorter kit branding vs long OSP `.pdf` post titles |

## Scorecard (after fix + live re-verify)

Legend: **PASS** = verified against live sources this run. SITE = whole-site row.

| Kit / scope | R1 source | R2 orig name | R3 byte PDF | R4 text/pages | R5 copy+DL | R6 unaltered | R7 visual | R9 mobile |
|---|---|---|---|---|---|---|---|---|
| science-legend-explainer | PASS | PASS | PASS | PASS (7p) | PASS | PASS | PASS | PASS |
| logo-history-explainer | PASS | PASS | PASS | PASS (6p) | PASS | PASS | PASS | PASS |
| drink-history-explainer | PASS | PASS | PASS | PASS (7p) | PASS | PASS | PASS | PASS |
| dog-breed-explainer | PASS | PASS | PASS | PASS (7p) | PASS | PASS | PASS | PASS |
| cat-breed-explainer | PASS | PASS | PASS | PASS (6p) | PASS | PASS | PASS | PASS |
| gadget-explainer | PASS | PASS | PASS | PASS (11p) | PASS | PASS | PASS | PASS |
| what-if-map-cartoon | PASS | PASS | PASS | PASS (17p) | PASS | PASS | PASS | PASS |
| dwarf-planet-origin-map | PASS | PASS | PASS | PASS (8p) | PASS | PASS | PASS | PASS |
| cosmic-origin-map | PASS | PASS | PASS | PASS (8p) | PASS | PASS | PASS | PASS |
| unusual-jobs-explainer | PASS | PASS | PASS | PASS (15p)* | PASS | PASS | PASS | PASS |
| **SITE (R8)** | — | — | — | — | — | — | — | **PASS** |

\*unusual-jobs: layout text == live `#p-package` exactly; raw-mode “word” fragments like `his-` / `connec-` are PDF page-break hyphenation in `pdftotext` raw, not missing content. Non-ASCII (`° · – — ‘ ’ “ ” • … → ■`) survive.

### R8 site-level detail — PASS

- All 13 kit pages + 13 `/downloads/*.pdf` + home/kits/guides/builder/about/privacy/sitemap → **HTTP 200** live; PDFs `application/pdf`.
- Non-PDF kits labelled: **Site-written kit. No original Open Source Prompt PH PDF…** on jeepney / street-food / festival.
- `python3 tests/test_site.py` → 0 failures.
- Internal links checked by test suite (675).

### R9 mobile detail — PASS (after fix)

Before fix: kit pages `scrollWidth` 780 on 390/360 viewports; Copy/Download ~34px; package text 12px; `.btn` font shorthand with `inherit` dropped size to ~13.3px in Chromium.  
After fix (live): no horizontal page scroll; package header wraps; buttons ≥44px; `.pkgtext` scrolls inside box both ways; text ≥14px; screenshots reviewed (desktop + mobile package).

## Failures found initially → fixes

1. **R2 FAIL:** no visible OSP original title/filename on kit pages (only `download=` attr).  
   **Fix:** `site/pdfs/<slug>.title` + build.py `Original title:` / `Original: … (file)` lines; site-written label for 3 non-PDF kits.
2. **R9 FAIL:** horizontal overflow from wide `pre`/`article.prose` max-width 760; small tap targets; sub-14px UI; broken `font: … inherit` shorthands.  
   **Fix:** CSS containment (`min-width:0`, `minmax(0,1fr)`), mobile wrap + 44px buttons, font-size ≥14px, replace font shorthands; rebuild + push.

PDF **bytes/text were never altered**.

## OSP posts not covered on mjd (exact titles)

62 posts beyond the 10 mapped kits (including older Advance duplicates for Liquor/Dog/Cat with identical PDFs, plus many other series). Full list from live wp-json this run:

- Liquor History – Advance Prompt- Creator Kit- AI Prompt Framework.pdf *(older duplicate; same PDF bytes)*
- Dog Breed -Advance Prompt- Creator Kit- AI Prompt Framework.pdf *(older duplicate; same PDF bytes)*
- Cat Breed -Advance Prompt- Creator Kit-AI Prompt Framework.pdf *(older duplicate; same PDF bytes)*
- World Military Weapon (map paper cut animation)-v8 … through v1
- Virus & Diseases Creator Kit- AI Prompt Framework.pdf
- Tagalog Drama Episode Creator Kit- AI Prompt Framework.pdf
- Racing Engine Explainers-v2 / v1
- Plant Science Botany Explainers-v4 … v1
- Human Neuroanatomy-v1 / Human Neuroanatomy
- [Country]’s Trillion Dollar Secret “Paper Cut Animation-v1 … / -v1
- Everyday Origins Country-v2
- Elements & Metals -v2 / v1
- Logo Dark Story -v2 / v1
- Dog Breed-v2 / v1
- Coronary Stenting-v2 / v1
- Cat Breeds-v2 / v1
- Geopolitics vs Country Borders; Bird Nest Builder; Word of GOD; Genesis Creation Cinematic; Geopolitical and territorial dispute; Liquor Creator
- Anatomy & Biology; Human Anatomy-v3/v2/v1
- Geo Boundiries-v4 … v1
- Healthy Food-v3/v2/v1
- Historical Landmarks-v5 … v1
- Border Legend; Earth Mysteries Geological Facts
- Ammunition-v4 … v1

## Needs Johnny’s decision?

- **Duplicate Advance PDFs:** no content choice — Oct vs Nov uploads are byte-identical; newest posts already selected.
- **Uncovered OSP catalog (59+ distinct kits):** whether to import more onto mjd is a product decision; not a fidelity bug in the current 10.
- **Kit H1 branding vs OSP titles** (e.g. Drink vs Liquor, Unusual Jobs vs Dark Job, Dwarf Planet vs ERIS): left as-is with visible Original title lines per your rule (do not silently rename).

## Evidence notes

- Live PDF sha256 matched fresh OSP for all 10 after deploy.
- Copy all (local server) matched layout text for all 10.
- Screenshots under `/tmp/osp-audit/shots3/` (local) and `LIVE-390-pkg-drink.png` (live).

## Change 2026-11-05: real name + PDF-only landing + Niche ideas tab (commit 62d511f)

| Check | Result | Evidence |
|---|---|---|
| Name replaced everywhere ("Open Source Prompt PH") | PASS | SITE_NAME, header brand (logo kept, "(working name)" removed), titles, OG, JSON-LD, footer, about, privacy, 404, README, app.js/css/content comments, og images + cover previews regenerated, 3 site-written PDFs. `grep -rai "prompt kit ph\|working name" docs` = none; pdftotext of all PDFs = none. |
| Landing + /kits/ show only the 10 PDF kits | PASS | Home 6 latest PDF kits + "See all 10 kits"; /kits/ "10 kits shown", 10 cards, ItemList 10, chips from PDF kits only; PDF kit pager/related link only PDF kits; no niche URL on home or /kits/. |
| Niche ideas tab | PASS | Nav: Home, Kits, Niche ideas, Guides, Builder, About (header + footer). /niche-ideas/ lists 3 niche kits; their URLs unchanged, in sitemap, breadcrumb "Niche ideas", pager/related only within niche ideas. |
| Mobile OK (360/390) + desktop 1280 | PASS | scrollWidth = viewport, nav wraps to 2 rows, tap targets 44px; header non-sticky under 820px to save space. |
| PDFs untouched / package text | PASS | cmp site/pdfs vs docs/downloads and live: identical (10/10); #package text identical to previous build (10/10). |
| Tests | PASS | tests/test_site.py: 24 html files, 0 failures (new checks: counts, niche isolation, no old name). |
| Live | PASS | Pages build `built`; /, /kits/, /niche-ideas/, PDF kit, 3 niche kit URLs, PDF download all 200. |


## Change 2026-11-05: import of all remaining OSP PDF posts (commit 42b765d)

Source: `wp-json/wp/v2/posts` returned **72 posts** (page 2 = "invalid page number"; not 73). Every post links exactly **1 PDF**; no post has 0 or several. 13 posts map to the existing 10 kits (3 older Advance duplicates). **57 new kits** imported; 2 more posts skipped as byte-identical duplicates. No post has a featured image, so covers are generated cards (`previews.cover_card`), self-hosted. All 57 PDFs have extractable text (no scanned/no-text PDFs; fallback note implemented anyway).

### Duplicates by sha256 (listed once)
- `3d6c49ac…`: **Human Neuroanatomy-v1 Creator Kit- AI Prompt Framework.pdf** (post 357, used) == Human Neuroanatomy Creator Kit- AI Prompt Framework (post 203, skipped)
- `3482928d…`: **Geo Boundiries-v1 Creator Kit- AI Prompt Framework** (post 191, used) == Border Legend Creator Kit- AI Prompt Framework (post 164, skipped; different title, same PDF `Border-Legend.pdf` vs `Geo-Boundiries-1.pdf`)
- Existing: Liquor/Dog/Cat Advance (posts 458/455/452) == posts 490/487/484 (already on the site).

### Rubric for all 67 PDF kits (10 existing + 57 new)
| Check | Result | Evidence |
|---|---|---|
| R1 source (post -> exactly one PDF) | PASS | 72/72 posts have 1 PDF link; mapping in `site/osp_kits.json` / `site/osp_existing.json` |
| R2 original name | PASS | H1 = exact OSP title for new kits; "Original title" line + `download=` original filename on 67/67 |
| R3 byte-identical PDF | PASS | live sha256 == fresh OSP sha256 for 67/67 |
| R4 text/pages verbatim | PASS | `pdftotext -layout` of served PDF == Full package text for 57/57 new; existing 10 package text unchanged vs prior build |
| R5 Copy all + Download | PASS | Copy all button + Download PDF with original filename on 67/67 |
| R6 existing 10 unaltered | PASS | PDFs cmp-identical; package text identical (only pager/related neighbours changed) |
| R7 visual | PASS | screenshots 360/390/1280 of home, /kits/, niche, OSP kit, existing kit |
| R8 site (tests, sitemap, JSON-LD) | PASS | 81 HTML files, 0 failures; sitemap 80 URLs; ItemList 67; CreativeWork JSON-LD on new kits |
| R9 mobile 360/390 | PASS | scrollWidth == viewport on all pages; /kits/ shows 24 cards + "Show more kits" (24 per click); 12 category chips wrap, 44px; filter/search work |
| Live | PASS | Pages built 42b765d; 67 kit pages 200 and contain their PDF text; niche pages 200 |
| Size/build | PASS | docs/ 15 MB (downloads 6.1 MB, assets 6.0 MB); build ~3 s |

Notes: `<title>` for new kits uses the title minus " Creator Kit- AI Prompt Framework(.pdf)" to stay under 65 chars; H1 and Original title are exact. Home shows 6 latest by OSP post date (all Nov 3 existing kits). Full package box is a fixed-height scroll box (max 420px), max 26 KB text, no JS rendering cost.

### New kits (title -> slug -> PDF -> pages -> category -> post date)
| OSP title | Slug | PDF URL | Pages | Cat | Date |
|---|---|---|---|---|---|
| World Military Weapon (map paper cut animation)-v8 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-map-paper-cut-animation-v8` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-map-paper-cut-animation-v8.pdf | 4 | Military | 2026-10-29 |
| World Military Weapon-v7 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v7` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v7.pdf | 3 | Military | 2026-10-29 |
| World Military Weapon-v6 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v6` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v6.pdf | 3 | Military | 2026-10-29 |
| World Military Weapon-v5 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v5` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v5.pdf | 3 | Military | 2026-10-29 |
| World Military Weapon-v4 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v4` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v4.pdf | 4 | Military | 2026-10-29 |
| World Military Weapon-v3 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v3.pdf | 5 | Military | 2026-10-29 |
| World Military Weapon-v2 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v2.pdf | 4 | Military | 2026-10-29 |
| World Military Weapon-v1 Creator Kit- AI Prompt Framework.pdf | `world-military-weapon-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/World-Military-Weapon-v1.pdf | 4 | Military | 2026-10-29 |
| Virus & Diseases Creator Kit- AI Prompt Framework.pdf | `virus-and-diseases` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Virus-Diseases-Creator-Kit.pdf | 5 | Health | 2026-10-29 |
| Tagalog Drama Episode Creator Kit- AI Prompt Framework.pdf | `tagalog-drama-episode` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Tagalog-Drama-Episode.pdf | 4 | Philippines | 2026-10-27 |
| Racing Engine Explainers-v2 Creator Kit- AI Prompt Framework.pdf | `racing-engine-explainers-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Racing-Engine-Explainers-v2.pdf | 3 | Tech | 2026-10-27 |
| Racing Engine Explainers-v1 Creator Kit- AI Prompt Framework.pdf | `racing-engine-explainers-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Racing-Engine-Explainers-v1.pdf | 5 | Tech | 2026-10-27 |
| Plant Science Botany Explainers-v4 Creator Kit- AI Prompt Framework.pdf | `plant-science-botany-explainers-v4` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Plant-Science-Botany-Explainers-v4.pdf | 6 | Science | 2026-10-27 |
| Plant Science Botany Explainers-v3 Creator Kit- AI Prompt Framework.pdf | `plant-science-botany-explainers-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Plant-Science-Botany-Explainers-v3.pdf | 6 | Science | 2026-10-27 |
| Plant Science Botany Explainers-v2 Creator Kit- AI Prompt Framework.pdf | `plant-science-botany-explainers-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Plant-Science-Botany-Explainers-v2.pdf | 6 | Science | 2026-10-27 |
| Plant Science Botany Explainers-v1 Creator Kit- AI Prompt Framework.pdf | `plant-science-botany-explainers-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Plant-Science-Botany-Explainers-v1.pdf | 5 | Science | 2026-10-27 |
| Human Neuroanatomy-v1 Creator Kit- AI Prompt Framework.pdf | `human-neuroanatomy-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Human-Neuroanatomy-v1.pdf | 3 | Health | 2026-10-27 |
| [Country]’s Trillion Dollar Secret “Paper Cut Animation-v1 Creator Kit- AI Prompt Framework.pdf | `countrys-trillion-dollar-secret-paper-cut-animation-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Countrys-Trillion-Dollar-Secret-22Paper-Cut-Animation-v1-Creator-Kit-AI-Prompt-Framework.pdf | 4 | Maps | 2026-10-27 |
| [Country]’s Trillion Dollar Secret-v1 Creator Kit- AI Prompt Framework | `countrys-trillion-dollar-secret-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Countrys-Trillion-Dollar-Secret-v1.pdf | 4 | Maps | 2026-10-27 |
| Everyday  Origins Country-v2 Creator Kit- AI Prompt Framework | `everyday-origins-country-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Everyday-Origins-Country-v1.pdf | 4 | History | 2026-10-25 |
| Elements & Metals -v2 Creator Kit- AI Prompt Framework | `elements-and-metals-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Elements-Metals-v2.pdf | 4 | Science | 2026-10-25 |
| Elements & Metals -v1 Creator Kit- AI Prompt Framework | `elements-and-metals-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Elements-Metals-v1.pdf | 3 | Science | 2026-10-25 |
| Logo Dark Story -v2 Creator Kit- AI Prompt Framework | `logo-dark-story-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Logo-Dark-Story-2.pdf | 3 | Brands | 2026-10-25 |
| Logo Dark Story -v1 Creator Kit- AI Prompt Framework | `logo-dark-story-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Logo-Dark-Story-1.pdf | 4 | Brands | 2026-10-25 |
| Dog Breed-v2 Creator Kit- AI Prompt Framework | `dog-breed-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Dog-Breed-2.pdf | 3 | Animals | 2026-10-24 |
| Dog Breed-v1 Creator Kit- AI Prompt Framework | `dog-breed-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Dog-Breed-1.pdf | 3 | Animals | 2026-10-24 |
| Coronary Stenting-v2 Creator Kit- AI Prompt Framework | `coronary-stenting-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Coronary-Stenting-2.pdf | 3 | Health | 2026-10-23 |
| Coronary Stenting-v1 Creator Kit- AI Prompt Framework | `coronary-stenting-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Coronary-Stenting-1.pdf | 3 | Health | 2026-10-23 |
| Cat Breeds-v2 Creator Kit- AI Prompt Framework | `cat-breeds-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Best_Cat-Breeds_V2-2.pdf | 4 | Animals | 2026-10-23 |
| Cat Breeds-v1 Creator Kit- AI Prompt Framework | `cat-breeds-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Best_Cat-Breeds_V1.pdf | 3 | Animals | 2026-10-23 |
| Geopolitics vs Country Borders Creator Kit- AI Prompt Framework | `geopolitics-vs-country-borders` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geopolitics-vs-Country-Borders.pdf | 6 | Maps | 2026-10-23 |
| Bird Nest Builder Creator Kit- AI Prompt Framework | `bird-nest-builder` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Bird-Nest-Builder.pdf | 4 | Animals | 2026-10-23 |
| Word of GOD Creator Kit- AI Prompt Framework | `word-of-god` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Word-of-GOD-Kit.pdf | 3 | Faith | 2026-10-23 |
| Genesis Creation Cinematic Creator Kit- AI Prompt Framework | `genesis-creation-cinematic` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Genesis-Creation-Cinematic.pdf | 4 | Faith | 2026-10-23 |
| Geopolitical and territorial dispute Creator Kit- AI Prompt Framework | `geopolitical-and-territorial-dispute` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geopolitical-and-territorial-dispute-1.pdf | 8 | Maps | 2026-10-23 |
| Liquor Creator Creator Kit- AI Prompt Framework | `liquor-creator` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Liquor-Creator-Kit.pdf | 4 | History | 2026-10-23 |
| Anatomy & Biology Creator Kit- AI Prompt Framework | `anatomy-and-biology` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Anatomy-Biology-Creator-Kit.pdf | 3 | Health | 2026-10-23 |
| Human Anatomy-v3 Creator Kit- AI Prompt Framework | `human-anatomy-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Human-Anatomy-3.pdf | 4 | Health | 2026-10-23 |
| Human Anatomy-v2 Creator Kit- AI Prompt Framework | `human-anatomy-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Human-Anatomy-2.pdf | 4 | Health | 2026-10-23 |
| Human Anatomy-v1 Creator Kit- AI Prompt Framework | `human-anatomy-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Human-Anatomy-1.pdf | 4 | Health | 2026-10-23 |
| Geo Boundiries-v4 Creator Kit- AI Prompt Framework | `geo-boundiries-v4` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geo-Boundiries-4.pdf | 5 | Maps | 2026-10-23 |
| Geo Boundiries-v3 Creator Kit- AI Prompt Framework | `geo-boundiries-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geo-Boundiries-3.pdf | 5 | Maps | 2026-10-23 |
| Geo Boundiries-v2 Creator Kit- AI Prompt Framework | `geo-boundiries-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geo-Boundiries-2.pdf | 5 | Maps | 2026-10-23 |
| Geo Boundiries-v1 Creator Kit- AI Prompt Framework | `geo-boundiries-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Geo-Boundiries-1.pdf | 5 | Maps | 2026-10-23 |
| Healthy Food-v3 Creator Kit- AI Prompt Framework | `healthy-food-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Healthy-Food-3.pdf | 4 | Health | 2026-10-23 |
| Healthy Food-v2 Creator Kit- AI Prompt Framework | `healthy-food-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Healthy-Food-2.pdf | 5 | Health | 2026-10-23 |
| Healthy Food-v1 Creator Kit- AI Prompt Framework | `healthy-food-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Healthy-Food-1.pdf | 4 | Health | 2026-10-23 |
| Historical Landmarks-v5 Creator Kit- AI Prompt Framework | `historical-landmarks-v5` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Historical-Landmarks-5.pdf | 6 | History | 2026-10-23 |
| Historical Landmarks-v4 Creator Kit- AI Prompt Framework | `historical-landmarks-v4` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Historical-Landmarks-4.pdf | 7 | History | 2026-10-23 |
| Historical Landmarks-v3 Creator Kit- AI Prompt Framework | `historical-landmarks-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Historical-Landmarks-3.pdf | 5 | History | 2026-10-23 |
| Historical Landmarks-v2 Creator Kit- AI Prompt Framework | `historical-landmarks-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Historical-Landmarks-2.pdf | 5 | History | 2026-10-23 |
| Historical Landmarks-v1 Creator Kit- AI Prompt Framework | `historical-landmarks-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Historical-Landmarks-1.pdf | 5 | History | 2026-10-23 |
| Earth Mysteries Geological Facts Creator Kit- AI Prompt Framework | `earth-mysteries-geological-facts` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Earth-Mysteries-Geological-Facts.pdf | 7 | Science | 2026-10-23 |
| Ammunition-v4  Creator Kit- AI Prompt Framework | `ammunition-v4` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Ammunition-4.pdf | 3 | Military | 2026-10-23 |
| Ammunition-v3  Creator Kit- AI Prompt Framework | `ammunition-v3` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Ammunition-3-1.pdf | 4 | Military | 2026-10-23 |
| Ammunition-v2  Creator Kit- AI Prompt Framework | `ammunition-v2` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Ammunition-2.pdf | 3 | Military | 2026-10-23 |
| Ammunition-v1  Creator Kit- AI Prompt Framework | `ammunition-v1` | https://opensourcepromptph.com/wp-content/uploads/2026/10/Ammunition-1-1.pdf | 6 | Military | 2026-10-23 |

## Change 2026-11-05: replicate the original site structure (commit 0946268)

Full inventory and gap list: `ORIGINAL_SITE_AUDIT.md`. Checkers: `tests/linkcheck.py` (internal links) and `tests/textdiff.py` (original vs mjd visible text).

| Check | Result | Evidence |
|---|---|---|
| Every original menu item present, same label/order, working link | PASS | 7/7 header + 7/7 footer (Premium niche, Video editing guide, Instructions, Explore prompts, Prompt workshop, Search via google, Facebook community); Niche ideas tab appended; anchors #guides/#workshop exist |
| Every original page has an mjd page with the same text | PASS | 92 original pages (home, /page/2-8/, 2 WP pages, 4 categories + 6 extra category pages, 72 posts): 2655 text lines, 0 missing except 4 lines of visitor comments (intentionally not copied) |
| Internal links resolve | PASS | 6654 internal links/srcs in docs/, 0 broken; live sitemap 172 URLs all 200; unknown URL returns 404 page |
| All 67 kits still pass | PASS | live sha256 == recorded OSP sha256 67/67; Full package text unchanged vs previous build 67/67; Copy all + Download present; tests 0 failures |
| Self-hosted media, no hotlinking | PASS | 5 carousel images, 1 page image, 4 MP4s, 4 .txt attachments (byte-identical) under /assets/osp/ and /files/ |
| Mobile 360/390 every new page type | PASS | no horizontal scroll at 360/390/1280/1366/1440 on home, page/N, category, search, WP pages, post, kits, kit, niche, guides, builder, about, 404; Menu button (8 items, 44px) below 1366px |
| Tests | PASS | tests/test_site.py: 173 HTML files, 0 failures |
| Live | PASS | Pages built 0946268; WebFetch of home and Instructions page shows replicated text |

Not replicated: comment threads/forms, GTM/AdSense/Site Kit sign-in/Ko-fi widget scripts, author/date archives, feeds, attachment pages, wp-admin. docs/ is 102 MB (videos 88 MB).
