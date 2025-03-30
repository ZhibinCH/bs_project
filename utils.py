# utils.py
# Standard library imports
import os
from datetime import datetime

# Third-party imports
import pandas as pd


def save_to_csv(tweets, filename_prefix="solana_tweets", output_dir="outputs"):
    if not isinstance(tweets, pd.DataFrame):
        if not tweets:
            print("No tweets to save. Skipping CSV export.")
            return
        # Convert to DataFrame
        df = pd.DataFrame(tweets)
    else:
        df = tweets.copy()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate filename with today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{output_dir}/{filename_prefix}_{today}.csv"
    
    # Save to CSV (without index column)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Saved {len(df)} tweets to {filename}")
    return df