# -*- coding: utf-8 -*-
import tweepy
import csv
import Mysql

# Twitter API credentials
consumer_key = "Kvu7hx11dVWfOS2Bth9Pfa3VR"
consumer_secret = "PYJIZAtbDJXAcMu6u27qrPHbIvz5tLFPBqoC6dFvGTdO6QQQtR"
access_token = "259892667-f0xQEhRuQLKcSDrYicDVmW40YjJOptoH8uVNu7rS"
access_secret = "uXhBSWkV0t0ptHzXlE2l58x52W8SoCXYbhwXzleQZZLqP"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# saving the tweets into CSV file :
def get_all_tweets(screen_name):
        search = tweepy.Cursor(api.search, q=screen_name, lang="en", tweet_mode='extended').items(200)
        with open('%s_tweets.csv' % screen_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["created_at", "id", "text", "source"])
            for tweet in search:
                at = tweet.created_at
                id = tweet.id
                text = noEmojis(tweet.full_text)
                temp = [at, id, text]
                writer.writerow(temp)
        pass


def noEmojis(text):
    returnString = ""
    for character in text:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString


# Saving the tweets into DB:
# def savingIntoDB(screen_name):
#     search = tweepy.Cursor(api.search, q=screen_name, lang="en",tweet_mode='extended').items(200)
#     Mysql.post(search)

def retriveOnly(screen_name):
    search = tweepy.Cursor(api.search, q=screen_name, lang="en",tweet_mode='extended').items(200)
    templist = []
    for tweet in search :
        at = tweet.created_at
        id = tweet.id
        text = noEmojis(tweet.full_text)
        templist.append([at, id, text])
    return templist

if __name__ == '__main__':
    # savingIntoDB("")

    get_all_tweets("@snapchatsupport")
