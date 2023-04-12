import pandas as pd
import requests

from datetime import datetime

import config
import utils


class Reddit:
    """
    A class for interacting with Reddit's API using OAuth2 authentication.

    Attributes:
        AUTH_URL (str): The URL to request an access token from Reddit's API.
        BASE_URL (str): The base URL for making API requests.
        client_id (str): The client ID for your Reddit API app.
        client_secret (str): The client secret for your Reddit API app.
        user_agent (str): A string identifying your app to Reddit's API.
        token (str): An OAuth2 access token used to authenticate API requests.

    Methods:
        fetch_token(): Requests an OAuth2 access token from Reddit's API.
        fetch_posts(subreddit, limit=5, mode='top', time='year'): Retrieves posts from a subreddit.
        parse_data(data): Parses and returns data from a Reddit API response.
    """
    AUTH_URL = 'https://www.reddit.com/api/v1/access_token'
    BASE_URL = 'https://oauth.reddit.com/'

    def __init__(self):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.user_agent = 'PythonAPI/0.1'
        self.headers = {
            'User-Agent': self.user_agent
        }
        self.token = None

    def fetch_token(self) -> str:
        """
        Requests an OAuth2 access token from Reddit's API using the client ID and secret.

        Raises:
            requests.HTTPError: If the request to the API fails.
            KeyError: If the response from the API does not contain an access token.
        """
        print('> fetching access token...')
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        data = {
            'grant_type': 'client_credentials',
        }
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                 auth=auth, data=data, headers=self.headers)
        self.token = response.json()['access_token']
        print('> access token fetched!')

    def fetch_posts(self, subreddit, start_date=datetime.now(), end_date=datetime.now(), limit=5, mode='new') -> list:
        """
        Retrieves posts from a subreddit using the Reddit API.

        Parameters:
            subreddit (str): The name of the subreddit to retrieve posts from.
            limit (int): The maximum number of posts to retrieve (default 5).
            mode (str): The sorting mode to use (default 'top').
            time (str): The time period to retrieve posts from (default 'year').

        Returns:
            A dictionary containing the response data from the API.

        Raises:
            requests.HTTPError: If the request to the API fails.
        """
        print('> fetching posts...')
        if not self.token:
            self.fetch_token()

        headers = {
            **self.headers,
            'Authorization': f'bearer {self.token}',
        }
        params = {
            'limit': limit,
        }
        after = ''
        current_date = utils.str_to_datetime(start_date)
        end_date = utils.str_to_datetime(end_date)
        posts = []

        while current_date > end_date:
            url = f'{self.BASE_URL}r/{subreddit}/{mode}?after={after}'
            print(f'> fetching posts from {url}...')
            response = requests.get(url, params=params, headers=headers)
            response_data = response.json()['data']

            for post in response_data['children']:
                post = post['data']
                created_utc = utils.utc_to_date(post['created_utc'])

                posts.append({
                    'title': post['title'].lower(),
                    'selftext': post['selftext'].lower(),
                    'ups': post['ups'],
                    'downs': post['downs'],
                    'link_flair_text': post['link_flair_text'],
                    'upvote_ratio': post['upvote_ratio'],
                    'num_comments': post['num_comments'],
                    'created_utc': created_utc,
                    'url': post['url'],
                    'permalink': post['permalink'],
                })

            print(current_date)
            current_date = utils.str_to_datetime(created_utc)

            if after == response_data['after']:
                break

            after = response_data['after']

        print('> done!')

        return posts

    @staticmethod
    def parse_data(posts: list) -> None:
        """
        Parses and returns data from a Reddit API response.

        Parameters:
            data (dict): The JSON data returned from a Reddit API response.

        Returns:
            A dictionary containing the parsed data.
        """
        utils.data_to_csv(posts)


if __name__ == '__main__':
    api = Reddit()
    data = api.fetch_posts(
        'conversas', start_date='01-03-23', end_date='01-03-22', limit=100)
    api.parse_data(data)
