import Mysql

def fetchFromUsers(content):
    try:
        usenameAndID = []
        keyword = '"' + content + '"'
        query = ("select * from users where username = " + keyword)
        result = Mysql.fetch(query)
        usenameAndID.append(result[0][0])
        usenameAndID.append(result[0][1])
        usenameAndID.append(result[0][2])
        usenameAndID.append(result[0][3])
        usenameAndID.append(result[0][4])
        usenameAndID.append(result[0][5])
        usenameAndID.append(result[0][6])
        return usenameAndID
    except:
        return None

def postinIntoUsers(content):
    # inserting into users:
    insertingIntoUser = ("INSERT into users"
                           "(userID, username,password,Usertype)"
                           "VALUES(%s,%s,%s,%s, %s)")
    userRow = (content[0], content[1], 'user', content[3])
    Mysql.post(insertingIntoUser, userRow)

def updatingAccount(userID, preffredAccount):
    updatingUsersAccount = ("UPDATE users set preferredAccount = %s  where userID = %s")
    values = (preffredAccount,userID)
    return Mysql.post(updatingUsersAccount, values)

def retriveUsers() :
    usersQuery = ("select * from users")
    return Mysql.fetch(usersQuery)

def retriveUsersByName(name) :
    name = "'" + name  +"'"
    if name == "'*'" :
        usersQuery = ("select * from users")
        return Mysql.fetch(usersQuery)
    else:
        usersQuery = ("select * from users where firstName = " + name)
        return Mysql.fetch(usersQuery)


def retrvieByUserID(ID) :
        usersQuery = ("select * from users where userID = " + ID + ";")
        return Mysql.fetch(usersQuery)

def updateuser(content):
    updateuser = ("update users set username = %s , firstname = %s, lastname= %s where userID = %s")
    infromation = (content[0], content[1], content[2],content[3])
    return (Mysql.post(updateuser, infromation))

def usersDashboard():
    query = "select users.userID , username, firstName, LastName, count(tweets_tweetsID) from users, tweets_has_users where tweets_has_users.userID = users.userID group by userID , username, firstName, LastName ;"
    return Mysql.fetch(query)

# checking if the username is exist ior not.
def checkingUsername(userName):
    queryForTheUsername = "select username from users where username = '"+userName+ "';"
    existence = Mysql.fetch(queryForTheUsername)
    if len(existence) == 0:
        return True
    else:
        return False

# returning a the max ID in the user table
def maxUserID():
    maxUserID = "select max(userID) from users ;"
    return (Mysql.fetch(maxUserID)[0][0])

# This method add a new user to the database.
def addingUsers(userName, firstName, lastName, email, password):
    if checkingUsername(userName) == False:
        return False
    else:
        newUserID = maxUserID() + 1
        userType = 'user'
        infromation = []
        infromation.append(newUserID)
        infromation.append(userName)
        infromation.append(password)
        infromation.append(userType)
        infromation.append(firstName)
        infromation.append(lastName)
        infromation.append(None)
        infromation.append(email)
        insertingIntoUser = ("INSERT into users"
                             "(userID, username,password,Usertype, firstName, lastName, preferredAccount, email)"
                             "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
        userRow = (infromation[0],infromation[1],infromation[2],infromation[3],infromation[4],infromation[5],infromation[6],infromation[7])
        Mysql.post(insertingIntoUser, userRow)
        return True
