CREATE DATABASE bank_reviews;
-- 1. Create database
-- 2. Connect to the database

-- 3. Create Banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100),
    app_name VARCHAR(100)
);

-- 4. Create Reviews table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC,
    source VARCHAR(50)
);

-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) AS review_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name;

-- Average rating per bank
SELECT b.bank_name, AVG(r.rating) AS avg_rating
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_name;
