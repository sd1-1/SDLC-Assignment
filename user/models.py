from flask import Flask, jsonify, request, session, redirect
from hashlib import sha256
from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")  # connection to database as the admin




class User():

    def login():
        matching_record = db.users_records.find_one({
            "email": request.form.get("useremail")
        })

        # hashing the password so it can be compared with the hash in the database
        password_hash = sha256(request.form.get(
            "userpassword").encode('utf-8')).hexdigest()

        if matching_record and password_hash == matching_record["password"]:

            session['loggedIn'] = True
            return redirect("landing")
        return redirect("/")

    def signout():
        # change session status to false when the signout button is clicked
        session["loggedIn"] = False
        return redirect("/")

    def loggedin():
        if 'loggedIn' in session and session['loggedIn']:
            return True


            
        
