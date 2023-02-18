from flask import Flask, jsonify, request, session, redirect
from hashlib import sha256
from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")  # connection to database as the admin




class User():

    def login(email,password):
        matching_record = db.users_records.find_one({
            "email": email
        })

        # hashing the password so it can be compared with the hash in the database
        password_hash = sha256(password.encode('utf-8')).hexdigest()

        if matching_record and password_hash == matching_record["password"]:

            
            return True
        return False

    def signout():
        # change session status to false when the signout button is clicked
        session["loggedIn"] = False
        return redirect("/")

    def loggedin():
        if 'loggedIn' in session and session['loggedIn']:
            return True


            
        
