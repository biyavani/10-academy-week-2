from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime

# ------------ CONFIGURATION ------------
BANK_APPS = {
    "CBE": "com.cbe.customer",           # example app ID — replace if needed
    "Dashen": "com.dashenbank.mobile",      # example app ID — replace
    "BOA": "com.bankofabyssinia.mobile"   # example app ID — replace
}

TOTAL_REVIEWS = 400   # per bank
OUTPUT_FILE = "data/google_reviews_raw.csv"
# ---------------------------------------


def fetch_reviews(app_id, bank_name, total=400):
    """Scrape reviews for one app from Google Play."""
    all_reviews = []
    count = 0
    next_token = None

    while count < total:
        batch, next_token = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=200,
            continuation_token=next_token
        )

        for r in batch:
            all_reviews.append({
                "review": r["content"],
                "rating": r["score"],
                "date": r["at"].strftime("%Y-%m-%d"),
                "bank": bank_name,
                "source": "Google Play"
            })

        count += len(batch)

        if not next_token:
            break

    return all_reviews


def main():
    all_data = []

    for bank, app_id in BANK_APPS.items():
        print(f"Scraping {bank}...")
        rows = fetch_reviews(app_id, bank, TOTAL_REVIEWS)
        all_data.extend(rows)

    df = pd.DataFrame(all_data)

    # Remove duplicates & missing
    df.drop_duplicates(subset=["review"], inplace=True)
    df.dropna(inplace=True)

    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} cleaned reviews to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

