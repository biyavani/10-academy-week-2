import psycopg2
import pandas as pd

# Load cleaned reviews from CSV (optional)
df = pd.read_csv("cleaned_reviews.csv")  # Columns: bank_name, app_name, review_text, rating, review_date, sentiment_label, sentiment_score, source

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="4525"
)
cur = conn.cursor()

# Insert unique banks
banks = df[['bank_name', 'app_name']].drop_duplicates()
for _, row in banks.iterrows():
    cur.execute("""
        INSERT INTO banks (bank_name, app_name)
        VALUES (%s, %s)
        ON CONFLICT (bank_id) DO NOTHING
    """, (row['bank_name'], row['app_name']))

# Get bank IDs
cur.execute("SELECT bank_id, bank_name FROM banks")
bank_map = {name: bank_id for bank_id, name in cur.fetchall()}

# Insert reviews
for _, row in df.iterrows():
    bank_id = bank_map[row['bank_name']]
    cur.execute("""
        INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        bank_id,
        row['review_text'],
        row['rating'],
        row['review_date'],
        row['sentiment_label'],
        row['sentiment_score'],
        row['source']
    ))

# Commit changes and close
conn.commit()
cur.close()
conn.close()

print("Reviews inserted successfully!")
