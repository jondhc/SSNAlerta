import os
import re
from time import gmtime, strftime

import tweepy

from secrets import *

# ====== Individual bot configuration ==========================
bot_username = 'SSNAlerta'
logfile_name = bot_username + ".log"
# ==============================================================

def get_tweets(screen_name):
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    # Initialize a list to hold all the tweets
    tweet_holder = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=2000)
    tweet_holder.extend(new_tweets)
    for tweet in tweet_holder:
        searchStr = r"Magnitud ([\d\.]+)"
        tweetStr = tweet.text
        magnitude_match = re.search(searchStr, tweetStr)
        if magnitude_match:
            magnitude = float(magnitude_match.group(1))
            if magnitude >= 4:
                print "Sismo mayor: " + tweet.text
            else:
                print "Menor a 4"





def create_tweet():
    """Create the text of the tweet you want to send."""
    # Replace this with your code!
    text = "Test..."
    return text


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    get_tweets("SismologicoMX")
    # tweet_text = create_tweet()
    # tweet(tweet_text)
