# Original site audit: opensourcepromptph.com (crawled 2026-11-05)

Sources: rendered HTML of every page below + `wp-json/wp/v2/{posts,pages,categories,tags,media,users,navigation}`. Menus are not exposed by the REST API (`menu-items` returns 401), so menus were read from the rendered header/footer HTML.

## Menus

Header (`Main navigation`) and footer (`Footer navigation`) carry the same 7 items, no submenus:

| # | Label | Original target | mjd target |
|---|---|---|---|
| 1 | Premium niche | https://ko-fi.com/opensourcepromptphpremium/shop | same (external) |
| 2 | Video editing guide | /50-chatgpt-video-editing-prompts-for-creators/ | /50-chatgpt-video-editing-prompts-for-creators/ |
| 3 | Instructions | /how-to-use-this-2-step-ai-automation-prompt/ | /how-to-use-this-2-step-ai-automation-prompt/ |
| 4 | Explore prompts | /#guides | /#guides |
| 5 | Prompt workshop | /#workshop | /#workshop |
| 6 | Search via google | https://www.google.com/search?q=site:+https://opensourcepromptph.com | https://www.google.com/search?q=site:+https://mjd.johnnybodegas.com (rewritten to this domain) |
| 7 | Facebook community | https://www.facebook.com/groups/890192480414598 | same (external) |

mjd adds one header tab after these: **Niche ideas** (/niche-ideas/). Footer adds a second row: Kits library, Niche ideas, Guides, Builder, About, Privacy.

Brand: `>_ OpenSource Prompt PH` + `THE CREATOR’S FIELD GUIDE` (mjd keeps the name Open Source Prompt PH). Footer: brand link `Free AI Prompts & Creator Kits | Open Source Prompt PH`, menu, `© 2026 Free AI Prompts & Creator Kits | Open Source Prompt PH · Practical ideas, thoughtfully explained.` No sidebar/widgets. No social links other than the Facebook group and Ko-fi.

## Homepage sections (in order)

1. Featured carousel: 5 slides (Earth Mysteries, Racing Engine Explainers, Historical Landmarks, Plant Science & Botany, Tagalog Drama Episodes), Pause/←/→, `01 / 05`, note line.
2. Hero: kicker `A little direction. A better creation.`, H1 `Better prompts. More possibilities.`, intro, 2 buttons, note, Prompt notebook card.
3. Principles row (01–04).
4. `#guides` The creator’s reading room: search form, 4 category links, 10 latest post cards (category, title, Read article ↗, Partee88, date), pagination 1 2 … 8 Next.
5. `#workshop` The prompt workshop: 3 steps + builder (topic, format select, editable prompt, Copy prompt ↗).

## Inventory

