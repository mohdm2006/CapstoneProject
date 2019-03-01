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
