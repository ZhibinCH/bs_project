# Solana-Related X (Twitter) & Reddit Scraper & LLM Evaluator

## Project Overview
This project focuses on web scraping recent Solana-related posts from **X (formerly Twitter)**, evaluating them using the **LLaMA-3.2-3B-Instruct** language model, and storing the results in **CSV format**. Due to **X's rate limits**, **Reddit scraping is included as a supplementary source**, but the primary focus remains on X. The Reddit scraper is implemented **only in a Jupyter Notebook** for demonstration purposes, while all other functionalities are executed through Python scripts.

## Features
- **Web Scraping**: Extracts recent Solana-related posts from X (last 7 days), with Reddit as an optional supplement.
- **LLM Evaluation**: Scores or classifies content based on various criteria such as relevance, risk, and reliability.
- **Data Storage**: Outputs the results in CSV format.
- **Jupyter Notebook Implementation for Reddit**: Demonstrates Reddit scraping interactively.
- **Python Scripts for X Scraping and Evaluation**: Dedicated scripts handle X scraping and LLM evaluation efficiently.

---

## Requirements
### Environment Setup (Conda)
It is recommended to use **Conda** to manage the environment. First, create and activate a new Conda environment:
```bash
conda create --name bs_project python=3.10 -y
conda activate bs_project
```

### Dependencies
Once inside the Conda environment, install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
### Setting Up Environment Variables
To run the project, you need to create a `.env` file in the root directory of the project and set up the following environment variables:
```bash
TWITTER_BEARER_TOKEN=<your_token>
TWITTER_EMAIL=<your_email>
TWITTER_USERNAME=<your_username>
TWITTER_PASSWORD=<your_password>
REDDIT_CLIENT_ID=<your_client_id>
REDDIT_CLIENT_SECRET=<your_client_secret>
REDDIT_USER_AGENT=<your_user_agent>
```

Make sure to replace the placeholders with your actual credentials to enable proper authentication for both Twitter and Reddit APIs.

---

## Implementation Details
### 1. Web Scraping
#### Tools Used
- **X Scraping (Primary Focus)**:
  - `selenium`: Extracts X posts.
  - Filters out retweets and non-English content.
- **Reddit Scraping (Supplementary, Jupyter Notebook Only)**:
  - `praw`: Fetches recent Solana-related posts.
  - Extracts up to 100 posts per predefined subreddit from the last 7 days.

#### Scraping Logic
- Extract posts containing "Solana" or "SOL" from the last 7 days.

### 2. LLM Evaluation
#### Language Model
- **LLaMA-3.2-3B-Instruct** is used for text classification and scoring.

#### Evaluation Criteria
Each post is analyzed based on:
- **Relevance Score (1-10)**: How strongly the post relates to Solana (10 = Directly about Solana, 1 = No clear connection).
- **Risk Level (Low/Medium/High)**: Identifies scam risks, misleading content, or speculative claims (High = Scams, misinformation, hate speech).
- **Reliability Score (1-10)**: Evaluates credibility based on user reputation and content validity (10 = Verified source + citations, 1 = Demonstrably false).
- **Sentiment (Positive/Neutral/Negative)**: Determines the overall tone of the post.
- **Credibility Score (1-10)**: Measures how credible the source/content is (10 = Verified source, 1 = Anonymous account or past misinformation).
- **Category Tags (Comma-Separated)**: Classifies the post into relevant categories (e.g., News, Investment Advice, Meme, Scam Alert).

### 3. Output
The project generates CSV files containing:
- Raw Data: The original scraped content from X and Reddit, ready for evaluation
- Evaluated Data: Processed content with LLM-assigned scores and classifications.
- **Note**: The data present in the outputs folder is primarily for demonstration purposes and may contain a limited number of rows.

---

## Folder Structure
```
bs_project/
│-- config.py 
│-- evaluator.py 
│-- outputs/
│   ├── evaluated_reddit_20250330.csv
│   ├── evaluated_tweets_20250330.csv
│   ├── solana_reddit_20250330.csv
│   ├── solana_tweets_20250330.csv
│-- twitter/
│   ├── auth.py
│   ├── scraper.py
│-- main.py 
│-- reddit_scraper.ipynb 
│-- README.md
│-- requirements.txt
│-- utils.py
```
- `evaluator.py`: Post evaluation used for x and reddit contents.
- `outputs/`: Stores raw and evaluated CSV files.
- `twitter/`: Contains scripts for X authentication and scraping.
- `main.py`: Main entry point to run scraping and evaluation.
- `reddit_scraper.ipynb`: **Jupyter Notebook for Reddit scraping (demonstration only).**
- `README.md`: Project documentation.
- `requirements.txt`: Lists all dependencies.
- `utils.py`: Helper functions for preprocessing and evaluation.

---

## Usage
### Running the Notebook (Reddit Scraping Only)
To run the **Reddit scraper (optional)**, open the Jupyter Notebook with VS Code or another preferred IDE and then run the notebook cells to execute the scraping process.

### Running Python Scripts (X Scraping & Evaluation)
To execute scraping and evaluation for **X (primary focus)**:
```bash
python main.py
```

---

## Limitations & Considerations
- **X Rate Limits**: Reddit scraping is implemented **only as a backup demonstration**, not as the primary source.
- **Bias in LLM**: LLaMA-3.2-3B-Instruct may have biases affecting risk and sentiment analysis. 
---

## Future Enhancements
- Use **Google Perspective API** for toxicity detection and **TextBlob** for sentiment analysis.
- Explore the use of a fine-tuned LLaMA model to improve the accuracy of evaluations.
- Investigate the integration of multiple language models to generate combined scoring for more robust assessments.



