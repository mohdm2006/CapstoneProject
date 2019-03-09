import Mysql
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import re


# inserting tweets into the tweets table.
def postintoTweets(content):
    insertingIntoTweets = ("INSERT into tweets"
                           "(createdAt, tweetsID,text,category,twitterAccount, combinID)"
                           "VALUES(%s,%s,%s,%s,%s,%s)")
    tweetRow = (content[0], content[1], content[2], content[3], content[4], content[5])
    Mysql.post(insertingIntoTweets, tweetRow)

# searching for a text in the database once the user want to specify a clone to search withen it .
def tweetSearch(text, account,cloneID):
    account = "'" + account + "'"
    searchForText = ("select createdAt, text, category from tweets where text like '% "+text+" %' and twitterAccount = "+ account +"and tweetsID in (select tweets_tweetsID from tweets_has_users where cloneID = "+ cloneID +");")
    return Mysql.fetch(searchForText)

# This method is for Admin when he searching for text in one of the users' tweets in the database
def tweetSearchForAnotherAccount(text, account, userID):
    account = "'" + account + "'"
    # searchForText = ("select createdAt, text, category from tweets where text like '% "+text+" %' and twitterAccount = "+ account +"and tweetsID in (select tweets_tweetsID from tweets_has_users where cloneID = "+ cloneID +");")
    searchForText = "select createdAt, text, category from tweets where combinID in (select tweets_combinID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +") and text like '% "+text+ " %' ;"
    return Mysql.fetch(searchForText)

# retriving tweets by dates, account and userID
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
        Allresult = []
        twitterAccount = "'" + twitterAccount + "'"

        retrivingStatisticB = "select count(*), category  from tweets where twitterAccount = "+ twitterAccount + " and  category= 'B' group by category order by category ;"
        if len(Mysql.fetch(retrivingStatisticB)) == 0:
            Allresult.append((0,'B'))
        else:
            Allresult.append(Mysql.fetch(retrivingStatisticB)[0])

        retrivingStatisticF = "select count(*), category  from tweets where twitterAccount = " + twitterAccount + " and category= 'F' group by category order by category ;"
        if len(Mysql.fetch(retrivingStatisticF)) == 0 :
            Allresult.append((0, 'F'))
        else:
            Allresult.append(Mysql.fetch(retrivingStatisticF)[0])

        retrivingStatisticNone = "select count(*), category  from tweets where twitterAccount = " + twitterAccount + " and category= 'None' group by category order by category ;"
        if len(Mysql.fetch(retrivingStatisticNone)) == 0:
            Allresult.append((0, 'None'))
        else:
            Allresult.append(Mysql.fetch(retrivingStatisticNone)[0])

        retrivingStatisticU = "select count(*), category  from tweets where twitterAccount = " + twitterAccount + " and category= 'U' group by category order by category ;"
        if len(Mysql.fetch(retrivingStatisticNone)) == 0:
            Allresult.append((0, 'U'))
        else:
            Allresult.append(Mysql.fetch(retrivingStatisticU)[0])

        return Allresult

    # this method find the most common words based on the userID, AccountName.
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
                tempVoc = []
                counter = 0
                for x in sorted(vectorizer.vocabulary_.items(), reverse=True):
                    if counter == 10:
                        break
                    tempVoc.append(x)
                    counter = counter +1
                return tempVoc
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
    Cat = "'" + changingCategroy(category) + "'"

    tweetsBydatesQuery = "select createdAt, text, category from tweets where tweetsID in (select tweets_tweetsID from tweets_has_users where userID = "+ str(userID) +" and tweets_twitterAccount ="+ account +") and createdAt between" + startDate + " and " + endDate +" and category = " + str(Cat) + "; "
    return Mysql.fetch(tweetsBydatesQuery)

# This method change the categories to a characters.
def changingCategroy(text):
    if (text == 'None'):
        text = "None"
    elif (text == 'Bug'):
        text = "B"
    elif (text == 'Feature request'):
        text = "F"
    elif (text == 'User experience'):
        text = "User experience"
    return text
#
# print(retriveByDateAndCate('@snapchatsupport',1, '2019-01-01', '2019-02-28', 'Bug'))

# finding all the matches and saving all the result tweets from the search into the file.
def searchText(text):
    resultOfSearch = []
    with open('orignalResult.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if re.search(" "+text+" ", row[1], re.IGNORECASE):
                    resultOfSearch.append(row)
    if len(resultOfSearch) == 0:
        return None
    else:
        wrtitngtweetsToAfile(resultOfSearch)
        return resultOfSearch

# writing another copy for the result in another file in order to retrive it later :
def writingIntoOrignalfile(texts):
    with open('orignalResult.csv', 'w') as writeFile2:
        writer = csv.writer(writeFile2)
        writer.writerows(texts)

# When the user refresh the result page all the orignal file will be written agian to the result file
# so, it can be downloaded.
def writingTheOrginalFileToresultFile(texts):
    with open('resultFile.csv', 'w') as writeFile2:
        writer = csv.writer(writeFile2)
        writer.writerows(texts)

# def fillingGapsInFirstgraph(statisticResultGraphOne):
#      values = []
#      if len(statisticResultGraphOne) == 4:
#          return statisticResultGraphOne
#      else:
#              values.append((0,'B'))
#              values.append((0,'F'))
#              values.append((0,'None'))
#              values.append((0,'U'))
#
#      print('last' , values)
#      print('statisticResultGraphOne ', statisticResultGraphOne)
#      # print('difference ', statisticResultGraphOne.difference(values))
#      # print(list(set(statisticResultGraphOne) - set(values)))
#          # if statisticResultGraphOne[0][1] == 'B'
#          #     values
#         # for value in statisticResultGraphOne:
#         #     if value[0][1] == 'B':
#         #         values.append((value[0][0]),(value[0][1]))
#         #     else
#
#
# #
# retrivingStatstic('@ubersupport')
# retrivingStatstic('@snapchatsupport')
# # retrivingStatstic('@googlemaps')
#
#
# # x = [(1, u'B'), (15, u'None'), (9, u'U')]
# # fillingGapsInFirstgraph(x)
# # retrivingStatstic('')

# termFrequency('@google',10)

termFrequency('@snapchatsupport',1)