import time

import requests
import config


def get_twitter_auth_token(
        key=config.twitter_api_key,
        secret=config.twitter_api_secret):
    print('getting the token...')

    auth_url = "https://api.twitter.com/oauth2/token"
    data = {'grant_type': 'client_credentials'}
    auth_resp = requests.post(auth_url, auth=(key, secret), data=data)
    token = auth_resp.json()['access_token']

    return token


def get_twitter_followers(handle, auth_token):
    headers = {'Authorization': 'Bearer %s' % auth_token}

    all_followers = set()

    next_cursor = -1

    while next_cursor != 0:
        followers_url = 'https://api.twitter.com/1.1/followers/ids.json?cursor=%s&' + \
                    'screen_name=%s&count=5000'
        followers_url = followers_url % (next_cursor, handle)

        followers_resp = requests.get(followers_url, headers=headers).json()
        print(followers_resp)
        followers_list = followers_resp['ids']

        all_followers.update(followers_list)
        print('num_followers', len(all_followers))
        
        next_cursor = followers_resp['next_cursor']
        print('next_cursor =', next_cursor)
        time.sleep(1)

    return all_followers


def read_tweet_file(tweets_file=config.tweets_file):
    with open(tweets_file, 'rt', encoding='utf8') as f_in:
        lines = []

        for line in f_in:
            line = line.strip()
            if line == '':
                continue

            print(line)
            handle, tweet_id = line.split(',')
            lines.append((handle, tweet_id))

        return lines


def append_to_file(handle, tweet_id, tweets_file=config.tweets_file):
    with open(tweets_file, 'at', encoding='utf8') as f_out:
        f_out.write(f'{handle},{tweet_id}\n')


def remove_from_file(tweet_id_to_delete, tweets_file=config.tweets_file):
    lines = read_tweet_file(tweets_file)

    with open(tweets_file, 'wt', encoding='utf8') as f_out:
        for handle, tweet_id in lines:
            if tweet_id == tweet_id_to_delete:
                continue 
            f_out.write(f'{handle},{tweet_id}\n')


def parse_url(url):
    tokens = url.split('/')
    handle = tokens[-3]
    tweet_id = tokens[-1]
    return handle, tweet_id