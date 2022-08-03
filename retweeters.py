import os
import json

from time import time
from pathlib import Path

import requests

import util


def get_retweeters(tweet_id, token):
    print(f'getting the retweeters for {tweet_id}...')

    url = 'https://api.twitter.com/1.1/statuses/retweets/%s.json?count=100' % tweet_id
    headers = {'Authorization': 'Bearer %s' % token}
    retweets_resp = requests.get(url, headers=headers)

    retweets = retweets_resp.json()

    retweeters = [{'name': r['user']['screen_name'], 'id': r['user']['id']} for r in retweets]

    return retweeters


def save_retweeters(tweet_id, token):
    print(f'saving the retweeters for {tweet_id}...')
    retweeters = get_retweeters(tweet_id, token)

    response = {
        'tweet': tweet_id,
        'retweeters': retweeters
    }

    ts = int(time())

    key = Path(f'{tweet_id}/{ts}.json')
    key.parent.mkdir(parents=True, exist_ok=True)

    with open(key, 'wt') as f_out:
        json.dump(response, f_out, indent=2)

    print('wrote to', key)


def main():    
    auth_token = util.get_twitter_auth_token()
    tweets = util.read_tweet_file()

    for _, tweet_id in tweets:
        print(f'processing {tweet_id}...')
        save_retweeters(tweet_id, auth_token)


if __name__ == '__main__':
    main()