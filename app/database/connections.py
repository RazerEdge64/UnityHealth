import mysql.connector

username = "root"
password = ""
cnx = mysql.connector.connect(user=username, password=password,
                              host='localhost',
                              database='unityhealth')

cursor = cnx.cursor()