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
