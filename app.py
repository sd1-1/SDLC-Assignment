from flask import Flask, render_template,redirect,request
from pymongo import MongoClient
from user import models
client = MongoClient("mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/usermanagement')
def usermanagement():
    return render_template('usermanagement.html')


@app.route('/quizresults')
def quizresults():
    return render_template('quizresults.html')

@app.route('/login', methods=['POST'])
def login():
    user = models.User()
    return user.login()

    
@app.route('/viewdata')
def viewdata():
    user = models.User()
    return user.viewdata()
    



if __name__ == "__main__":
    app.run(debug=True)