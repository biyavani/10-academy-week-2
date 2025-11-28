import pandas as pd
import re
from textblob import TextBlob


def get_sentiment(text):
    '''
    Get sentiment polarity of the text.

    Parameters:
    text (str): Text for sentiment analysis

    Returns:
    float: Sentiment polarity
    '''
    blob_obj = TextBlob(text)
    polarity_score = blob_obj.sentiment.polarity
    return polarity_score


def extract_domain(email):
    '''
    Extracts the domain from an email address.

    Parameters:
    email (str): Email address

    Returns:
    str: Domain name    
    '''
    found = re.search(r'@[\w.]+', email)
    return found.group() if found else None


def calculate_moving_averages(data, window=50):
    '''
    Calculate simple and exponential moving averages for the given stock data.

    Parameters:
    data (DataFrame): Stock data
    window (int): Window size for moving averages

    Returns:
    DataFrame: Stock data with moving averages 
    '''
    df_calc = data.copy()
    df_calc['SMA'] = df_calc['Close'].rolling(window=window).mean()
    df_calc['EMA'] = df_calc['Close'].ewm(span=window, adjust=False).mean()
    return df_calc


def read_csv_file(file_path):
    '''
    Read and clean a CSV file.

    Parameters:
    file_path (str): Path to the CSV file

    Returns:
    dict: Dictionary with cleaned data, column names, and row count
    '''
    csv_df = pd.read_csv(file_path)
    csv_df = csv_df.loc[:, ~csv_df.columns.str.contains('^Unnamed')]
    columns_list = list(csv_df.columns)
    total_rows = len(csv_df)

    return {
        'data': csv_df,
        'column_names': columns_list,
        'row_count': total_rows
    }


def merge_data(news_data, stock_data, date_column, stock_date_column):
    '''
    Merge news and stock data on the specified date column.

    Parameters:
    news_data (DataFrame): News data
    stock_data (DataFrame): Stock data
    date_column (str): Date column in the news data
    stock_date_column (str): Date column in the stock data

    Returns:
    DataFrame: Merged data
    '''
    joined_df = pd.merge(
        stock_data,
        news_data,
        left_on=date_column,
        right_on=stock_date_column,
        how='inner'
    )
    return joined_df
