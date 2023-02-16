from flask import Flask, render_template,redirect,request, session,jsonify
from pymongo import MongoClient
import json
from bson.json_util import dumps
from hashlib import sha256
import numpy as np

client = MongoClient("mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db") #connection to database as the admin

app = Flask(__name__)
app.secret_key = "abc123" #required for session and used to encrpyt the cookies


@app.route('/')
def index():
    if 'loggedIn' in session and session['loggedIn']: #check whether user is already logged in using session
        return render_template('landing.html')
    else:   
        return render_template('index.html')  #go back to the login page if they are not logged in


@app.route('/landing')
def landing():
    
    if 'loggedIn' in session and session['loggedIn']:
        return render_template('landing.html')
    else:
        return redirect("/")




@app.route('/quizresults',methods=['POST','GET'])
def quizresults():
    if 'loggedIn' in session and session['loggedIn']:



        module = request.form.get("module")  #get the form data that has been submitted
        if not module:
                return render_template('quizresults.html')  
      


        quizmarks_list = []
        modulemarks_list = []
        for document in db.sdlc_records.find({},{ "_id": 0,"results": 1 }): #get the results from the sdlc collection with all the data
            results = document['results']
            for result in results:
                if result['module'] == module:
                    quizmarks_list.append(result['quiz_mark'])  
                    modulemarks_list.append(result['module_mark'])
        
        chart_data = [{ "x": quizmarks_list[i], "y": modulemarks_list[i]} for i in range(len(quizmarks_list))]

            
       
        std_quiz = round(np.std(quizmarks_list),1)

    
        average_marks = round(sum(quizmarks_list) / len(quizmarks_list))
        
        return render_template('quizresults.html',mean_results=average_marks,standard_deviation=std_quiz, data=chart_data)
    else:
        return redirect("/")
    

@app.route('/login', methods=['POST'])
def login():
    matching_record = db.users_records.find_one({
        "email": request.form.get("useremail")  
    })

    password_hash = sha256(request.form.get("userpassword").encode('utf-8')).hexdigest()  #hashing the password so it can be compared with the hash in the database
    
    if matching_record and password_hash == matching_record["password"]:

        session['loggedIn'] = True
        return redirect("landing")
    return redirect("/")    

    
@app.route('/viewdata')
def viewdata():
    if 'loggedIn' in session and session['loggedIn']:
        cursor = db.sdlc_records.find() #gets all data in the sdlc_records collection
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
        db.sdlc_records.delete_many({}) #delete everything before looping through each document and inserting it into the database
        for student_data in info:      
            db.sdlc_records.insert_one(
                student_data
            ) 
        return "Success"

       
    else:
        return redirect("/")
    



@app.route('/signout')
def signout():
    session["loggedIn"] = False #change session status to false when the signout button is clicked
    return redirect("/")


@app.route('/updateexistingdata', methods=['POST'])
def updateexistingdata():
    if 'loggedIn' in session and session['loggedIn']:
        
      
        data = request.files['files2']

        
        info = json.loads(data.read())

        filter = { 'student_id': info['student_id'] } #This enables us to update the matching document with the same student_id as inputted in the json
        
        newvalues = info 
        db.sdlc_records.replace_one(filter, newvalues)
        
        return "successfully updated existing data, please press back"
    else:   
        return redirect("/")


@app.route('/deletedata', methods=['POST'])
def deletedata():
    if 'loggedIn' in session and session['loggedIn']:
        
    
        data = request.files['files3']

        
        info = json.loads(data.read())

        filter = { 'student_id': info['student_id'] }
        
       
        db.sdlc_records.delete_one(filter)
        
        return "successfully deleted data, please press back"
    else:   
        return redirect("/")



    

if __name__ == "__main__":
    app.run(debug=True)