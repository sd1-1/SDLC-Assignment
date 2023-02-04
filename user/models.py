from flask import Flask,jsonify,request,session,redirect
from app import db
from bson.json_util import dumps


class User:

    def login(self):
        matching_record = db.users_records.find_one({
            "email": request.form.get("useremail")
        })
        
        if matching_record and request.form.get("userpassword") == matching_record["password"]:
            return redirect("landing")

        return jsonify({"error": "invalid login"})


    def viewdata(self):
        cursor = db.sdlc_records.find()
        list_cursor = list(cursor)
        json_data = dumps(list_cursor)
        return json_data
