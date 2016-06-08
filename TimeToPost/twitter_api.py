import tweepy
import api_credentials


#
# Creates an api that can be used to access twitter data
#
class TwitterAPI:

    def __init__(self):
        auth_handler = tweepy.OAuthHandler(api_credentials.consumer_token, api_credentials.consumer_secret)
        auth_handler.set_access_token(api_credentials.access_token, api_credentials.access_secret)
        self.api = tweepy.API(auth_handler)
