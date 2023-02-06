from flask import Flask, render_template,redirect,request, session,jsonify
from pymongo import MongoClient
from bson.json_util import dumps
client = MongoClient("mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")

app = Flask(__name__)
app.secret_key = "abc123"


@app.route('/')
def index():
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('landing.html')
    else:   
        return render_template('index.html')


@app.route('/landing')
def landing():
    print(session)
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('landing.html')
    else:
        return redirect("/")

@app.route('/usermanagement')
def usermanagement():
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('usermanagement.html')
    else:
        return redirect("/")
    


@app.route('/quizresults')
def quizresults():
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('quizresults.html')
    else:
        return redirect("/")
    

@app.route('/login', methods=['POST'])
def login():
    matching_record = db.users_records.find_one({
        "email": request.form.get("useremail")
    })
    if matching_record and request.form.get("userpassword") == matching_record["password"]:

        session['loggedIn'] = True
        return redirect("landing")
    return redirect("/")    

    
@app.route('/viewdata')
def viewdata():
    if 'loggedIn' in session and session['loggedIn']:
        cursor = db.sdlc_records.find()
        list_cursor = list(cursor)
        json_data = dumps(list_cursor)

        return json_data
    else:
        return redirect("/")
    

    

@app.route('/uploadnewdata',methods=['POST'])
def uploadnewdata():
    
    if 'loggedIn' in session and session['loggedIn']:
        data = request.form.get("file")
        db.sdlc_records.delete_many({})       
        
        return data

        

       
    else:
        return redirect("/")
    



@app.route('/signout')
def signout():
    session["loggedIn"] = False
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)