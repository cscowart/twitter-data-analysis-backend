import botometer
import collections
import re
from textblob import TextBlob
import tweepy
# from IPython import embed
# from boto.s3.connection import S3Connection
import os


class AuthinticatedAPI:
    def __init__(self):
        twitter_consumer_key = os.environ.get('twitter_consumer_key')
        twitter_consumer_secret_key = os.environ.get('twitter_consumer_secret_key')
        twitter_access_token = os.environ.get('twitter_access_token')
        twitter_access_token_secret = os.environ.get('twitter_access_token_secret')
        rapid_api_key = os.environ.get('rapid_api_key')
        twitter_app_auth = {
            'consumer_key': twitter_consumer_key,
            'consumer_secret': twitter_consumer_secret_key,
            'access_token': twitter_access_token,
            'access_token_secret': twitter_access_token_secret,
        }
        self.bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapid_api_key,
                          **twitter_app_auth)
        auth = tweepy.AppAuthHandler(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret_key)
        self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
        self.num = 100
        self.stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'amp']
        
    def clean_text_data(self, text):
        # remove urls, hashtags and punctuation
        text_no_urls = " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text).split())
        #  make all letters lowercase
        text_lowercase = text_no_urls.lower()
        return text_lowercase
    
    def word_counts(self, text_array):
        words_array = []
        for text in text_array:
            word_list = text.split()
            for word in word_list:
                if word in self.stopwords:
                    continue
                words_array.append(word)
        words_count = collections.Counter(words_array)
        return words_count.most_common(len(words_count))
    
    # Consider adding parameters to this function so that the user can add things to the processing of the text data, more interaction **********************
    def filter_tweets(self, status_array):
        # takes in a status array cleans the data and filters it down to 100 tweets, ignoring empty tweets (post-cleaning).
        text_array = []
        status_array_filtered = []
        retweet_array = []
        hashtag_array = []

        for status in status_array:
            # checks if 100 tweets has been reached
            if len(text_array) >= self.num:
                break
                
            # check if it is a retweet, if so add to the retweet list and continue on
            # need to add further modification to this processing based on what I want
            # currently ony looking for maybe who the user retweets, might add RT text for analysis
            if status.full_text.startswith('RT @'):
                # consider adding whole user profiles for visualizations purposes
                retweet_array.append(status.retweeted_status.user.screen_name)
                continue

            # go through the status and clean the text
            clean_text = self.clean_text_data(status.full_text)
            
            # ignore tweets that become empty after cleaning
            if clean_text == '':
                continue

            # keep adding to the final product until you reach 100 or you dont have tweets to go through
            if len(text_array) >= 100:
                break
            else:
                text_array.append(clean_text)
                # use status id to get oembed for diplay of tweet
                status_array_filtered.append(status.id)

        # generate RT counts
        retweet_user_counts = collections.Counter(retweet_array)
        

        # return the a clean text array of 100 tweets, matching array of statuses that were used, and array of users retweeted in the last 200 tweets
        return {'text_array':text_array, 'status_array':status_array_filtered, 'retweet_user_counts':retweet_user_counts.most_common(len(retweet_user_counts))}
        
    def collect_dates(self, status_array):
        # dates for all tweet activity
        dates_all = []
        # dates for activity not including RT's
        dates_no_rt = []
        for status in status_array:
            dates_all.append(status.created_at)
            if not status.full_text.startswith('RT @'):
                dates_no_rt.append(status.created_at)

        return {'dates_all' :dates_all, 'dates_no_rt':dates_no_rt[:100]}


    def get_hashtags(self, status_array, search_term):
        hashtag_array = []
        count = 1
        for status in status_array:
            if count >= 100:
                break
            if not status.full_text.startswith('RT @'):
                count += 1
                for hashtag in status.entities['hashtags']:
                    # filter search term
                    if hashtag['text'] not in [search_term]:
                        hashtag_array.append(hashtag['text'])

        hashtag_counts = collections.Counter(hashtag_array)
        return hashtag_counts.most_common(len(hashtag_counts))
        
    def get_sentiment(self, text_array):
        sentiments = []
        for text in text_array:
            tweet_blob = TextBlob(text)
            sent = tweet_blob.sentiment
            sentiments.append({'polarity':sent.polarity, 'subjectivity':sent.subjectivity})
        return sentiments


    def get_user_bot_score(self, handle):
        result = self.bom.check_account(handle)
        return result

    def generate_data(self, status_array, search_term = ''):
        filtered_text_data = self.filter_tweets(status_array)
        tweets_dates = self.collect_dates(status_array)
        word_counts = self.word_counts(filtered_text_data['text_array'])
        hashtag_counts = self.get_hashtags(status_array, search_term)
        sentiments = self.get_sentiment(filtered_text_data['text_array'])
        # bot_score = self.get_user_bot_score(self.handle)
        return {
            'filtered_text_data':filtered_text_data, 
            'tweets_dates':tweets_dates, 
            'word_counts':word_counts, 
            'hashtag_counts':hashtag_counts,
            'sentiments':sentiments,
            # 'bot_score':bot_score,
            }

    # STRETCH GOAL
    # # Location Data
    # def get_location_data(self, location):
    #     self.location = location

    # Handle Data
    def get_handle_data(self, handle, num=200, retweets=True):
        # 200 tweets is the max for one call, this will be filtered down to 100
        self.handle = handle
        status_array = self.twitter_api.user_timeline(screen_name=handle, count = num, include_rts=retweets, tweet_mode='extended')
        return self.generate_data(status_array)

    def get_user_data(self, handle):
        try:
            response = self.twitter_api.get_user(screen_name=handle)
            result = response._json
        except:
            result = {'id':False}
        return result


    # STRETCH GOAL
    # # Trending Topic Data
    # def get_topic_data(self, topic):
    #     self.topic = topic


# test = AuthinticatedAPI()
# handle = test.get_user_data('realDonaldTrump')
# embed()