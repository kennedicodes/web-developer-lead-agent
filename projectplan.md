# Project Plan — No-Website Lead Generation Agent

Goal: find local businesses with **no website** and add them to the lead sheet
(`1pmrDIdcl15OYWrnK_srha1UlzLu4EkgnlMUB2sA_F0w`) without duplicating existing leads.

Sheet columns: A = Business name, B = Phone, C = Email, D = City/State (E+ left blank).

## Tasks
- [x] Point `config.py` at the new sheet and broaden industries
- [x] Add `sheet.py` (connect, read existing leads, normalize name/phone, dedupe, write A–D)
- [x] Rewrite `main.py` pipeline: skip businesses with websites, dedupe against sheet, 50 leads per run across searches
- [x] Reset progress automatically when the search list changes (`progress.py`)
- [x] Remove chatbot/website-crawl code (`detector.py`, `extractor.py`, `logger.py`)
- [x] Find the "Business Name" header row (title/metrics rows above the table) and write to the next empty row
- [x] Fail fast if the service account can't edit the sheet
- [x] Save each run's output and any crash to `run_log.txt`
- [x] Replace Yellow Pages scraping (rate-limited) with Google Places API search (`places.py`), with a monthly call cap
- [x] Update `PROJECT_OVERVIEW.md`
- [x] Verify dedupe normalization offline
- [x] Verify live run against the sheet (3-lead test run added rows 99–101 correctly)
