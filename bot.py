import os
import time
import tweepy


from pymongo import Connection


class TwitterAPI:
    """
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    """
    def __init__(self):
        consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
        consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        """Send a tweet"""
        self.api.update_status(message)

    def mentions_timeline(self):
        return self.api.mentions_timeline()

if __name__ == "__main__":

    def mongo_conn():
      # Format: MONGOHQ_URL: mongodb://<user>:<pass>@<base_url>:<port>/<url_path>
      if os.environ.get('MONGOHQ_URL'):
          return Connection(os.environ['MONGOHQ_URL'])
      else:
          return Connection()

    twitter = TwitterAPI()
    db = mongo_conn().app22869812
    while True:
        # Get tweets here
        for tweet in twitter.mentions_timeline():
            if db.seenTweets.find({tweetId: tweet.id}) is None:
                twitter.tweet("Great! Create task for {0}:{1}".format(tweet.author.screen_name, tweet.entries['hashtags']));
            else:
                db.seenTweets.insert({tweetId: tweet.id})
        time.sleep(60)
