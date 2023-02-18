
import sys
sys.path.append("..")
from flask import Flask
import json
from user.user import User
import pytest

#this tests the login functionality for a correct and incorrect combination

def test_login():   
    assert User.login("admin@wmg.com","admin") == True

def test_login_incorrect():
    assert User.login("admin@wmg.com","wrongpassword") == False