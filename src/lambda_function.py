import os

import tweepy
from dotenv import load_dotenv

from tweet_module import choose_rails_article, get_popular_article, summary_tweet

load_dotenv(verbose=True)
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.environ.get("TWITTER_API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")


def post_tweet(tweet: str) -> None:
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_KEY_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    )

    client.create_tweet(text=tweet)


def lambda_handler():
    popular_artilces = get_popular_article()
    ai_article = choose_rails_article(popular_artilces)
    tweet = summary_tweet(ai_article)
    print(f"{tweet=}")

    post_tweet(tweet)


lambda_handler()