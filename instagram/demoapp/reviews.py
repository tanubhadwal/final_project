
import requests
import matplotlib.pyplot as plt
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = 'c6458215cb9e498288a86c4a2cf7516c'
BASE_URL = 'https://api.instagram.com/v1/'

def Positive_Negative(media_id):
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    count_of_positive_comments = 0
    count_of_negitive_comments = 0

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    count_of_negitive_comments = count_of_negitive_comments + 1
                else:
                    count_of_positive_comments = count_of_positive_comments + 1
        else:
            print 'There are no existing comments on the post!'
        #Ploting a pie chart
        labels = ['Postive Comments','Negitive Comments']
        numbers = [count_of_positive_comments,count_of_negitive_comments]
        explode = (0, 0.1)
        fig1, ax1 = plt.subplots()
        ax1.pie(numbers, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()

    else:
        print 'Status code other than 200 received!'