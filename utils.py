import pandas as pd

from datetime import datetime


def datetime_to_str(timestamp: str) -> str:
    return datetime.strftime(timestamp, '%H:%M:%S|%d-%m-%y')


def utc_to_datetime(timestamp: float) -> str:
    return datetime.utcfromtimestamp(timestamp)


def str_to_datetime(time_string: str) -> str:
    return datetime.strptime(time_string, '%d-%m-%y')


def data_to_csv(data, filename='') -> None:
    now = datetime.now()
    timestamp_str = datetime_to_str(now)
    filename = f'posts-{timestamp_str}.csv' if filename != '' else 'posts.csv'

    if type(data) == 'dict':
        dataframe = pd.DataFrame.from_dict(data)

    else:
        dataframe = pd.DataFrame(data,
                                 columns=[
                                     'title', 'selftext', 'ups', 'downs',
                                     'link_flair_text', 'upvote_ratio',
                                     'num_comments', 'timestamp', 'url',
                                     'permalink'
                                 ])

    dataframe.to_csv(filename, sep=',')
    print(f'> data written to {filename}!')
