import os
import tweets_has_users
import retrivingClassifying as DataRetrival
import usersTable
import tweetsTable
from flask import Flask, render_template, request, redirect, session, flash, send_file
import csv
import StringIO
from flask import Flask, stream_with_context
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response


app = Flask(__name__)

@app.route('/')
def dex():
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", Account = session['defualtAccount'], Name = session['Name'], usertype=session['Usertype'], data = session['statstic'], data2 = session['statstic2'],users = session['allUsers'])

@app.route('/login', methods=['POST','GET'])
def login():
    if len(request.form) != 0:
        username = request.form['username']
        userRow = usersTable.fetchFromUsers(username)
        if userRow is not None:
            session['userID'] = userRow[0]
            session['username'] = userRow[1]
            session['defualtAccount'] = userRow[6]
            session['Usertype'] = userRow[3]
            session['Name'] = userRow[4]
            session['LName'] = userRow[5]
            session['Accounts'] = tweets_has_users.fetchingAccounts(session['userID'])
            if userRow[2] == request.form['password']:
                session['allUsers'] = usersTable.usersDashboard()
                session['statstic'] = tweetsTable.retrivingStatstic(session['defualtAccount'])
                session['statstic2'] = tweetsTable.termFrequency(session['defualtAccount'],session['userID'])
                return render_template('dashboard.html', Name=session['Name'], Account=session['defualtAccount'], usertype=session['Usertype'], data= session['statstic'], data2 = session['statstic2'],users = session['allUsers'])
            else:
                session.clear()
                return render_template('login.html', wrongUsername='wrong username or password')
        else:
            return render_template('login.html',wrongUsername='wrong username or password')
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return dex()

@app.route('/analyzing', methods=['POST', 'GET'])
def analyzing():
    if len(session) != 0:
        assoiateTable = tweets_has_users.fetchingFromtweets_has_users(session['userID'],session['defualtAccount'])
        return render_template("analyzing.html", assoiateTable = assoiateTable , Name = session['Name'], Account=session['defualtAccount'],usertype=session['Usertype'])
    else:
        return render_template('404.html')

@app.route('/setting')
def setting():
    if len(session) != 0:
        return render_template("Setting.html", Name = session['Name'], Account=session['defualtAccount'],usertype=session['Usertype'])
    else:
        return render_template('404.html')

@app.route('/accounts')
def accounts():
    if len(session) != 0:
        return render_template("Accounts.html", Accounts = session['Accounts'], Name = session['Name'], Account=session['defualtAccount'],usertype=session['Usertype'])
    else:
        return render_template('404.html')

@app.route('/accounts', methods=['POST','GET'])
def newAccount():
    if len(session) != 0:
        twitterAccount = request.form['twitterAccount']
        if twitterAccount is not None:
            DataRetrival.clssifingNewTweets(twitterAccount, session['userID'])
            session['Accounts'] = tweets_has_users.fetchingAccounts(session['userID'])
            return render_template("Accounts.html", Accounts = session['Accounts'], Name = session['Name'],Account=session['defualtAccount'],usertype=session['Usertype'])
        else:
            return render_template("Accounts.html", Accounts = session['Accounts'],Account=session['defualtAccount'],usertype=session['Usertype'])
    else:
        return render_template('404.html')

@app.route('/chooseAccount', methods=['POST','GET'])
def chooseAccount():
    session['defualtAccount'] = request.form['choosenAccount']
    usersTable.updatingAccount(session['userID'],session['defualtAccount'])
    session['statstic'] = tweetsTable.retrivingStatstic(session['defualtAccount'])
    session['statstic2'] = tweetsTable.termFrequency(session['defualtAccount'], session['userID'])
    return render_template("Accounts.html", Accounts = session['Accounts'], Name = session['Name'],Account=session['defualtAccount'],usertype=session['Usertype'])


@app.route('/result', methods=['POST','GET'])
def result():
    session['CloneID'] = request.args.get('cloneID')
    texts = tweets_has_users.fetchingTweet(session['CloneID'])
    tweetsTable.wrtitngtweetsToAfile(texts)
    return render_template('result.html', texts=texts, Name=session['Name'], Account=session['defualtAccount'],usertype=session['Usertype'])

@app.route("/Users")
def Users():
    if session['Usertype'] == 'Admin':
        users = usersTable.retriveUsers()
        return render_template('editUsers.html', users=users,usertype=session['Usertype'])
    else:
        return render_template("dashboard.html", data = session['statstic'])

@app.route('/retriveAccount', methods=['POST','GET'])
def retriveAccount():
     firstName = request.form['firstName']
     users = usersTable.retriveUsersByName(firstName)
     return render_template("editUsers.html", users=users,usertype=session['Usertype'])

@app.route('/retriveAllAccount', methods=['POST','GET'])
def retriveAllAccount():
     users = usersTable.retriveUsersByName("*")
     return render_template("editUsers.html", users=users,usertype=session['Usertype'])

@app.route('/moreUserDetails', methods=['POST','GET'])
def moreUserDetails():
    ID= request.args.get('UserID')
    UserInformation = usersTable.retrvieByUserID(ID)
    return render_template('editUsers2.html', UserInformation = UserInformation, usertype=session['Usertype'],Account=session['defualtAccount'])

