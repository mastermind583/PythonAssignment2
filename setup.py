# Name: Jacob Gregie
# FSUID: jcg19
# Due Date: 9/27/2021
# “The program in this file is the individual work of Jacob Gregie”

import sqlite3

conn = sqlite3.connect('reviewData.db')
print ("Opened database successfully")

conn.execute('''
             CREATE TABLE Reviews (Username CHARACTER(40), Restaurant CHARACTER(50),
             ReviewTime DATETIME, Rating REAL, Review CHARACTER(500))
            ''')
print ("Table created successfully")

conn.execute('''
             CREATE TABLE Ratings (Restaurant CHARACTER(50), Food REAL, Service REAL,
             Ambience REAL, Price REAL, Overall REAL)
            ''')
print ("Table created successfully")

conn.close()