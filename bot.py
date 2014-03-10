import os
import time
import tweepy
import requests
import json

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
    
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.volunteerbeat-v1+json'}
    login_payload = {'email': 'facebook@idreamz.net', 'password': 'codepathdemo'}
    print "Logging in..."
    r = requests.post("http://api.volunteerbeat.com/session", data=json.dumps(login_payload), headers=headers)
    print "Log in status: {0}".format(r.status_code)
    my_cookies = r.cookies

    # Log into our server.
    while True:
        # Get tweets here
        for tweet in twitter.mentions_timeline():
            if db.seenTweets.find({"tweetId": tweet.id}).count() == 0:
                task_payload = {
                    "description": "This is a simple task",
                    "details": "This is a lot more information about the task, this should only be displayed to volunteers who have been approved for the task",
                    "starts_at": "2014-02-18T08:43:30Z",
                    "location": {
                        "latitude": 40.22,
                        "longitude": -120.11
                    },
                "category_id": 1
                }
                r = requests.post("http://api.volunteerbeat.com/tasks", data=json.dumps(task_payload), cookies=my_cookies, headers=headers)
                db.seenTweets.insert({"tweetId": tweet.id})
                print "Status of request: {0}".format(r.status_code)
                print "Created task! {0}".format(r.json()['id'])
        time.sleep(60)
