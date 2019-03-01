import retriveData
import Mysql
import NaiveBayes
import tweetsTable
import tweets_has_users
import datetime
import re

# retriving new tweets:
def retriveAndclassifying(screen_name):
    tweets = retriveData.retriveOnly(screen_name)
    return tweets

# building the model based on the collected data set:
def buildingThemodel():
    DTModel = NaiveBayes.DecsionTree()
    return DTModel

# cloning the new tweets then classify them one by one:
def clssifingNewTweets(screen_name,userID):
    # generating a combineID:
    combineID = chckingForCombinID()

    # generating Cloning time:
    CloneTime = datetime.datetime.now()

    # retrieving from twitter:
    NewTweets = retriveAndclassifying(screen_name)

    # generating CloneID:
    newCloneID = chckingForCloneID()

    # building the model for the prediction :
    prediction = buildingThemodel()
    for count in range(len(NewTweets)):
        # cleanText = noEmojis(NewTweets[count][2])
        cleanText = re.sub(r"http\S+", "", noEmojis(NewTweets[count][2]))
        OneTweetText = NaiveBayes.vectorizer.transform([cleanText])
        category = prediction.predict(OneTweetText)
        if not tweets_has_users.checkingtweetsAndUserID(userID, NewTweets[count][1]):
            contnent = [NewTweets[count][0], NewTweets[count][1], str(cleanText), transforming(category),screen_name, combineID ]
            tweetsTable.postintoTweets(contnent)
            tweets_has_users.postingIntotweets_has_users(contnent,screen_name,userID,newCloneID,CloneTime, combineID)


def chckingForCloneID():
    query = ("select max(cloneID) from tweets_has_users ;")
    bigestCloneID = Mysql.fetch(query)
    if bigestCloneID[0][0] is None:
        return 1
    else:
        return bigestCloneID[0][0]+1

def chckingForCombinID():
    query = ("select max(combinID) from tweets ;")
    bigestCombinID = Mysql.fetch(query)
    if bigestCombinID[0][0] is None:
        return 1
    else:
        return bigestCombinID[0][0]+1

# changing the type of categroy:
def transforming(category):
    if(category == ['F']):
        category = "F"
    elif (category == ['None']):
        category = "None"
    elif (category == ['B']):
        category = "B"
    elif (category == ['U']):
        category = "U"
    return category

#cleaning the text from the emojis:
def noEmojis(text):
    returnString = ""
    for character in text:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString

# This method return the new tweets only:
# def printR():
#     print("hello")
