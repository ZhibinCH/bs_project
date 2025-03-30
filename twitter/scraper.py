# twitter/scraper.py
# Standard library imports
import time
import random

# Third-party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_to_load_tweets(driver, max_attempts):

    print(f"Scrolling to load tweets (max attempts: {max_attempts})...")
    last_height = driver.execute_script("return document.body.scrollHeight")

    for attempt in range(max_attempts):
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.uniform(3.0, 5.0))  # Random delay to mimic human behavior

        # Check if new content loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f"No new content after attempt {attempt + 1}. Stopping scroll.")
            break
        last_height = new_height

def scrape_tweets(driver, max_tweets):
    
    print(f"Extracting up to {max_tweets} tweets...")

    # Wait for tweets to load and get all tweet elements
    tweet_elements = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
    )[:max_tweets]

    tweets = []
    for idx, tweet in enumerate(tweet_elements, 1):
        try:
            print(f"Processing tweet {idx}...")
            tweets.append({
                "username": tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]').text,
                "content": tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text,
                "timestamp": tweet.find_element(By.XPATH, './/time').get_attribute('datetime'),
                "link": tweet.find_element(By.XPATH, './/time/..').get_attribute('href'),
                # **extract_engagement(tweet),  # Include replies/reposts/likes/views
            })
        except Exception as e:
            print(f"Failed to extract tweet {idx}: {e}")
            continue

    print(f"Successfully extracted {len(tweets)} tweets.")
    return tweets