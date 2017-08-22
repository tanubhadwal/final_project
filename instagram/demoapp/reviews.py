
import requests
import matplotlib.pyplot as plt
from paralleldots import set_api_key, get_api_key
# Setting your API key
set_api_key('qsw38mBRbE0gUAudAxCa4BriJkrLfvlyQBN9XTe6JPo')

 # Viewing your API key
get_api_key()


API= 'qsw38mBRbE0gUAudAxCa4BriJkrLfvlyQBN9XTe6JPo'

def Positive_Negative(media_id):
    request_url = ( 'media/%s/comments/?access_token=%s') % (media_id, API)
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