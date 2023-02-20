from flask import Flask, jsonify, request, session, redirect
from hashlib import sha256
from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://sdlcadmin:Apples123@cluster0.euazjbc.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database("sdlc_db")  # connection to database as the admin



def hash_password(password):
    return sha256(password.encode('utf-8')).hexdigest()



def log_in(email,password):   #finds the document inside the collection with the same email
    matching_record = db.users_records.find_one({
        "email": email
    })

    # hashing the password so it can be compared with the hash in the database
    password_hash = hash_password(password)

    if matching_record and password_hash == matching_record["password"]:

        
        return True
    return False

def sign_out():
    # change session status to false when the signout button is clicked
    session["loggedIn"] = False
    return redirect("/")


def calculate_mean(list): # calculates mean from a list
    return sum(list) / len(list)


def loggedin():
    if 'loggedIn' in session and session['loggedIn']:
        return True

def calculate_std_dev(list): #this function calculates the standard deviation of a list
    mean = calculate_mean(list)
    n = len(list)
    mean = calculate_mean(list)
    sum_sq = sum(i * i for i in list)
    return (sum_sq / n - mean * mean) ** 0.5



        
a = hash_password("admin")

print(a)