| URL | Title | Type | Menu position | mjd |
|---|---|---|---|---|
| / | Free AI Prompts & Creator Kits | Open Source Prompt PH | home | brand | replicated |
| /page/2/ … /page/8/ | home, page N | post list | pagination | replicated |
| /50-chatgpt-video-editing-prompts-for-creators/ | 50 ChatGPT Video Editing Prompts for Creators | WP page | 2 Video editing guide | replicated (image + 4 videos self-hosted) |
| /how-to-use-this-2-step-ai-automation-prompt/ | From Free Prompt to Finished Video | WP page | 3 Instructions | replicated (image + 4 videos self-hosted) |
| /category/advance-premium-free/ | Category: Advance Premium Free (1 posts, 1 pages) | category | home filter chip | replicated |
| /category/advance-prompt/ | Category: Advance Prompt (5 posts, 1 pages) | category | home filter chip | replicated |
| /category/premium-free/ | Category: Premium Free (3 posts, 1 pages) | category | home filter chip | replicated |
| /category/uncategorized/ | Category: Uncategorized (63 posts, 7 pages) | category | home filter chip | replicated |
| /?s=… | Search Results for “…” | search | home search form | replicated as /search/?s=… (client-side, title match) |
| /404 | 404 — Page not found | 404 | — | replicated text |
| /author/partee88/ | author archive | WP mechanics | post meta link | skipped (author name shown as text) |
| /2026/10/ etc., /feed/, /comments/feed/, /wp-admin/, /wp-login.php, /wp-json/, attachment pages (99 media items), /navigation/ (wp_navigation post) | WordPress mechanics | — | — | skipped |
| /science-legend-advance-prompt-creator-kit-ai-prompt-framework-pdf/ | Science legend-Advance Prompt Creator Kit-AI Prompt Framework.pdf | post (Advance Prompt) | home/category list | replicated -> PDF /downloads/science-legend-explainer.pdf, kit page /kits/science-legend-explainer/ |
| /logo-history-advance-prompt-creator-kit-ai-prompt-framework-pdf/ | Logo History -Advance Prompt Creator Kit-AI Prompt Framework.pdf | post (Advance Prompt) | home/category list | replicated -> PDF /downloads/logo-history-explainer.pdf, kit page /kits/logo-history-explainer/ |
| /liquor-history-advance-prompt-creator-kit-ai-prompt-framework-pdf-2/ | Liquor History -Advance Prompt Creator Kit-AI Prompt Framework.pdf | post (Advance Prompt) | home/category list | replicated -> PDF /downloads/drink-history-explainer.pdf, kit page /kits/drink-history-explainer/ |
| /dog-breed-advance-prompt-creator-kit-ai-prompt-framework-pdf-2/ | Dog Breed -Advance Prompt Creator Kit-AI Prompt Framework.pdf | post (Advance Prompt) | home/category list | replicated -> PDF /downloads/dog-breed-explainer.pdf, kit page /kits/dog-breed-explainer/ |
| /cat-breed-advance-prompt-creator-kit-ai-prompt-framework-pdf-2/ | Cat Breed-Advance Prompt Creator Kit-AI Prompt Framework.pdf | post (Advance Prompt) | home/category list | replicated -> PDF /downloads/cat-breed-explainer.pdf, kit page /kits/cat-breed-explainer/ |
| /2d_zackstyle-gadget-explainer-creator-kit-ai-prompt-framework-pdf/ | 2D_ZackStyle Gadget Explainer Creator Kit- AI Prompt Framework.pdf | post (Premium Free) | home/category list | replicated -> PDF /downloads/gadget-explainer.pdf, kit page /kits/gadget-explainer/ + Topics_1000.txt |
| /whatif-map-cartoon-explainer-creator-kit-ai-prompt-framework-pdf/ | WHATIF MAP CARTOON EXPLAINER Creator Kit- AI Prompt Framework.pdf | post (Premium Free) | home/category list | replicated -> PDF /downloads/what-if-map-cartoon.pdf, kit page /kits/what-if-map-cartoon/ + 1000_TOPICS_WHATIF_MAP.txt |
| /eris-origin-map-explainer-creator-kit-ai-prompt-framework-pdf/ | ERIS ORIGIN MAP EXPLAINER Creator Kit- AI Prompt Framework.pdf | post (Advance Premium Free) | home/category list | replicated -> PDF /downloads/dwarf-planet-origin-map.pdf, kit page /kits/dwarf-planet-origin-map/ + 1000_Astronomical_Names.txt |
| /cosmic-origin-map-explainer-creator-kit-ai-prompt-framework-pdf/ | COSMIC ORIGIN MAP EXPLAINER Creator Kit- AI Prompt Framework.pdf | post (Premium Free) | home/category list | replicated -> PDF /downloads/cosmic-origin-map.pdf, kit page /kits/cosmic-origin-map/ + 1000_Astronomical_Names.txt |
| /dark-job-creator-kit-ai-prompt-framework-pdf/ | Dark Job Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/unusual-jobs-explainer.pdf, kit page /kits/unusual-jobs-explainer/ |
| /liquor-history-advance-prompt-creator-kit-ai-prompt-framework-pdf/ | Liquor History – Advance Prompt- Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/drink-history-explainer.pdf, kit page /kits/drink-history-explainer/ |
| /dog-breed-advance-prompt-creator-kit-ai-prompt-framework-pdf/ | Dog Breed -Advance Prompt- Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/dog-breed-explainer.pdf, kit page /kits/dog-breed-explainer/ |
| /cat-breed-advance-prompt-creator-kit-ai-prompt-framework-pdf/ | Cat Breed -Advance Prompt- Creator Kit-AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/cat-breed-explainer.pdf, kit page /kits/cat-breed-explainer/ |
| /world-military-weapon-map-paper-cut-animation-v8-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon (map paper cut animation)-v8 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-map-paper-cut-animation-v8.pdf, kit page /kits/world-military-weapon-map-paper-cut-animation-v8/ |
| /world-military-weapon-v7-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v7 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v7.pdf, kit page /kits/world-military-weapon-v7/ |
| /world-military-weapon-v6-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v6 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v6.pdf, kit page /kits/world-military-weapon-v6/ |
| /world-military-weapon-v5-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v5 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v5.pdf, kit page /kits/world-military-weapon-v5/ |
| /world-military-weapon-v4-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v4 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v4.pdf, kit page /kits/world-military-weapon-v4/ |
| /world-military-weapon-v3-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v3 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v3.pdf, kit page /kits/world-military-weapon-v3/ |
| /world-military-weapon-v2-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v2 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v2.pdf, kit page /kits/world-military-weapon-v2/ |
| /world-military-weapon-v1-creator-kit-ai-prompt-framework-pdf/ | World Military Weapon-v1 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/world-military-weapon-v1.pdf, kit page /kits/world-military-weapon-v1/ |
| /virus-diseases-creator-kit-ai-prompt-framework-pdf/ | Virus & Diseases Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/virus-and-diseases.pdf, kit page /kits/virus-and-diseases/ |
| /tagalog-drama-episode-creator-kit-ai-prompt-framework-pdf/ | Tagalog Drama Episode Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/tagalog-drama-episode.pdf, kit page /kits/tagalog-drama-episode/ |
| /racing-engine-explainers-v2-creator-kit-ai-prompt-framework-pdf/ | Racing Engine Explainers-v2 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/racing-engine-explainers-v2.pdf, kit page /kits/racing-engine-explainers-v2/ |
| /racing-engine-explainers-v1-creator-kit-ai-prompt-framework-pdf/ | Racing Engine Explainers-v1 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/racing-engine-explainers-v1.pdf, kit page /kits/racing-engine-explainers-v1/ |
| /plant-science-botany-explainers-v4-creator-kit-ai-prompt-framework-pdf/ | Plant Science Botany Explainers-v4 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/plant-science-botany-explainers-v4.pdf, kit page /kits/plant-science-botany-explainers-v4/ |
| /plant-science-botany-explainers-v3-creator-kit-ai-prompt-framework-pdf/ | Plant Science Botany Explainers-v3 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/plant-science-botany-explainers-v3.pdf, kit page /kits/plant-science-botany-explainers-v3/ |
| /plant-science-botany-explainers-v2-creator-kit-ai-prompt-framework-pdf/ | Plant Science Botany Explainers-v2 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/plant-science-botany-explainers-v2.pdf, kit page /kits/plant-science-botany-explainers-v2/ |
| /plant-science-botany-explainers-v1-creator-kit-ai-prompt-framework-pdf/ | Plant Science Botany Explainers-v1 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/plant-science-botany-explainers-v1.pdf, kit page /kits/plant-science-botany-explainers-v1/ |
| /human-neuroanatomy-v1-creator-kit-ai-prompt-framework-pdf/ | Human Neuroanatomy-v1 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/human-neuroanatomy-v1.pdf, kit page /kits/human-neuroanatomy-v1/ |
| /countrys-trillion-dollar-secret-paper-cut-animation-v1-creator-kit-ai-prompt-framework-pdf/ | [Country]’s Trillion Dollar Secret “Paper Cut Animation-v1 Creator Kit- AI Prompt Framework.pdf | post (Uncategorized) | home/category list | replicated -> PDF /downloads/countrys-trillion-dollar-secret-paper-cut-animation-v1.pdf, kit page /kits/countrys-trillion-dollar-secret-paper-cut-animation-v1/ |
| /countrys-trillion-dollar-secret-v1-creator-kit-ai-prompt-framework/ | [Country]’s Trillion Dollar Secret-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/countrys-trillion-dollar-secret-v1.pdf, kit page /kits/countrys-trillion-dollar-secret-v1/ |
| /everyday-origins-country-v2-creator-kit-ai-prompt-framework/ | Everyday  Origins Country-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/everyday-origins-country-v2.pdf, kit page /kits/everyday-origins-country-v2/ |
| /elements-metals-v2-creator-kit-ai-prompt-framework/ | Elements & Metals -v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/elements-and-metals-v2.pdf, kit page /kits/elements-and-metals-v2/ |
| /elements-metals-v1-creator-kit-ai-prompt-framework/ | Elements & Metals -v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/elements-and-metals-v1.pdf, kit page /kits/elements-and-metals-v1/ |
| /logo-dark-story-v2-creator-kit-ai-prompt-framework/ | Logo Dark Story -v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/logo-dark-story-v2.pdf, kit page /kits/logo-dark-story-v2/ |
| /logo-dark-story-v1-creator-kit-ai-prompt-framework/ | Logo Dark Story -v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/logo-dark-story-v1.pdf, kit page /kits/logo-dark-story-v1/ |
| /dog-breed-v2-creator-kit-ai-prompt-framework/ | Dog Breed-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/dog-breed-v2.pdf, kit page /kits/dog-breed-v2/ |
| /dog-breed-1-creator-kit-ai-prompt-framework/ | Dog Breed-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/dog-breed-v1.pdf, kit page /kits/dog-breed-v1/ |
| /coronary-stenting-2-creator-kit-ai-prompt-framework/ | Coronary Stenting-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/coronary-stenting-v2.pdf, kit page /kits/coronary-stenting-v2/ |
| /coronary-stenting-1-creator-kit-ai-prompt-framework/ | Coronary Stenting-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/coronary-stenting-v1.pdf, kit page /kits/coronary-stenting-v1/ |
| /cat-breeds-2-kit-ai-prompt-framework/ | Cat Breeds-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/cat-breeds-v2.pdf, kit page /kits/cat-breeds-v2/ |
| /cat-breeds-1-kit-ai-prompt-framework/ | Cat Breeds-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/cat-breeds-v1.pdf, kit page /kits/cat-breeds-v1/ |
| /geopolitics-vs-country-borders-kit-ai-prompt-framework/ | Geopolitics vs Country Borders Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geopolitics-vs-country-borders.pdf, kit page /kits/geopolitics-vs-country-borders/ |
| /bird-nest-builder-kit-ai-prompt-framework/ | Bird Nest Builder Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/bird-nest-builder.pdf, kit page /kits/bird-nest-builder/ |
| /word-of-god-kit-ai-prompt-framework/ | Word of GOD Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/word-of-god.pdf, kit page /kits/word-of-god/ |
| /genesis-creation-cinematic-kit-ai-prompt-framework/ | Genesis Creation Cinematic Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/genesis-creation-cinematic.pdf, kit page /kits/genesis-creation-cinematic/ |
| /geopolitical-and-territorial-dispute-kit-ai-prompt-framework/ | Geopolitical and territorial dispute Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geopolitical-and-territorial-dispute.pdf, kit page /kits/geopolitical-and-territorial-dispute/ |
| /liquor-creator-kit-ai-prompt-framework/ | Liquor Creator Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/liquor-creator.pdf, kit page /kits/liquor-creator/ |
| /anatomy-biology-creator-kit-ai-prompt-framework/ | Anatomy & Biology Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/anatomy-and-biology.pdf, kit page /kits/anatomy-and-biology/ |
| /human-anatomy-3-creator-kit-ai-prompt-framework/ | Human Anatomy-v3 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/human-anatomy-v3.pdf, kit page /kits/human-anatomy-v3/ |
| /human-anatomy-2-creator-kit-ai-prompt-framework/ | Human Anatomy-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/human-anatomy-v2.pdf, kit page /kits/human-anatomy-v2/ |
| /human-anatomy-1-creator-kit-ai-prompt-framework/ | Human Anatomy-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/human-anatomy-v1.pdf, kit page /kits/human-anatomy-v1/ |
| /human-neuroanatomy-creator-kit-ai-prompt-framework/ | Human Neuroanatomy Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/human-neuroanatomy-v1.pdf, kit page /kits/human-neuroanatomy-v1/ |
| /geo-boundiries-4-creator-kit-ai-prompt-framework/ | Geo Boundiries-v4 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geo-boundiries-v4.pdf, kit page /kits/geo-boundiries-v4/ |
| /geo-boundiries-3-creator-kit-ai-prompt-framework/ | Geo Boundiries-v3 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geo-boundiries-v3.pdf, kit page /kits/geo-boundiries-v3/ |
| /geo-boundiries-2-creator-kit-ai-prompt-framework/ | Geo Boundiries-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geo-boundiries-v2.pdf, kit page /kits/geo-boundiries-v2/ |
| /geo-boundiries-1-creator-kit-ai-prompt-framework/ | Geo Boundiries-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geo-boundiries-v1.pdf, kit page /kits/geo-boundiries-v1/ |
| /healthy-food-3-creator-kit-ai-prompt-framework/ | Healthy Food-v3 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/healthy-food-v3.pdf, kit page /kits/healthy-food-v3/ |
| /healthy-food-2-creator-kit-ai-prompt-framework/ | Healthy Food-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/healthy-food-v2.pdf, kit page /kits/healthy-food-v2/ |
| /healthy-food-1-creator-kit-ai-prompt-framework/ | Healthy Food-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/healthy-food-v1.pdf, kit page /kits/healthy-food-v1/ |
| /historical-landmarks-5-creator-kit-ai-prompt-framework/ | Historical Landmarks-v5 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/historical-landmarks-v5.pdf, kit page /kits/historical-landmarks-v5/ |
| /historical-landmarks-4-creator-kit-ai-prompt-framework/ | Historical Landmarks-v4 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/historical-landmarks-v4.pdf, kit page /kits/historical-landmarks-v4/ |
| /historical-landmarks-3-creator-kit-ai-prompt-framework/ | Historical Landmarks-v3 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/historical-landmarks-v3.pdf, kit page /kits/historical-landmarks-v3/ |
| /historical-landmarks-2-creator-kit-ai-prompt-framework/ | Historical Landmarks-v2 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/historical-landmarks-v2.pdf, kit page /kits/historical-landmarks-v2/ |
| /historical-landmarks-1-creator-kit-ai-prompt-framework/ | Historical Landmarks-v1 Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/historical-landmarks-v1.pdf, kit page /kits/historical-landmarks-v1/ |
| /border-legend-creator-kit-ai-prompt-framework/ | Border Legend Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/geo-boundiries-v1.pdf, kit page /kits/geo-boundiries-v1/ |
| /earth-mysteries-geological-facts-creator-kit-ai-prompt-framework/ | Earth Mysteries Geological Facts Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/earth-mysteries-geological-facts.pdf, kit page /kits/earth-mysteries-geological-facts/ |
| /ammunition_4-creator-kit-ai-prompt-framework/ | Ammunition-v4  Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/ammunition-v4.pdf, kit page /kits/ammunition-v4/ |
| /ammunition_3-creator-kit-ai-prompt-framework/ | Ammunition-v3  Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/ammunition-v3.pdf, kit page /kits/ammunition-v3/ |
| /ammunition_2-creator-kit-ai-prompt-framework/ | Ammunition-v2  Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/ammunition-v2.pdf, kit page /kits/ammunition-v2/ |
| /ammunition_1-creator-kit-ai-prompt-framework/ | Ammunition-v1  Creator Kit- AI Prompt Framework | post (Uncategorized) | home/category list | replicated -> PDF /downloads/ammunition-v1.pdf, kit page /kits/ammunition-v1/ |

