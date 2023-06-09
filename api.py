import pandas as pd
import requests

from datetime import datetime

import config
import utils


class Reddit:
    AUTH_URL = 'https://www.reddit.com/api/v1/access_token'
    BASE_URL = 'https://oauth.reddit.com/'

    def __init__(self):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.user_agent = 'PythonAPI/0.1'
        self.headers = {'User-Agent': self.user_agent}
        self.token = None

    def fetch_token(self) -> str:
        print('> fetching access token...')
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        data = {
            'grant_type': 'client_credentials',
        }
        response = requests.post('https://www.reddit.com/api/v1/access_token',
                                 auth=auth,
                                 data=data,
                                 headers=self.headers)
        self.token = response.json()['access_token']
        print('> access token fetched!')

    def fetch_posts(self,
                    subreddit,
                    start_date=datetime.now(),
                    end_date=datetime.now(),
                    limit=5,
                    mode='new') -> list:
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

        while current_date > end_date and after != None:
            url = f'{self.BASE_URL}r/{subreddit}/{mode}?after={after}'
            print(f'> fetching posts from {url}...')
            response = requests.get(url, params=params, headers=headers)
            response_data = response.json()['data']

            for post in response_data['children']:
                post = post['data']

                posts.append({
                    'title':
                    post['title'].lower(),
                    'author':
                    post['author'],
                    'selftext':
                    post['selftext'].lower(),
                    'ups':
                    post['ups'],
                    'downs':
                    post['downs'],
                    'link_flair_text':
                    post['link_flair_text'],
                    'upvote_ratio':
                    post['upvote_ratio'],
                    'num_comments':
                    post['num_comments'],
                    'timestamp':
                    utils.datetime_to_str(
                        utils.utc_to_datetime(post['created_utc'])),
                    'url':
                    post['url'],
                    'permalink':
                    post['permalink'],
                })

            current_date = utils.utc_to_datetime(post['created_utc'])
            after = response_data['after']

        print('> done!')

        utils.data_to_csv(posts)
        return posts


if __name__ == '__main__':
    api = Reddit()
    data = api.fetch_posts('AmizadeVirtual',
                           start_date='01-03-23',
                           end_date='01-03-22',
                           limit=100)
