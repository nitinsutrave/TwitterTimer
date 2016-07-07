from twitter_api import TwitterAPI
import datetime
import tweepy

#
# Convert the integer reprsentation of day to a readable string
#
def get_day_as_string(i):
    return {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }[i]


#
# Represent the time in 24 hours format
#
def get_time_as_string(max_valued_time):
    if max_valued_time < 10:
        return "0" + str(max_valued_time) + ":00"
    else:
        return str(max_valued_time) + ":00"


#
# Initialize an empty hash that will maintain the count of tweets per hour and per day
#
def init_tweet_counter_hash():
    #
    # Because that is how python deals with days of the week
    # days_of_week=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    #
    days_of_week = [0,         1,           2,          3,        4,          5,        6]

    hours_of_day = []
    for i in range(24):
        hours_of_day.append(i)

    tweet_counter_hash = {'day': {}, 'hour': {}}
    for day in days_of_week:
        tweet_counter_hash['day'][day] = 0

    for hour in hours_of_day:
        tweet_counter_hash['hour'][hour] = 0

    return tweet_counter_hash


#
# Used to filter tweets that were created in the last one week
#
def time_delimiter():
    return (datetime.datetime.now() - datetime.timedelta(weeks=1))


#
# Populate tweet_counter_hash with number of tweets by the
# user's followers in the last week
# as per time of post and day of post
#
def populate_tweet_counter_hash(followers_ids, api):
    tweet_counter_hash = init_tweet_counter_hash()
    one_week_back = time_delimiter()

    # Using only top 10 followers to keep up with time constraints
    followers_ids = followers_ids[0:10]

    #
    # Fetch the timeline of 100 posts for every follower and increment post count according to time/day
    #
    for followers_id in followers_ids:
        print "Doing follower: " + str(followers_id)
        try:
            timeline = api.user_timeline(id=followers_id, count=100)
        except tweepy.RateLimitError:
            print "*** RATE LIMIT EXCEEDED"
            break
        except tweepy.TweepError:
            print("Couldn't run for user " + str(followers_id))
            continue
        for post in timeline:
            if post.created_at < one_week_back:
                continue

            day_of_week = post.created_at.weekday()
            hour = post.created_at.hour

            tweet_counter_hash['day'][day_of_week] += 1
            tweet_counter_hash['hour'][hour] += 1

    return tweet_counter_hash


#
# Used if user id has been provided through the webapp
#
def calculate_from_user_id(user_identifier, api):
    followers_ids = api.followers_ids(id=user_identifier)
    return populate_tweet_counter_hash(followers_ids, api)


#
# Used if user name(screen name) has been provided through the webapp
#
def calculate_from_screen_name(user_identifier, api):
    followers_ids = api.followers_ids(screen_name=user_identifier)
    return populate_tweet_counter_hash(followers_ids, api)


#
# Determine the best time to post based on the calcualted follower post counts
#
def calculate_best_time_to_post(tweet_counter_hash):
    max_valued_time = 0
    max_value = 0
    for key in tweet_counter_hash['hour'].keys():
        if tweet_counter_hash['hour'][key] > max_value:
            max_value = tweet_counter_hash['hour'][key]
            max_valued_time = key
    return get_time_as_string(max_valued_time)


#
# Determine the best day to post based on the calcualted follower post counts
#
def calculate_best_day_to_post(tweet_counter_hash):
    max_valued_day = 0
    max_value = 0
    for key in tweet_counter_hash['day'].keys():
        if tweet_counter_hash['day'][key] > max_value:
            max_value = tweet_counter_hash['day'][key]
            max_valued_day = key
    return get_day_as_string(max_valued_day)


#
# Starting point for the calculation of best time and best day for a user to post
#
def calculate(user_id, api):
    tweet_counter_hash = calculate_from_user_id(user_id, api)

    print "The calculated hash is:"
    print tweet_counter_hash

    best_time_to_post = calculate_best_time_to_post(tweet_counter_hash)
    best_day_to_post = calculate_best_day_to_post(tweet_counter_hash)

    return {
        'best_time_to_post': best_time_to_post,
        'best_day_to_post': best_day_to_post
    }
