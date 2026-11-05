# Open Source Prompt PH
Static site. Source in `site/` (content.py, css, js), built to `docs/` by `build.py`. Set `BASE_URL` in build.py before deploying.
Rebuild: `python3 build.py`  Test: `python3 tests/test_site.py`
Preview: `python3 -m http.server 8842 --bind 127.0.0.1 -d docs` then open http://127.0.0.1:8842/
Browser QA (axe, screenshots to shots/): `python3 tests/qa_browser.py http://127.0.0.1:8842/`
Internal links are root-relative, so serve docs/ at a domain root.
