import pandas as pd

from datetime import datetime


def datetime_to_str(timestamp: str) -> str:
    """
    Given a string representation of a timestamp, returns a string
    representation of the timestamp in the format 'HH-MM-SS.DD-MM-YY'.

    Parameters:
        timestamp (str): A string representation of a timestamp, in any format.

    Returns:
        A string representation of the timestamp in the format 'HH-MM-SS.DD-MM-YY'.
    """
    return datetime.strftime(timestamp, '%H:%M:%S|%d-%m-%y')


def utc_to_datetime(timestamp: float) -> str:
    """
    Converts a UTC float timestamp to a date string in the format 'HH-MM-SS.DD-MM-YY'.

    Parameters:
        timestamp (float): A UTC float timestamp.

    Returns:
        A string representation of the timestamp in the format 'HH-MM-SS.DD-MM-YY'.
    """
    return datetime.utcfromtimestamp(timestamp)


def str_to_datetime(time_string: str) -> str:
    """
    Converts a string representation of a date in the format 'DD-MM-YY' to a datetime object.

    Parameters:
        time_string (str): A string representing a date in the format 'DD-MM-YY'.

    Returns:
        A string representation of a datetime object that corresponds to the given time_string.
    """
    return datetime.strptime(time_string, '%d-%m-%y')


def data_to_csv(data, filename='') -> None:
    """
    Given a dictionary of data, creates a pandas DataFrame and writes it to a CSV file
    with a filename in the format 'posts-HH-MM-SS.DD-MM-YY.csv', where the timestamp
    is the current local time.

    Parameters:
        data (dict): A dictionary of data to be written to a CSV file.

    Returns:
        None
    """

    now = datetime.now()
    timestamp_str = datetime_to_str(now)
    filename = f'posts-{timestamp_str}.csv' if filename != '' else 'posts.csv'

    if type(data) == 'dict':
        dataframe = pd.DataFrame.from_dict(data)

    else:
        dataframe = pd.DataFrame(data, columns=['title', 'selftext', 'ups', 'downs', 'link_flair_text',
                                                'upvote_ratio', 'num_comments', 'timestamp', 'url', 'permalink'])

    dataframe.to_csv(filename, sep=',')
    print(f'> data written to {filename}!')
