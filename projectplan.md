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
- [x] Expand `CITIES` to 109 cities (3,270 searches) so 300 leads/day doesn't run out of new businesses
- [x] Replace `CITIES` with 187 high-net-worth cities nationwide, West Coast first (5,610 searches)
- [x] Add `LEADS_PER_RUN = 300` and a `MAX_LEADS_PER_DAY = 300` daily cap
- [x] Switch the data source from Google Places to Serper.dev (`serper.py`): paged search with up to 10 pages per search, monthly credit cap (live test added 5 leads for 12 credits)
- [x] Update `PROJECT_OVERVIEW.md` for Serper setup and costs
- [x] Verify dedupe normalization offline
- [x] Verify live run against the sheet (3-lead test run added rows 99–101 correctly)
