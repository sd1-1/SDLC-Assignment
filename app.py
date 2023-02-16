from flask import Flask, render_template,redirect,request, session,jsonify
from pymongo import MongoClient
import json
from bson.json_util import dumps
from hashlib import sha256
import numpy as np

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
    


@app.route('/quizresults',methods=['POST'])
def quizresults():
    if 'loggedIn' in session and session['loggedIn']:


        module = request.form.get("module")
        print(module)


        marks_list = []
        for document in db.sdlc_records.find({},{ "_id": 0,"results": 1 }):
            results = document['results']
            print(results)
            for result in results:
                if result['module'] == module:

                    marks_list.append(result['quiz_mark'])
                
       
        std_quiz = np.std(marks_list)

        
        average_marks = round(sum(marks_list) / len(marks_list))
        
        return render_template('quizresults.html',mean_results=average_marks,standard_deviation=round(std_quiz))
    else:
        return redirect("/")
    

@app.route('/login', methods=['POST'])
def login():
    matching_record = db.users_records.find_one({
        "email": request.form.get("useremail")
    })

    password_hash = sha256(request.form.get("userpassword").encode('utf-8')).hexdigest()
    
    if matching_record and password_hash == matching_record["password"]:

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
        data = request.files['file']
        info = json.loads(data.read())
        db.sdlc_records.delete_many({})
        for student_data in info:      
            db.sdlc_records.insert_one(
                student_data
            ) 
        return "Success"

       
    else:
        return redirect("/")
    



@app.route('/signout')
def signout():
    session["loggedIn"] = False
    return redirect("/")


@app.route('/updateexistingdata', methods=['POST'])
def updateexistingdata():
    if 'loggedIn' in session and session['loggedIn']:
        
        print(request.files)
        data = request.files['files2']

        
        info = json.loads(data.read())

        filter = { 'student_id': info['student_id'] }
        
        newvalues = info 
        db.sdlc_records.replace_one(filter, newvalues)
        
        return "successfully updated existing data, please press back"
    else:   
        return redirect("/")


@app.route('/deletedata', methods=['POST'])
def deletedata():
    if 'loggedIn' in session and session['loggedIn']:
        
        print(request.files)
        data = request.files['files3']

        
        info = json.loads(data.read())

        filter = { 'student_id': info['student_id'] }
        
       
        db.sdlc_records.delete_one(filter)
        
        return "successfully deleted data, please press back"
    else:   
        return redirect("/")



    





if __name__ == "__main__":
    app.run(debug=True)