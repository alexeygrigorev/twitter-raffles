import os
from pathlib import Path


tweets_file = Path('tweets.txt')

twitter_api_key = os.getenv('TWITTER_API_KEY')
twitter_api_secret = os.getenv('TWITTER_API_SECRET')

top_winners = 10