import Mysql
from sklearn.feature_extraction.text import TfidfVectorizer
import csv


def postintoTweets(content):
    insertingIntoTweets = ("INSERT into tweets"
                           "(createdAt, tweetsID,text,category,twitterAccount, combinID)"
                           "VALUES(%s,%s,%s,%s,%s,%s)")
    tweetRow = (content[0], content[1], content[2], content[3], content[4], content[5])
    Mysql.post(insertingIntoTweets, tweetRow)

def tweetSearch(text, account,cloneID):
    account = "'" + account + "'"
    searchForText = ("select createdAt, text, category from tweets where text like '% "+text+" %' and twitterAccount = "+ account +"and tweetsID in (select tweets_tweetsID from tweets_has_users where cloneID = "+ cloneID +");")
    return Mysql.fetch(searchForText)


def retriveByDate(account,userID, startDate, endDate):
    account = "'"+ account +"'"
    startDate = "'"+startDate+"'"
    endDate = "'"+ endDate +"'"
    tweetsBydatesQuery = "select createdAt, text, category from tweets where tweetsID in (select tweets_tweetsID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +") and createdAt between" + startDate + " and " + endDate
    return Mysql.fetch(tweetsBydatesQuery)

def retriveAlltweets(account,userID):
    account = "'" + account + "'"
    retrivingAlltweetsForAccount = "select createdAt, text, category from tweets where combinID in (select tweets_combinID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +")"
    return Mysql.fetch(retrivingAlltweetsForAccount)

# retriving the statstic for to view it in charts
def retrivingStatstic(twitterAccount):
    if twitterAccount is None:
        return None
    else:
        twitterAccount = "'" + twitterAccount + "'"
        retrivingStatistic = "select count(*), category  from tweets where twitterAccount = "+ twitterAccount + "group by category ;"
        return Mysql.fetch(retrivingStatistic)

def termFrequency(account,userID):
    if account is None:
        return None
    else:
        vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, min_df=3, stop_words='english', use_idf=True,
                                     token_pattern=u"\w{4,}", lowercase=True)
        account = "'" + account + "'"
        textForAccountandUser = "select text from tweets where tweetsID in (select tweets_tweetsID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +")"
        texts = Mysql.fetch(textForAccountandUser)
        if len(texts) != 0:
            container = []
            for text in texts:
                container.append(text[0])
            X = vectorizer.fit_transform(container)
            return sorted(vectorizer.vocabulary_.items(), reverse=True)
        else:
            print("Thre is no data")

# this method takes all the result into one file in order to download it later.
def wrtitngtweetsToAfile(text):
    finalRow = []
    firstrow = []
    firstrow.append('Created_at')
    firstrow.append('Text')
    firstrow.append('Category')
    finalRow.append(firstrow)
    for row in text:
            temprow = []
            temprow.append(row[0])
            temprow.append(row[1])
            temprow.append(row[2])
            finalRow.append(temprow)
    with open('resultFile.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(finalRow)

# retrive tweets from database by date and categgory:
def retriveByDateAndCate(account,userID, startDate, endDate, category):
    account = "'"+ account +"'"
    startDate = "'"+startDate+"'"
    endDate = "'"+ endDate +"'"
    print("category ", category)
    Cat = "'" + changingCategroy(category) + "'"
    # print(Cat)
    tweetsBydatesQuery = "select createdAt, text, category from tweets where tweetsID in (select tweets_tweetsID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +") and createdAt between" + startDate + " and " + endDate +" and category = " + str(Cat) + "; "
    print(tweetsBydatesQuery)
    return Mysql.fetch(tweetsBydatesQuery)


def changingCategroy(text):
    if (text == 'None'):
        text = "None"
    elif (text == 'Bug'):
        text = "B"
    elif (text == 'Feature request'):
        text = "F"
    elif (text == 'User experience'):
        text = "User experience"
    print(len(text), text)
    return text
#
# print(retriveByDateAndCate('@snapchatsupport',1, '2019-01-01', '2019-02-28', 'Bug'))