# Lead Generation Agent — Project Overview

## What This Is

An automated Python agent that finds local businesses **without a website** in **high-net-worth cities across the US** and adds them to a Google Sheet lead list. One run adds up to **300 new leads**, never adds a business already in the sheet, and never adds more than 300 in a day.

Businesses come from **Google Maps search results via [Serper.dev](https://serper.dev)**. Serper is a low-cost third-party service that runs the search on Google Maps and returns each business's name, phone, address and website. Finding businesses and checking for a website happen in the same call.

---

## Target Markets

187 high-net-worth cities and suburbs in 36 states, listed in `CITIES` in `config.py`. West Coast cities come first:
- **California:** Atherton, Palo Alto, Beverly Hills, Malibu, Newport Beach, La Jolla…
- **Pacific Northwest:** Bellevue, Medina, Mercer Island, Lake Oswego…
- **Mountain West / Southwest:** Scottsdale, Boulder, Aspen, Park City…
- **Texas:** Highland Park, Southlake, The Woodlands…
- **Midwest:** Winnetka, Hinsdale, Edina, Bloomfield Hills…
- **South and Florida:** Brentwood TN, Buckhead, Naples, Palm Beach…
- **Mid-Atlantic:** Bethesda, McLean…
- **Northeast:** Greenwich, Scarsdale, Short Hills, Wellesley…

## Target Industries

30 local-service keywords where businesses often have no website:
- **Home services:** plumbers, electricians, HVAC, roofers, handymen, painters, locksmiths…
- **Outdoor:** landscaping, lawn care, tree service
- **Cleaning:** house cleaning, carpet cleaning, dry cleaners
- **Automotive:** auto repair, auto body, towing
- **Personal care:** barbers, nail salons, hair salons, beauty supply
- **Other services:** tailors, movers, pet grooming, daycare, tutoring
- **Food:** restaurants, food trucks, bakeries

30 keywords × 187 cities gives **5,610 searches**, roughly 20,000+ leads before searches start repeating.

To change targets, edit `INDUSTRIES` or `CITIES`. Saved progress resets automatically when the search list changes.

---

## Files

| File | Purpose |
|------|---------|
| `config.py` | Sheet ID, industries, cities, leads per run/day, Serper credit limit, pages per search, sites that don't count as a website |
| `serper.py` | Serper.dev Google Maps search: 20 businesses per page with name, phone, website and city/state. Tracks monthly credit usage |
| `sheet.py` | Google Sheets connection, reading existing leads, name/phone normalization, dedupe, writing rows |
| `progress.py` | Saves which search to resume from (`search_progress.json`) and counts leads added today (`daily_leads.json`) |
| `run_log.py` | Saves each run's output and any crash to `run_log.txt` |
| `main.py` | Runs the pipeline |

---

## Sheet Layout

The tab has a title and live metrics above the table. The agent finds the **"Business Name"** header row, reads every lead below it, and writes new leads into the next empty row.

| A | B | C | D | E+ |
|---|---|---|---|---|
| Business name | Phone | Email (left blank; Google Maps doesn't list emails) | City, State | left blank (filled manually) |

---

## Pipeline

1. Load every existing lead from the sheet and confirm the agent can edit it.
2. Work through each "keyword in city" search (e.g. "plumber in Naples, FL"), resuming where the last run stopped.
3. For each search, read result pages of 20 businesses each. Stop paging when a page brings nothing new, or after 10 pages. Deeper pages tend to have more businesses without websites.
4. For each business:
   - **Has a website?** Skip it. A Facebook, Yelp or booking page doesn't count as a website, so those businesses are still leads.
   - **No phone number?** Skip it.
   - **Already in the sheet?** Skip it.
   - Otherwise, add it.
5. Stop at 300 leads for the run, or for the day.

---

## Deduplication Strategy

Older rows are inconsistent: column A may contain just the name, "Name Phone", or "Name • Phone". To handle this, the agent builds two lookup sets:

- **Phones:** digits from column B, plus any phone number found inside column A. These are normalized to the last 10 digits.
- **Names:** column A with any phone number, bullets, punctuation and suffixes (LLC, Inc, Co, The…) stripped, then lowercased.

A business counts as a duplicate if either its phone or its normalized name matches. Leads added during a run go into the same sets, so a run can't add the same business twice.

---

## How to Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install gspread google-auth
python main.py
```

Requires:
- `creds.json` (Google service account key) in the project root, with the sheet shared (**Editor**) with the service account's email.
- A Serper.dev API key in `serper_api_key.txt` (or the `SERPER_API_KEY` environment variable). Sign up at serper.dev; new accounts get 2,500 free credits.

**Costs:**
- The Google Sheets API is free.
- Each Serper Maps search costs **3 credits**. Credits cost about $1 per 1,000 ($50 for 50,000, valid 6 months).
- In testing, a search page averaged several businesses with no website, so 300 leads a day should use roughly **150–250 credits a day**. That's about **$5–8 a month**, or **under 0.1¢ per lead**.
- Harder categories in affluent cities, like plumbers in Naples, use more credits per lead.
- `MAX_SERPER_CREDITS_PER_MONTH` in `config.py` (default 10,000, about $10) stops the agent before spend can run away.
