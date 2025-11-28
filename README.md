## Methodology

1. **Web Scraping**  
   - Collected reviews, ratings, dates, and app names for **CBE, Dashen Bank, and Awash Bank**.  
   - Targeted a minimum of **400 reviews per bank** using `google-play-scraper`.  
   - Ensured **English language** reviews to maintain consistency.  
   - Filtered out non-relevant or duplicate reviews during scraping.  
   - Collected data in **batches** to handle API or network limitations efficiently.  

2. **Preprocessing**  
   - Removed duplicate reviews to avoid bias in analysis.  
   - Handled missing values, ensuring **<5% missing data** in the final dataset.  
   - Normalized dates to `YYYY-MM-DD` format for consistency and easier time-series analysis.  
   - Checked for **invalid or empty review entries** and cleaned them.  
   - Saved cleaned data to **`bank_reviews.csv`** for downstream analysis.  

3. **Dataset**  
   - Columns: `review`, `rating`, `date`, `bank`, `source`.  
   - Total reviews: **1,200+**, meeting target KPI.  
   - Verified **data quality metrics** such as completeness and consistency.  
   - Dataset structured to allow **easy sentiment analysis, theme extraction, and visualization**.  

4. **Reproducibility & Documentation**  
   - Scripts (`scraper.py` and `preprocessing.py`) are modular and reusable.  
   - `requirements.txt` included to ensure **all dependencies are tracked**.  
   - Project structured with **`src/` for scripts** and **`data/` for outputs**.  
