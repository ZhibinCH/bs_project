# config.py

# --- Scraper Configuration ---
MAX_TWEETS = 200       # Recommended for most analytical purposes
SCROLL_ATTEMPTS = 10   # Number of scroll attempts to load more tweets
DEFAULT_DAYS = 7       # Default date range (7 days)

# --- Twitter URLs ---
LOGIN_URL = "https://x.com/i/flow/login"
# Search URL template with placeholders for dates
SEARCH_URL_TEMPLATE = (
    "https://x.com/search?q=(solana OR $SOL)%20lang%3Aen%20"
    "since%3A{start_date}%20until%3A{end_date}&src=typed_query"
)

# --- Browser Settings ---
CHROME_OPTIONS = {
    "window_size": "1200x800",      # Browser window dimensions
    "disable_notifications": True,  # Block pop-up notifications
    "detach": True,                 # Keep browser open after script ends
}