@app.route('/updateUser', methods=['POST','GET'])
def updateUser():
    content = []
    content.append(request.form['username'])
    content.append(request.form['firstName'])
    content.append(request.form['lastName'])
    content.append(request.form['userID'])
    usersTable.updateuser(content)
    UserInformation = usersTable.retrvieByUserID(content[3])
    return render_template('editUsers2.html',  Accounts = session['Accounts'], UserInformation = UserInformation, usertype=session['Usertype'])

# This function retrive the data based on the cloneID and the text
@app.route('/searchtext', methods=['POST','GET'])
def searchtext():
    keyword = request.form['search']
    texts = tweetsTable.tweetSearch(keyword, session['defualtAccount'], session['CloneID'])
    tweetsTable.wrtitngtweetsToAfile(texts)
    return render_template('result.html',  Accounts = session['Accounts'], usertype=session['Usertype'], texts=texts)

# This method Do cloning for account
@app.route('/retriveMore', methods=['POST','GET'])
def retriveMore():
    DataRetrival.clssifingNewTweets(session['defualtAccount'], session['userID'])
    assoiateTable = tweets_has_users.fetchingFromtweets_has_users(session['userID'], session['defualtAccount'])
    return render_template("analyzing.html", Accounts = session['Accounts'],Account=session['defualtAccount'],usertype=session['Usertype'],assoiateTable = assoiateTable , Name = session['Name'])


# this method retrive the tweets based on the date and the account name:
@app.route('/retriveBasedOnDate', methods=['POST','GET'])
def retriveBasedOnDate():
    startDate = request.form['startDate']
    print(startDate)
    endDate = request.form['endDate']
    print(endDate)
    tweetsType =  request.form['categroyName']
    print(tweetsType)
    if tweetsType == 'All':
        texts = tweetsTable.retriveByDate(session['defualtAccount'],session['userID'], startDate, endDate )
    else :
        texts =tweetsTable.retriveByDateAndCate(session['defualtAccount'],session['userID'], startDate, endDate, tweetsType)
    tweetsTable.wrtitngtweetsToAfile(texts)
    return render_template('result.html', texts=texts, Name=session['Name'], Account=session['defualtAccount'],
                           usertype=session['Usertype'])

# retriving all tweets based on userID and twitter account
@app.route('/retriveAlltweets', methods=['POST','GET'])
def retriveAlltweets():
    texts = tweetsTable.retriveAlltweets(session['defualtAccount'], session['userID'])
    tweetsTable.wrtitngtweetsToAfile(texts)
    return render_template('result.html', texts=texts, Name=session['Name'], Account=session['defualtAccount'],
                           usertype=session['Usertype'])

@app.route('/myInfo', methods=['POST','GET'])
def myInfo():
    ID = session['userID']
    UserInformation = usersTable.retrvieByUserID(str(ID))
    return render_template('editUsers2.html', UserInformation = UserInformation, usertype=session['Usertype'],Account=session['defualtAccount'])

# downloading labled data:
@app.route('/Dowanload', methods=['POST','GET'])
def Dowanload():
    def generate():
        # reading form the file and save the values in a list.
        leabledFile = []
        with open('resultFile.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            leabledFile.append(list(reader))

        # creating an object of StringIO.
        data = StringIO.StringIO()
        w = csv.writer(data)

        # Saving the values in the object
        for texts in leabledFile:
            for row in texts:
                w.writerow(row)
                yield data.getvalue()
                data.seek(0)
                data.truncate(0)
        # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='results.csv')
    return Response(
            stream_with_context(generate()),
            mimetype='text/csv', headers=headers
        )

@app.route('/retriveAllAccountInDashboard', methods=['POST','GET'])
def retriveAllAccountInDashboard():
    return render_template('dashboard.html', Name=session['Name'], Account=session['defualtAccount'],
                           usertype=session['Usertype'], data=session['statstic'], data2=session['statstic2'],
                           users=session['allUsers'])


@app.route('/usersAccountsandTweets', methods=['POST','GET'])
def usersAccountsandTweets():
    userID = request.args.get('UserID')
    session['userTweetsinforamtionID'] = userID
    AccountsInformation = tweets_has_users.UserTweetsInformation(userID)
    return render_template('userTweetsAccounts.html', Name=session['Name'], Account=session['defualtAccount'],
                           usertype=session['Usertype'],
                           tweetsInformation = AccountsInformation)

@app.route('/usersAccountsandTweetsresult', methods=['POST','GET'])
def usersAccountsandTweetsresult():
    accountname = request.args.get('info')
    session['accountNametoDownload'] = accountname
    texts = tweetsTable.retriveAlltweets(session['accountNametoDownload'], session['userTweetsinforamtionID'])
    tweetsTable.wrtitngtweetsToAfile(texts)
    return render_template('result.html', texts=texts, Name=session['Name'], Account=session['defualtAccount'],
                           usertype=session['Usertype'])


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.debug = True
    app.run()
