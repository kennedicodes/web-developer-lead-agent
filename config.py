SHEET_ID = "1pmrDIdcl15OYWrnK_srha1UlzLu4EkgnlMUB2sA_F0w"  # from the URL: /spreadsheets/d/THIS_PART/edit

# Local-service categories where many businesses have no website
INDUSTRIES = {
    "home services": ["plumber", "electrician", "hvac", "roofing contractor", "handyman",
                      "painting contractor", "flooring contractor", "locksmith", "pressure washing"],
    "outdoor": ["landscaping", "lawn care", "tree service"],
    "cleaning": ["house cleaning", "carpet cleaning", "dry cleaners"],
    "automotive": ["auto repair", "auto body shop", "towing"],
    "personal care": ["barber shop", "nail salon", "hair salon", "beauty supply"],
    "other services": ["tailor", "moving company", "pet grooming", "daycare", "tutoring"],
    "food": ["restaurant", "food truck", "bakery"],
}

# Google Places API calls allowed per calendar month (1,000 are free; above that ~$35 per 1,000).
# Raise this only if you're OK paying for extra lookups.
MAX_PLACES_CALLS_PER_MONTH = 1000

# Websites on these sites are listings/profiles, not the business's own website
DIRECTORY_DOMAINS = [
    "yellowpages.com", "yelp.com", "facebook.com", "instagram.com", "linkedin.com",
    "twitter.com", "x.com", "tiktok.com", "youtube.com", "pinterest.com", "nextdoor.com",
    "bbb.org", "mapquest.com", "manta.com", "angi.com", "angieslist.com", "homeadvisor.com",
    "thumbtack.com", "houzz.com", "porch.com", "buildzoom.com", "bark.com", "birdeye.com",
    "superpages.com", "citysearch.com", "chamberofcommerce.com", "alignable.com", "dnb.com",
    "bizapedia.com", "opencorporates.com", "buzzfile.com", "loc8nearme.com", "cylex.us.com",
    "hotfrog.com", "merchantcircle.com", "showmelocal.com", "brownbook.net", "n49.com",
    "google.com", "apple.com", "bing.com", "yahoo.com", "duckduckgo.com", "wikipedia.org",
    "tripadvisor.com", "opentable.com", "doordash.com", "ubereats.com", "grubhub.com",
    "seamless.org", "postmates.com", "menupix.com", "allmenus.com", "menuism.com",
    "groupon.com", "zillow.com", "carfax.com", "cars.com", "repairpal.com", "care.com",
    "winnie.com", "vagaro.com", "styleseat.com", "booksy.com", "fresha.com", "schedulicity.com",
    "indeed.com", "glassdoor.com", "ziprecruiter.com", "nj.com", "patch.com", "reddit.com",
]

CITIES = [
     # EST
    "Naples FL", "Boca Raton FL", "Coral Gables FL",
    "Bethesda MD", "McLean VA", "Greenwich CT",
    "Charlotte NC", "Raleigh NC", "Atlanta GA",
    "Princeton NJ", "Westchester NY",
    # CST
    "Highland Park TX", "Southlake TX", "The Woodlands TX",
    "Austin TX", "Nashville TN", "Franklin TN",
    "Naperville IL", "Winnetka IL", "Lake Forest IL",
    "Edina MN", "Leawood KS"
]
