from google_play_scraper import reviews
import psycopg2
from datetime import datetime

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="YOUR_USERNAME",
    password="YOUR_PASSWORD"
)
cur = conn.cursor()

# List of banks and their Google Play app IDs
banks = {
    "Awash Bank": "com.awashbank.app",       # replace with actual app ID
    "Dashen Bank": "com.dashenbank.app",     # replace with actual app ID
    "CBE Bank": "com.cbe.app"                # replace with actual app ID
}

# Insert banks into the database
for bank_name, app_id in banks.items():
    cur.execute("""
        INSERT INTO banks (bank_name, app_name)
        VALUES (%s, %s)
        ON CONFLICT (bank_id) DO NOTHING
    """, (bank_name, app_id))

# Fetch bank IDs
cur.execute("SELECT bank_id, bank_name FROM banks")
bank_map = {name: bank_id for bank_id, name in cur.fetchall()}

# Scrape reviews and insert
for bank_name, app_id in banks.items():
    print(f"Scraping reviews for {bank_name}...")
    all_reviews, _ = reviews(
        app_id,
        lang='en',
        country='us',
        count=500  # scrape 500 reviews per app
    )

    for r in all_reviews:
        bank_id = bank_map[bank_name]
        review_text = r['content']
        rating = r['score']
        review_date = r['at'].date()
        sentiment_label = None       # optional, can run sentiment analysis later
        sentiment_score = None       # optional
        source = "Google Play"

        cur.execute("""
            INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source))

conn.commit()
cur.close()
conn.close()
print("Scraping and insertion completed!")
