# main.py
# Standard library imports
import os
import time
from datetime import datetime, timedelta

# Third-party imports
from dotenv import load_dotenv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Local application imports
from config import (
    CHROME_OPTIONS,
    DEFAULT_DAYS,
    MAX_TWEETS,
    SCROLL_ATTEMPTS,
    SEARCH_URL_TEMPLATE
)
from evaluator import evaluate_dataframe
from twitter.auth import login
from twitter.scraper import scrape_tweets, scroll_to_load_tweets
from utils import save_to_csv

def setup_browser():

    print("Setting up Chrome browser...")
    options = webdriver.ChromeOptions()
    
    # Apply all settings from config.py
    for arg, value in CHROME_OPTIONS.items():
        options.add_argument(f"--{arg.replace('_', '-')}={value}")
    
    # Initialize driver with automatic ChromeDriver management
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def main():
    # --- Initialization ---
    load_dotenv()  # Load environment variables from .env
    print("=== Solana Tweet Scraper ===")

    # --- Browser Setup ---
    driver = setup_browser()
    driver.set_page_load_timeout(30)  # 30-second page load timeout

    try:
        # --- Login ---
        login(
            driver,
            email=os.getenv("TWITTER_EMAIL"),
            password=os.getenv("TWITTER_PASSWORD"),
            username=os.getenv("TWITTER_USERNAME"),
        )

        # --- Search for Tweets ---
        start_date = (datetime.now() - timedelta(days=DEFAULT_DAYS)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        search_url = SEARCH_URL_TEMPLATE.format(start_date=start_date, end_date=end_date)

        print(f"Searching tweets from {start_date} to {end_date}...")
        driver.get(search_url)
        time.sleep(5)  # Wait for search results to load

        # --- Scraping ---
        scroll_to_load_tweets(driver, SCROLL_ATTEMPTS)
        tweets = scrape_tweets(driver, MAX_TWEETS)

        # --- Save Results ---
        tweets_df = save_to_csv(tweets)
        
        # --- Results ---
        print("\n=== Results ===")
        print(f"Total tweets collected: {len(tweets)}")
        print("\n=== Evaluation ===")
        evaluated_tweets = evaluate_dataframe(tweets_df)
        evaluated_tweets_df = save_to_csv(evaluated_tweets, filename_prefix="evaluated_tweets")
        print(f"Evaluated tweet dataframe has shape: {evaluated_tweets_df.shape}")
    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error.png")  # Save screenshot for debugging
    finally:
        driver.quit()
        print("Browser closed. Done!")

if __name__ == "__main__":
    main()