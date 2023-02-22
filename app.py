from flask import Flask, render_template, redirect, request, session,jsonify
from pymongo import MongoClient
import json
from bson.json_util import dumps
from hashlib import sha256

from user.user import *

client = MongoClient(
    "mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")  # connection to database as the admin

app = Flask(__name__)
app.secret_key = "abc123"  # required for session and used to encrpyt the cookies


@app.route('/')
def index():
    if loggedin():  # check whether user is already logged in using session
        return render_template('landing.html')
    else:

        # go back to the login page if they are not logged in
        return render_template('index.html')


@app.route('/landing')
def landing():
    if loggedin():
        return render_template('landing.html')
    else:
        return redirect("/")


@app.route('/quizresults', methods=['POST', 'GET'])
def quizresults():
    if loggedin():

        # get the form data that has been submitted
        module = request.form.get("module")
        if not module:
            return render_template('quizresults.html',selectedmodule="Select Module")

        quizmarks_list = []
        modulemarks_list = []
        # get the results from the sdlc collection with all the data
        for document in db.sdlc_records.find({}, {"_id": 0, "results": 1}):
            results = document['results']
            for result in results:
                if result['module'] == module:
                    quizmarks_list.append(result['quiz_mark'])
                    modulemarks_list.append(result['module_mark'])

        chart_data = [{"x": quizmarks_list[i], "y": modulemarks_list[i]} for i in range(
            len(quizmarks_list))]  # manipulate data in format to be able to be used in chart js

        std_quiz = round(calculate_std_dev(quizmarks_list),1)

        average_marks = round(calculate_mean(quizmarks_list))

        return render_template('quizresults.html', mean_results=average_marks, standard_deviation=std_quiz, data=chart_data,selectedmodule=module)
    else:
        return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('useremail')
    password = request.form.get('userpassword')
    if log_in(email,password):
        session['loggedIn'] = True
        return redirect("/landing")
    return redirect("/")


@app.route('/viewdata')
def viewdata():
    if loggedin():
        cursor = db.sdlc_records.find()  # gets all data in the sdlc_records collection
        list_cursor = list(cursor)
        json_data = dumps(list_cursor)
        return json.loads(json_data)
    else:
        return redirect("/")


@app.route('/uploadnewdata', methods=['POST'])
def uploadnewdata():
    if loggedin():
       
        student_id = int(request.form.get("student-id"))
        module = request.form.get("module")
        quiz_result = int(request.form.get("quiz-result"))
        
        modules = []


     
        

        record = json.loads(dumps(db.sdlc_records.find_one({'student_id' : student_id})))

        results = record["results"]
       
        for result in results:
            modules.append(result["module"])

        if module in modules:
                return "Quiz data already exists for that module, press back"    
       
        new_results = {
            "module": module,
            "quiz_mark": int(quiz_result),
            "module_mark": 0
        }
        results.append(new_results)
        filter = {
            "student_id": student_id
        }
        new_vals =    {
            "$set": { "results": results }
        }
        # update results
        db.sdlc_records.update_one(filter, new_vals)
        
        return "Success"





    else:
        return redirect("/")


@app.route('/signout')
def signout():
    return sign_out()


@app.route('/updateexistingdata', methods=['POST'])
def updateexistingdata():
    if loggedin():

        student_id = int(request.form.get("student-id"))
        module = request.form.get("module")
        quiz_result = int(request.form.get("quiz-result"))
        
        record = json.loads(dumps(db.sdlc_records.find_one({'student_id' : student_id})))
        results = record["results"]
        index_to_change = -1
        prev = {}
        # seach for result to change
        for index, res in enumerate(results):
            if res["module"] == module:
                index_to_change = index
                prev = res

        if index_to_change == -1:
            return "Didn't work, please press back and try"
        
        # update result by index
        results[index_to_change] = {
            "module": module,
            "quiz_mark": int(quiz_result),
            "module_mark": prev["module_mark"]
        }
        filter = {
            "student_id": student_id
        }
        new_vals =    {
            "$set": { "results": results }
        }
        # update results
        db.sdlc_records.update_one(filter, new_vals)
        
        return "Success"

@app.route('/deletedata', methods=['POST'])
def deletedata():
    if loggedin():
        student_id = int(request.form.get("student-id"))
        module = request.form.get("module")
        
        record = json.loads(dumps(db.sdlc_records.find_one({'student_id' : student_id})))
        results = record["results"]
        index_to_delete = -1
        prev = {}
        # seach for result to delete
        for index, res in enumerate(results):
            if res["module"] == module:
                index_to_delete = index
               

        if index_to_delete == -1:
            return "Didn't work, please press back and try"
        
     
        
        del results[index_to_delete]


        filter = {
            "student_id": student_id
        }
        new_vals =    {
            "$set": { "results": results }
        }

        db.sdlc_records.update_one(filter, new_vals)
        
        return "Success"        

       
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
