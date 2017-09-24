import os
import re
from time import gmtime, strftime

import tweepy
from tweepy.api import API

from secrets import *

bot_username = 'SSNAlerta'
logfile_name = bot_username + ".log"

# Twitter authentication
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)

# Parameters
screen_name = "SismologicoMX"
minMagnitude = 3
mwStr = r"Magnitud ([\d\.]+)"
latStr = r"Lat ([\d\.]+)"
lngStr = r"Lon ([\d\.]+)"


# Twitter Streaming
class TwitterStreaming(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or API()

    def on_status(self, status):
        if status.user.screen_name == screen_name:
            tweetStr = status.text
            magnitude_match = re.search(mwStr, tweetStr)
            if magnitude_match:
                magnitude = float(magnitude_match.group(1))
                if magnitude >= minMagnitude:
                    api.update_status(tweetStr)
                    print "Sismo mayor a " + str(minMagnitude) + " grados: " + tweetStr + " Su magnitud: " + str(
                        magnitude)


# Twitter Listening to all filtered tweets with the word SISMO
def twitStream():
    stream = tweepy.streaming.Stream(auth, TwitterStreaming())
    stream.filter(track=['SISMO'], languages=['es'])


def create_tweet():
    text = "Test"
    return text


def tweet(text):
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    # tweet_text = create_tweet()
    # tweet(tweet_text)
    twitStream()