## Gap list vs mjd before this change (all closed unless noted)

- Header/footer menus differed (mjd had Home/Kits/Niche ideas/Guides/Builder/About) -> now the 7 original items in order + Niche ideas.
- Homepage structure/wording differed -> now carousel, hero, notebook, principles, reading room with 10 latest posts + pagination, workshop builder (same prompt template).
- 2 WP pages missing -> added with same text; image and 4 MP4 videos self-hosted (88 MB).
- 4 category archives + pagination missing -> added (/category/<slug>/, /category/uncategorized/page/2-7/).
- 72 post URLs missing -> each original post slug now has an mjd page with the same title, meta line, file block(s) and Download, plus post navigation and a link to the kit page.
- 4 .txt attachments (Topics_1000, 1000_TOPICS_WHATIF_MAP, 1000_Astronomical_Names x2) missing -> self-hosted byte-identical under /files/ and linked from the posts and the matching kit pages.
- Search -> /search/?s= (static, client-side).
- 404 wording -> replicated.

## Not replicated (by design)

- Comments: the WhatIf post has 2 visitor comments and every post has a comment form (posts to wp-comments-post.php). Not copied (user data); static site shows `Comments are not available on this copy of the site.`
- Third-party scripts: Google Tag Manager/Analytics, AdSense, Google Site Kit sign-in, Ko-fi floating widget, WP emoji. Not loaded (no-tracking policy). The Ko-fi link stays in the menu.
- Author archive, date archives, feeds, attachment pages, wp-admin/login: WordPress mechanics.
- Visual theme (lime-on-dark editorial theme) is not cloned pixel-for-pixel; structure and text are replicated in the mjd palette.
