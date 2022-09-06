import sys
import json

from random import shuffle
from pathlib import Path

import util
import config


def read_all_retweeters(files):
    all_retweeters = {}

    for file in files:
        with file.open(encoding='utf8') as f_in:
            body = json.load(f_in)

        for line in body['retweeters']:
            screen_name = line['name']
            user_id = line['id']
            all_retweeters[user_id] = screen_name

        print('num_retweeters', len(all_retweeters))

    return all_retweeters


def main(remove=True):
    url = sys.argv[1]
    handle, tweet_id = util.parse_url(url)

    retweets_folder = Path(f'retweets/{tweet_id}/')
    if not retweets_folder.exists():
        print(f"{retweets_folder} doesn't exist, exiting...")
        return

    files = sorted(retweets_folder.glob('*.json'))
    retweeters = read_all_retweeters(files)
    print(retweeters)

    token = util.get_twitter_auth_token()
    folowers = util.get_twitter_followers(handle, token)

    valid_participants = list(retweeters.keys() & folowers)
    shuffle(valid_participants)

    top = config.top_winners
    winner_ids = valid_participants[:top]
    winners = [retweeters[i] for i in winner_ids]

    winners_file = Path(f'winners/{tweet_id}.txt')
    winners_file.parent.mkdir(parents=True, exist_ok=True)

    print('winners:')
    print()

    with winners_file.open('wt', encoding='utf8') as f_out:
        for winner in winners:
            f_out.write(f'@{winner}\n')
            print(f'@{winner}')

    if remove == True:
        for file in files:
            file.unlink()
        retweets_folder.rmdir()
    
    util.remove_from_file(tweet_id)


if __name__ == '__main__':
    main()

