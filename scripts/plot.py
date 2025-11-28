import pandas as pd
import matplotlib.pyplot as plt

def plot_correlation(data, x_col, y_col, title):
    '''
    Plot the correlation between two columns in the data

    :param data: The DataFrame containing the data
    :param x_col: The column name for the x-axis
    :param y_col: The column name for the y-axis
    :param title: The title of the plot

    :return: None
    '''
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data[x_col], data[y_col], c='blue')
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True)
    plt.tight_layout()
    plt.show()


def plot_moving_averages(data, date_column, stock_value_column, window, title):
    '''
    Plot the moving averages for a given stock.

    Parameters:
    - data: DataFrame containing historical stock data
    - date_column: Name of the column containing date information
    - stock_value_column: Name of the column containing stock values
    - window: Window size for moving averages
    - title: Title of the plot

    Returns:
    - None (displays the plot)
    '''
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data[date_column], data[stock_value_column], label='Close Price')
    ax.plot(data[date_column], data['SMA'], label=f'SMA ({window})')
    ax.plot(data[date_column], data['EMA'], label=f'EMA ({window})')
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()


def plot_stock_data(df, date_column='date', stock_value_column='stock_value', title='Stock Value Over Time'):
    """
    Plots stock value over time from a CSV file.

    Args:
    - file_path (str): Path to the CSV file.
    - date_column (str): The name of the date column in the CSV file (default is 'date').
    - stock_value_column (str): The name of the stock value column in the CSV file (default is 'stock_value').
    - title (str): Title for the plot (default is 'Stock Value Over Time').
    """

    # Convert to datetime and clean invalid entries
    df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df = df.dropna(subset=[date_column])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df[date_column], df[stock_value_column], color='b', label=stock_value_column)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Value')
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_time_series(data, time_unit, title, xlabel):
    """
    Plots article count over time (year, month, week, or day) aggregated by the specified time_unit.

    Parameters:
        data: DataFrame containing a datetime column 'date'.
        time_unit: One of 'year', 'month', 'week', or 'day'.
        title: Title of the plot.
        xlabel: Label for the x-axis.
    """
    # Create helper columns for grouping
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.to_period('M').astype(str)
    data['week'] = data['date'].dt.to_period('W').astype(str)
    data['day'] = data['date'].dt.date

    group_col = None
    if time_unit == 'year':
        group_col = 'year'
    elif time_unit == 'month':
        group_col = 'month'
    elif time_unit == 'week':
        group_col = 'week'
    elif time_unit == 'day':
        group_col = 'day'
    else:
        raise ValueError("Invalid time_unit. Choose from 'year', 'month', 'week', or 'day'.")

    agg_data = data.groupby(group_col).size().reset_index(name='article_count')

    fig, ax = plt.subplots(figsize=(24, 6))
    ax.plot(agg_data[group_col], agg_data['article_count'], marker='o')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Article Count')
    plt.xticks(rotation=90)
    ax.grid(True)
    plt.tight_layout()
    plt.show()
