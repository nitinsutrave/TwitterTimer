from django.shortcuts import render, redirect
from twitter_api import TwitterAPI
from .models import Users
import tweepy

import PostTimeCalculator


#
# The home page for the webapp
#
def index(request):
    return render(request, 'TimeToPost/index.html', {})


#
# The result page displaying the best time and day to post
#
def process(request):
    user_identifier = request.POST['user_identifier']
    user_identifier_type = request.POST['user_identifier_type']

    twitter_api = TwitterAPI()

    try:
        response = redirect('result')
        if user_identifier_type == "user_id":
            user = Users.objects.get(user_id=user_identifier)
            response.set_cookie('app_user_id', user_identifier)
        else:
            user = Users.objects.get(user_name=user_identifier)
            response.set_cookie('app_user_name', user_identifier)

        try:
            api = twitter_api.get_api_object(user.user_access_token, user.user_access_secret)
            response.set_cookie('app_access_token', user.user_access_token)
            response.set_cookie('app_access_secret', user.user_access_secret)
        except tweepy.TweepError:
            user.delete()
            print "Authentication failed. Redirecting user to relogin"
            redirect_url = twitter_api.auth_handler.get_authorization_url()
            request_token = twitter_api.auth_handler.request_token
            response = redirect(redirect_url)
            response.set_cookie('request_token', request_token)
            if user_identifier_type == "user_id":
                response.set_cookie('app_user_id', user_identifier)
            else:
                response.set_cookie('app_user_name', user_identifier)

        return response

    except Users.DoesNotExist:
        print "User not found in DB. Will redirect user to fetch verifier token"
        response = redirect(twitter_api.auth_handler.get_authorization_url())
        if user_identifier_type == "user_id":
            response.set_cookie('app_user_id', user_identifier)
        else:
            response.set_cookie('app_user_name', user_identifier)
        request_token = twitter_api.auth_handler.request_token
        response.set_cookie('request_token', request_token)

    return response


def result(request):

    twitter_api = TwitterAPI()

    if ('app_access_token' in request.COOKIES.keys()) or ('app_access_secret' in request.COOKIES.keys()):
        api = twitter_api.get_api_object(request.COOKIES.get('app_access_token'), request.COOKIES.get('app_access_secret'))
        user_id = api.me().id_str
    else:
        api = twitter_api.get_api_object_from_verifier(request.GET['oauth_verifier'], request.COOKIES.get('request_token'))

        user_access_token = twitter_api.auth_handler.access_token
        user_access_secret = twitter_api.auth_handler.access_token_secret
        user_id = api.me().id_str
        user_name = api.me().screen_name

        new_user_entry = Users(user_name=user_name, user_id=str(user_id), user_access_secret=user_access_secret, user_access_token=user_access_token)
        new_user_entry.save()

    calculated_value = PostTimeCalculator.calculate(user_id, api)

    best_time_to_post = calculated_value['best_time_to_post']
    best_day_to_post = calculated_value['best_day_to_post']

    return render(request, 'TimeToPost/result.html', {'best_time_to_post': best_time_to_post, 'best_day_to_post': best_day_to_post})
