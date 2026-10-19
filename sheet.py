import json
import re
import gspread
from google.oauth2.service_account import Credentials
from config import SHEET_ID

# Sheet columns: A = Business name, B = Phone, C = Email, D = City/State
PHONE_PATTERN = re.compile(r"\(?\d{3}\)?[\s.\-]*\d{3}[\s.\-]*\d{4}")
NAME_SUFFIXES = {"llc", "inc", "co", "corp", "corporation", "ltd", "company", "the"}


def connect():
    creds = Credentials.from_service_account_file("creds.json", scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    return gspread.authorize(creds).open_by_key(SHEET_ID).sheet1


def normalize_phone(s):
    """Digits only, last 10 (drops a leading country code). '' if not a full number."""
    digits = re.sub(r"\D", "", s or "")
    return digits[-10:] if len(digits) >= 10 else ""


def normalize_name(s):
    """Lowercase name with any phone number, bullets, punctuation and company suffixes removed."""
    s = PHONE_PATTERN.sub(" ", s or "").lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s.replace("&", " and ").replace("'", ""))
    words = [w for w in s.split() if w not in NAME_SUFFIXES]
    return " ".join(words)


def _header_index(rows):
    """Index of the 'Business Name' header row (the tab has a title and metrics above the table)."""
    for i, row in enumerate(rows):
        if row and row[0].strip().lower() == "business name":
            return i
    raise SystemExit("Couldn't find the 'Business Name' header in column A of the sheet.")


def load_existing(sheet):
    """
    Read every lead in the sheet.
    Returns (names, phones, next_row): dedupe sets plus the first empty row number below the data.
    """
    rows = sheet.get_all_values()
    names, phones = set(), set()
    for row in rows[_header_index(rows) + 1:]:
        col_a = row[0] if len(row) > 0 else ""
        col_b = row[1] if len(row) > 1 else ""

        name = normalize_name(col_a)
        if name:
            names.add(name)

        # Older rows have the phone inside column A; newer rows have it in column B
        for raw in PHONE_PATTERN.findall(col_a) + [col_b]:
            phone = normalize_phone(raw)
            if phone:
                phones.add(phone)
    return names, phones, len(rows) + 1


def check_write_access(sheet, row_num):
    """Fail fast if the service account can read but not edit the sheet (writes an empty value to an empty cell)."""
    try:
        sheet.update(values=[[""]], range_name=f"A{row_num}", value_input_option="RAW")
    except gspread.exceptions.APIError as e:
        if "permission" in str(e).lower():
            with open("creds.json") as f:
                email = json.load(f)["client_email"]
            raise SystemExit(
                f"The agent can read the sheet but can't edit it.\n"
                f"Share the sheet with {email} and give it Editor access, then run again."
            )
        raise


def is_duplicate(name, phone, names, phones):
    phone = normalize_phone(phone)
    return (phone and phone in phones) or normalize_name(name) in names


def add_lead(sheet, row_num, name, phone, email, city_state, names, phones):
    """Write a lead into columns A–D of row_num and record it so this run won't add it again."""
    sheet.update(
        range_name=f"A{row_num}:D{row_num}",
        values=[[name, phone, email, city_state]],
        value_input_option="RAW",
    )
    names.add(normalize_name(name))
    if normalize_phone(phone):
        phones.add(normalize_phone(phone))
