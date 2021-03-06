import Mysql
import pandas as pd
import csv
def postingIntotweets_has_users(content, account,userID,newCloneID, CloneTime,combineID):
    insetIntoTweetsHasUsers = ("INSERT into tweets_has_users"
                               "(userID, cloneID, cloneTime, tweets_tweetsID, tweets_twitterAccount,tweets_combinID)"
                               "VALUES(%s,%s,%s,%s,%s,%s)")
    sRow = (userID, newCloneID, CloneTime, content[1], account, combineID)
    Mysql.post(insetIntoTweetsHasUsers,sRow)

def fetchingFromtweets_has_users(userID, choosenAccount):
    chooesnAccount = "'"+ choosenAccount + "'"
    keyword = str(userID)
    query = ("select count(*), cloneID, tweets_twitterAccount,cloneTime from tweets_has_users where userID = " + keyword + " and tweets_twitterAccount = " + chooesnAccount + " group by cloneID, userID,tweets_twitterAccount,cloneTime ;")
    result = Mysql.fetch(query)
    return result

# retrieving the tags from database for a specific user
def fetchingAccounts(userID):
    keyword = str(userID)
    query = "select distinct(tweets_twitterAccount) from tweets_has_users where userID = " + keyword + ";"
    result = Mysql.fetch(query)
    return result

# check if the tweet is exist based on the userID and tweetID.
def checkingtweetsAndUserID(userID, tweetID):
    if int(userID):
        query = "select * from tweets_has_users where tweets_tweetsID = " + str(tweetID) + " and userID = " + str(userID) + " ;"
        content = Mysql.fetch(query)
        if len(content) > 0:
            return True
        else:
            return False


def fetchingTweet(CloneID):
    query = "select createdAt,text, category from tweets where combinID in (select tweets_combinID from tweets_has_users where cloneID = " + str(
        CloneID) + " ) ; "
    result = Mysql.fetch(query)
    return result

# This function retrives the tweets information for a user
def UserTweetsInformation(userID):
    query = "select count(tweets_tweetsID), tweets_twitterAccount from tweets_has_users where userid = "+ str(userID) + " group by tweets_twitterAccount;"
    return Mysql.fetch(query)


def checkAccount(Account, userID):
    query = "select * from tweets_has_users where userID = " + str(userID) + " and tweets_twitterAccount = '"+ Account +"';"
    print query
    account = Mysql.fetch(query)
    print(len(account))
    if len(account) == 0:
        return False
    else:
       return True

