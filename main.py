import time
import run_log
from config import INDUSTRIES, CITIES, LEADS_PER_RUN, MAX_LEADS_PER_DAY, MAX_PAGES_PER_SEARCH
from serper import search_businesses, quota_reached, credits_this_month
from sheet import connect, load_existing, check_write_access, is_duplicate, add_lead
from progress import query_signature, load_progress, save_progress, leads_added_today, record_lead

MAX_API_FAILURES = 3  # stop if Serper keeps failing

run_log.start()
sheet = connect()
existing_names, existing_phones, next_row = load_existing(sheet)
check_write_access(sheet, next_row)
print(f"Loaded {len(existing_names)} existing leads from the sheet.")

# Flat ordered list of every (keyword, city) search, e.g. ("plumber", "Naples, FL")
queries = []
for keywords in INDUSTRIES.values():
    for keyword in keywords:
        for city in CITIES:
            state = city.rsplit(" ", 1)
            queries.append((keyword, f"{state[0]}, {state[1]}" if len(state) == 2 else city))

signature = query_signature(queries)
query_index = load_progress(signature) % len(queries)

leads_added = 0
skipped_has_site = 0
skipped_duplicate = 0
skipped_no_phone = 0
api_failures = 0
queries_done = 0
stop_reason = ""

# Never add more than MAX_LEADS_PER_DAY in a day, even across several runs
MAX_LEADS_PER_RUN = min(LEADS_PER_RUN, MAX_LEADS_PER_DAY - leads_added_today())
if MAX_LEADS_PER_RUN <= 0:
    raise SystemExit(f"Already added {leads_added_today()} leads today (MAX_LEADS_PER_DAY = {MAX_LEADS_PER_DAY}). Run again tomorrow.")

print(f"Starting lead generation agent — target {MAX_LEADS_PER_RUN} leads ({leads_added_today()} already added today)...")

# Work through searches until the lead target is reached or every search has been run once
while leads_added < MAX_LEADS_PER_RUN and queries_done < len(queries) and not stop_reason:
    keyword, city = queries[query_index]
    print(f"\n'{keyword}' in {city}")

    ll = None
    seen = set()  # businesses already seen in this search (pages can overlap)
    for page_num in range(1, MAX_PAGES_PER_SEARCH + 1):
        if quota_reached():
            stop_reason = "Monthly Serper credit limit reached (MAX_SERPER_CREDITS_PER_MONTH in config.py)."
            break

        businesses, ll = search_businesses(keyword, city, page_num, ll)
        if businesses is None:
            api_failures += 1
            if api_failures >= MAX_API_FAILURES:
                stop_reason = f"Serper failed {MAX_API_FAILURES} times in a row. Try again later."
            break
        api_failures = 0

        new = [b for b in businesses if b["id"] not in seen]
        seen.update(b["id"] for b in businesses)

        for b in new:
            name, phone = b["name"], b["phone"]

            if b["website"]:
                skipped_has_site += 1
                continue

            if not phone:
                print(f"  Skip (no phone): {name}")
                skipped_no_phone += 1
                continue

            if is_duplicate(name, phone, existing_names, existing_phones):
                print(f"  Skip (already in sheet): {name}")
                skipped_duplicate += 1
                continue

            add_lead(sheet, next_row, name, phone, "", b["city_state"], existing_names, existing_phones)
            next_row += 1
            leads_added += 1
            record_lead()
            print(f"  Added ({leads_added}/{MAX_LEADS_PER_RUN}): {name} | {phone} | {b['city_state']}")
            time.sleep(1)  # stay under the Google Sheets write limit (60/minute)

            if leads_added >= MAX_LEADS_PER_RUN:
                break

        print(f"  Page {page_num}: {len(new)} new businesses checked ({skipped_has_site} with websites so far)")
        # Stop paging when Google has nothing new left for this search
        if leads_added >= MAX_LEADS_PER_RUN or not new or len(businesses) < 20 or not ll:
            break

    if stop_reason or leads_added >= MAX_LEADS_PER_RUN:
        # Stopped partway through this search — redo it next run (businesses already added are skipped)
        save_progress(query_index, signature)
        break

    query_index = (query_index + 1) % len(queries)
    queries_done += 1
    save_progress(query_index, signature)

if stop_reason:
    print(f"\n{stop_reason}")

keyword, city = queries[query_index]
print(f"\nDone! Added: {leads_added} | Have website: {skipped_has_site} | Already in sheet: {skipped_duplicate} | "
      f"No phone: {skipped_no_phone}")
print(f"Serper credits used this month: {credits_this_month()} (about ${credits_this_month() / 1000:.2f})")
print(f"Next run starts with: '{keyword}' in {city}")
print("Check your Google Sheet.")
