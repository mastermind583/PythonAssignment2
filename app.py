# Name: Jacob Gregie
# FSUID: jcg19
# Due Date: 9/27/2021
# “The program in this file is the individual work of Jacob Gregie”

from flask import Flask, render_template, request
import sqlite3 as sql
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/enternew')
def new_review():
   return render_template('addReview.html')

@app.route('/searchrev')
def get_review():
   return render_template('getReviews.html')

@app.route('/addrev',methods = ['POST', 'GET'])
def addrev():
    if request.method == 'POST':
        try:
            un = request.form['Username']
            rs = request.form['Restaurant']
            fd = request.form['Food']
            sv = request.form['Service']
            am = request.form['Ambience']
            pr = request.form['Price']
            ov = request.form['Overall']
            rv = request.form['Review']
            rt = datetime.now()

            with sql.connect("reviewData.db") as con:
                cur = con.cursor()
                
                cur.execute("INSERT INTO Reviews (Username,Restaurant,ReviewTime,Rating,Review) VALUES (?,?,?,?,?)",(un,rs,rt,ov,rv) )
                cur.execute("INSERT INTO Ratings (Restaurant,Food,Service,Ambience,Price,Overall) VALUES (?,?,?,?,?,?)",(rs,fd,sv,am,pr,ov))

                con.commit()
        except:
            con.rollback()

        finally:
            return render_template("index.html")
            con.close()

@app.route('/getrev',methods = ['POST', 'GET'])
def getrev():
    if request.method == 'POST':

        #get user inputted string for restaurant, format it for the sql command
        rs = request.form['Restaurant']
        user_input = ("'" + rs + "'")

        con = sql.connect("reviewData.db")
        con.row_factory = sql.Row
        
        #only select rows for the restaurant that the user inputted
        cur = con.cursor()
        cur.execute("SELECT Username, Review, Rating FROM Reviews WHERE Restaurant = ?",(rs,))
        rows = cur.fetchall()

        return render_template("showReviews.html", restaurant = rs, rows = rows)

@app.route('/report')
def list():
   con = sql.connect("reviewData.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute('''
                SELECT Restaurant, AVG(Food) AS Food, AVG(Service) AS Service, AVG(Ambience) AS Ambience, 
                AVG(Price) AS Price, AVG(Overall) AS Overall FROM Ratings GROUP BY Restaurant 
                ORDER BY Overall DESC, Restaurant ASC LIMIT 10
              ''')

   rows = cur.fetchall()
   return render_template("showReport.html",rows = rows)

if __name__ == '__main__':
   app.run(host='0.0.0.0')