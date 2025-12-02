import psycopg2
import pandas as pd

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bank_reviews",
    user="postgres",
    password="4525"
)

# Load reviews with bank info
query = """
SELECT r.review_text, r.rating, r.sentiment_label, r.sentiment_score, b.bank_name
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
"""
df = pd.read_sql(query, conn)
conn.close()

print(df.head())
from textblob import TextBlob

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return label, polarity

df[['sentiment_label', 'sentiment_score']] = df['review_text'].apply(lambda x: pd.Series(analyze_sentiment(x)))
# Top positive reviews per bank (drivers)
for bank in df['bank_name'].unique():
    print(f"\nTop positive reviews for {bank}:")
    top_reviews = df[df['bank_name'] == bank].sort_values(by='sentiment_score', ascending=False).head(5)
    for r in top_reviews['review_text']:
        print("-", r)

# Top negative reviews per bank (pain points)
for bank in df['bank_name'].unique():
    print(f"\nTop negative reviews for {bank}:")
    bottom_reviews = df[df['bank_name'] == bank].sort_values(by='sentiment_score').head(5)
    for r in bottom_reviews['review_text']:
        print("-", r)
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
sns.countplot(data=df, x='bank_name', hue='sentiment_label')
plt.title("Sentiment Distribution per Bank")
plt.ylabel("Number of Reviews")
plt.xlabel("Bank")
plt.legend(title='Sentiment')
plt.tight_layout()
plt.show()
plt.figure(figsize=(8,5))
sns.boxplot(data=df, x='bank_name', y='rating')
plt.title("Rating Distribution per Bank")
plt.ylabel("Rating (1-5)")
plt.xlabel("Bank")
plt.tight_layout()
plt.show()
from wordcloud import WordCloud

for bank in df['bank_name'].unique():
    text = " ".join(df[(df['bank_name'] == bank) & (df['sentiment_label']=='Negative')]['review_text'])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Negative Review Keywords - {bank}")
    plt.show()

