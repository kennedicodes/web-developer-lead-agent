# Lead Generation Agent — Project Overview

## What This Is

An automated Python agent that finds local businesses **without a website** across the **East Coast and Midwest** and adds them to a Google Sheet lead list. Each run adds up to **50 new leads** and never adds a business already in the sheet.

Businesses come from the **Google Places API** (Google Maps listings). Each result says whether the business has a website, so finding and checking businesses happen in one step. A run takes about a minute.

---

## Target Markets

### East Coast
Naples FL, Boca Raton FL, Coral Gables FL, Bethesda MD, McLean VA, Greenwich CT, Charlotte NC, Raleigh NC, Atlanta GA, Princeton NJ, Westchester NY

### Midwest / South
Highland Park TX, Southlake TX, The Woodlands TX, Austin TX, Nashville TN, Franklin TN, Naperville IL, Winnetka IL, Lake Forest IL, Edina MN, Leawood KS

---

## Target Industries

Any business type works. `config.py` focuses on local services where businesses often have no website: home services (plumbers, electricians, HVAC, roofers, handymen, painters, locksmiths…), landscaping, cleaning, automotive, barbers/salons, tailors, movers, pet grooming, daycare, tutoring, and food. To change targets, edit `INDUSTRIES` or `CITIES`. Saved progress resets automatically when the search list changes.

---

## Files

| File | Purpose |
|------|---------|
| `config.py` | Sheet ID, industry keywords, cities, monthly API call limit, sites that don't count as a website |
| `places.py` | Google Places API search: up to 20 businesses per call with name, phone, website, city/state and open/closed status. Tracks monthly API usage |
| `sheet.py` | Google Sheets connection, reading existing leads, name/phone normalization, dedupe, writing rows |
| `progress.py` | Saves which search to resume from (`search_progress.json`) |
| `run_log.py` | Saves each run's output and any crash to `run_log.txt` |
| `main.py` | Runs the pipeline |

---

## Sheet Layout

The tab has a title and live metrics above the table. The agent finds the **"Business Name"** header row, reads every lead below it, and writes new leads into the next empty row.

| A | B | C | D | E+ |
|---|---|---|---|---|
| Business name | Phone | Email (left blank; Google doesn't provide emails) | City, State | left blank (filled manually) |

---

## Pipeline

1. Load every existing lead from the sheet and confirm the agent can edit it.
2. Work through each "keyword in city" search (e.g. "plumber in Naples, FL"), resuming where the last run stopped. Each search returns up to 3 pages of 20 businesses.
3. For each business:
   - **Has a website?** Skip it. A Facebook, Yelp or booking page doesn't count as a website, so those businesses are still leads.
   - **Permanently or temporarily closed?** Skip it.
   - **No phone number?** Skip it.
   - **Already in the sheet?** Skip it.
   - Otherwise, add it.
4. Stop after 50 leads, or after every search has been run once.

---

## Deduplication Strategy

Older rows are inconsistent: column A may contain just the name, "Name Phone", or "Name • Phone". To handle this, the agent builds two lookup sets:

- **Phones:** digits from column B, plus any phone number found inside column A. These are normalized to the last 10 digits.
- **Names:** column A with any phone number, bullets, punctuation and suffixes (LLC, Inc, Co, The…) stripped, then lowercased.

A business counts as a duplicate if either its phone or its normalized name matches. Leads added during a run go into the same sets, so a run can't add the same business twice.

---

## How to Run

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install gspread google-auth
python main.py
```

Requires:
- `creds.json` (Google service account key) in the project root, with the sheet shared (**Editor**) with the service account's email.
- A Google Places API key, either in the `GOOGLE_PLACES_API_KEY` environment variable or in `places_api_key.txt`. Create it in Google Cloud Console: enable **Places API (New)**, turn on billing, and restrict the key to that API.

**Costs:**
- The Google Sheets API is free.
- A 50-lead run uses roughly 20–25 Places API calls. Each call returns up to 20 businesses, and about 2–3 per call have no website.
- Google includes 1,000 calls a month free (about 40 runs). After that, it charges about $35 per 1,000 calls (about $0.80 per run).
- `MAX_PLACES_CALLS_PER_MONTH` in `config.py` (default 1,000) stops the agent at the free limit. Raise it only if you're willing to pay.
