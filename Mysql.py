import sys, traceback
import datetime
import datetime
import mysql.connector
cnx = mysql.connector.connect(user='root', password='0148410545',
                              host='localhost',
                              database='capstone',charset='utf8mb4')

def fetch(query):
    cnx.connect()
    contnent = []
    mycursor = cnx.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    for x in myresult:
        contnent.append(x)
    cnx.close()
    return contnent

def post(query,row):
    cnx.connect()
    cursor = cnx.cursor()
    cursor.execute(query, row)
    cnx.commit()
    cursor.close()
    cnx.close()

def creatingAcloneID(cnx):
    firstCloneValues = 1
    lastID = cnx.execute("select ")


