import sys
import util


def main():
    url = sys.argv[1]
    new_handle, new_tweet_id = util.parse_url(url)

    tweets = util.read_tweet_file()

    for _, tweet_id in tweets:
        if tweet_id == new_tweet_id:
            print(f'{tweet_id} is already added, exiting...')
            return

    util.append_to_file(new_handle, new_tweet_id)


if __name__ == '__main__':
    main()

