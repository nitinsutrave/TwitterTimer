from django.shortcuts import render
import PostTimeCalculator


#
# The home page for the webapp
#
def index(request):
    return render(request, 'TimeToPost/index.html', {})


#
# The result page displaying the best time and day to post
#
def result(request):
    user_identifier = request.POST['user_identifier']
    user_identifier_type = request.POST['user_identifier_type']

    calculated_value = PostTimeCalculator.calculate(user_identifier, user_identifier_type)

    best_time_to_post = calculated_value['best_time_to_post']
    best_day_to_post = calculated_value['best_day_to_post']

    return render(request, 'TimeToPost/result.html', {'best_time_to_post': best_time_to_post, 'best_day_to_post': best_day_to_post})
