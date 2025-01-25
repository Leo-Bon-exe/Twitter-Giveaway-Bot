import tweepy
import time
import os

consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

client = tweepy.Client(bearer_token=bearer_token)

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

friends_to_tag = ['@Friend1', '@Friend2']

hashtag_or_word = 'Giveaway OR giveaway OR GIVEAWAY OR #giveaway OR "giving away"'


def get_unretweeted_tweets(hashtag_or_word, num_tweets):
    unretweeted_tweets = []

    while len(unretweeted_tweets) < num_tweets:
        response = client.search_recent_tweets(query=hashtag_or_word, max_results=100)
        if response.data:
            for tweet in response.data:
                unretweeted_tweets.append(tweet)

                if len(unretweeted_tweets) >= num_tweets:
                    break

    return unretweeted_tweets


tweets_to_process = get_unretweeted_tweets(hashtag_or_word, 50)

for tweet in tweets_to_process:
    try:

        api.create_favorite(tweet.id)
        print(f"Liked tweet: {tweet.text}")

        api.retweet(tweet.id)
        print(f"Retweeted tweet: {tweet.text}")

        api.create_friendship(tweet.author_id)
        print(f"Followed: {tweet.author_id}")

        reply = ""
        if "tag" in tweet.text.lower():
            reply += f"{' '.join(friends_to_tag)} "

        if "platform" in tweet.text.lower():
            reply += "PC"

        if reply:
            api.update_status(f"@{tweet.author_id} {reply}", in_reply_to_status_id=tweet.id)
            print(f"Replied with: {reply}")

        time.sleep(10)

    except tweepy.TweepyException as e:
        print(f"Error: {e}")
    except StopIteration:
        break
