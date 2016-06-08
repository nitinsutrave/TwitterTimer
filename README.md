# TwitterTimer
Enter your Twitter User ID / User Name and get the best time for you to put up a post on Twitter

## Requirements
Tweepy (http://www.tweepy.org/)

Python 2.7 (https://www.python.org/downloads/)

Python Django (https://www.djangoproject.com/)

## How to Run Locally
1. Clone the Repository
2. Add a file TimeToPost/api_credentials.py and include the following in it:

  consumer_token = ''
  
  consumer_secret = ''
  
  access_token = ''
  
  access_secret = ''
  
3. Start the server using the command 'python manage.py runserver'
4. Access the page at http://127.0.0.1:8000/TimeToPost
