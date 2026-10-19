import time
import run_log
from config import INDUSTRIES, CITIES
from places import search_businesses, quota_reached, calls_this_month
from sheet import connect, load_existing, check_write_access, is_duplicate, add_lead
from progress import query_signature, load_progress, save_progress

MAX_LEADS_PER_RUN = 50
MAX_API_FAILURES = 3  # stop if the Places API keeps failing

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
skipped_closed = 0
api_failures = 0
queries_done = 0
stop_reason = ""

print("Starting lead generation agent...")

# Work through searches until 50 leads are found or every search has been run once
while leads_added < MAX_LEADS_PER_RUN and queries_done < len(queries) and not stop_reason:
    keyword, city = queries[query_index]
    print(f"\n'{keyword}' in {city}")

    page_token = None
    for page_num in range(1, 4):  # Google returns at most 3 pages (60 businesses) per search
        if quota_reached():
            stop_reason = "Monthly Places API limit reached (MAX_PLACES_CALLS_PER_MONTH in config.py)."
            break

        businesses, page_token = search_businesses(keyword, city, page_token)
        if businesses is None:
            api_failures += 1
            if api_failures >= MAX_API_FAILURES:
                stop_reason = f"Places API failed {MAX_API_FAILURES} times in a row. Try again later."
            break
        api_failures = 0

        for b in businesses:
            name, phone = b["name"], b["phone"]

            if b["website"]:
                skipped_has_site += 1
                continue

            if not b["open"]:
                print(f"  Skip (closed): {name}")
                skipped_closed += 1
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
            print(f"  Added ({leads_added}/{MAX_LEADS_PER_RUN}): {name} | {phone} | {b['city_state']}")
            time.sleep(1)  # stay under the Google Sheets write limit (60/minute)

            if leads_added >= MAX_LEADS_PER_RUN:
                break

        print(f"  Page {page_num}: {len(businesses)} businesses checked ({skipped_has_site} with websites so far)")
        if leads_added >= MAX_LEADS_PER_RUN or not page_token:
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
      f"No phone: {skipped_no_phone} | Closed: {skipped_closed}")
print(f"Places API calls this month: {calls_this_month()}")
print(f"Next run starts with: '{keyword}' in {city}")
print("Check your Google Sheet.")
