import tweepy
import api_credentials
import ast


#
# Creates an api that can be used to access twitter data
#
class TwitterAPI:

    def __init__(self):
        self.auth_handler = tweepy.auth.OAuthHandler(api_credentials.consumer_token, api_credentials.consumer_secret, 'http://127.0.0.1:8000/TimeToPost/result/')
        self.api = None

    def get_api_object(self, access_token, access_secret):
        self.auth_handler.set_access_token(access_token, access_secret)
        return tweepy.API(self.auth_handler)

    def get_api_object_from_verifier(self, oauth_verifier, request_token):
        oauth_verifier = oauth_verifier.encode('ascii', 'ignore')
        self.auth_handler.get_authorization_url()
        self.auth_handler.request_token = ast.literal_eval(request_token)
        self.auth_handler.get_access_token(oauth_verifier)
        return tweepy.API(self.auth_handler)
