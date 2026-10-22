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

# Serper.dev credits allowed per calendar month. Each Maps search costs 3 credits; credits are ~$1 per 1,000.
# 10,000 credits = ~$10/month max. 300 leads/day uses roughly 150-250 credits/day.
MAX_SERPER_CREDITS_PER_MONTH = 10000

# Result pages to read per search (20 businesses each). Deeper pages have more businesses without websites.
MAX_PAGES_PER_SEARCH = 10

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

# Leads added per run, and the most the agent will add in one day (re-running the same day stops early)
LEADS_PER_RUN = 50
MAX_LEADS_PER_DAY = 300

# High-net-worth cities and suburbs across the US, West Coast first
CITIES = [
    # California — Bay Area
    "Atherton CA", "Palo Alto CA", "Los Altos CA", "Menlo Park CA", "Woodside CA",
    "Saratoga CA", "Los Gatos CA", "Cupertino CA", "Hillsborough CA", "Burlingame CA",
    "San Mateo CA", "San Francisco CA", "Mill Valley CA", "Sausalito CA", "Tiburon CA",
    "Walnut Creek CA", "Danville CA", "Lafayette CA", "Orinda CA", "Piedmont CA",
    "Pleasanton CA", "San Ramon CA", "Napa CA", "Sonoma CA",
    # California — Southern / Central
    "Beverly Hills CA", "Malibu CA", "Santa Monica CA", "Pacific Palisades CA", "Brentwood CA",
    "Manhattan Beach CA", "Palos Verdes Estates CA", "Calabasas CA", "Westlake Village CA",
    "Pasadena CA", "San Marino CA", "La Canada Flintridge CA", "Newport Beach CA",
    "Laguna Beach CA", "Irvine CA", "Dana Point CA", "San Clemente CA", "Rancho Santa Fe CA",
    "La Jolla CA", "Del Mar CA", "Carlsbad CA", "Coronado CA", "Santa Barbara CA",
    "Montecito CA", "Carmel-by-the-Sea CA", "Palm Springs CA", "Truckee CA",
    # Pacific Northwest
    "Bellevue WA", "Medina WA", "Mercer Island WA", "Kirkland WA", "Redmond WA",
    "Sammamish WA", "Seattle WA", "Issaquah WA", "Lake Oswego OR", "West Linn OR",
    "Portland OR", "Bend OR",
    # Mountain West / Southwest
    "Scottsdale AZ", "Paradise Valley AZ", "Sedona AZ", "Boulder CO", "Aspen CO", "Vail CO",
    "Cherry Hills Village CO", "Castle Rock CO", "Denver CO", "Park City UT", "Salt Lake City UT",
    "Jackson WY", "Ketchum ID", "Boise ID", "Henderson NV", "Summerlin NV", "Reno NV",
    "Santa Fe NM", "Honolulu HI",
    # Texas
    "Highland Park TX", "University Park TX", "Southlake TX", "Colleyville TX", "Plano TX",
    "Frisco TX", "The Woodlands TX", "Bellaire TX", "Sugar Land TX", "Austin TX",
    "West Lake Hills TX", "San Antonio TX",
    # Midwest
    "Winnetka IL", "Lake Forest IL", "Highland Park IL", "Glencoe IL", "Hinsdale IL",
    "Naperville IL", "Oak Brook IL", "Chicago IL", "Edina MN", "Wayzata MN", "Minnetonka MN",
    "Leawood KS", "Overland Park KS", "Mission Hills KS", "Ladue MO", "Clayton MO",
    "Bloomfield Hills MI", "Birmingham MI", "Grosse Pointe MI", "Ann Arbor MI",
    "Carmel IN", "Zionsville IN", "Dublin OH", "Upper Arlington OH", "Indian Hill OH",
    "Shaker Heights OH", "Mequon WI",
    # South
    "Nashville TN", "Franklin TN", "Brentwood TN", "Mountain Brook AL", "New Orleans LA",
    "Buckhead GA", "Alpharetta GA", "Johns Creek GA", "Milton GA",
    "Charlotte NC", "Raleigh NC", "Cary NC", "Chapel Hill NC", "Asheville NC",
    "Charleston SC", "Mount Pleasant SC", "Hilton Head Island SC",
    # Florida
    "Naples FL", "Boca Raton FL", "Palm Beach FL", "Jupiter FL", "Coral Gables FL",
    "Key Biscayne FL", "Miami Beach FL", "Fort Lauderdale FL", "Winter Park FL",
    "Sarasota FL", "Ponte Vedra Beach FL",
    # Mid-Atlantic
    "Bethesda MD", "Potomac MD", "Chevy Chase MD", "Annapolis MD", "McLean VA",
    "Great Falls VA", "Arlington VA", "Alexandria VA", "Washington DC",
    # Northeast
    "Greenwich CT", "Darien CT", "New Canaan CT", "Westport CT", "Scarsdale NY", "Rye NY",
    "Bronxville NY", "Manhattan NY", "Brooklyn NY", "Great Neck NY", "Garden City NY",
    "Southampton NY", "East Hampton NY", "Princeton NJ", "Short Hills NJ", "Summit NJ",
    "Montclair NJ", "Ridgewood NJ", "Saddle River NJ", "Bryn Mawr PA", "Villanova PA",
    "Philadelphia PA", "Wellesley MA", "Weston MA", "Newton MA", "Lexington MA",
    "Brookline MA", "Boston MA", "Newport RI",
]
