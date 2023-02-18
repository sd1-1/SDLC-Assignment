
import sys
sys.path.append("..")
from flask import Flask
import json
from user.user import User
import pytest





@pytest.mark.parametrize("email,password,expected", [
    ("admin@wmg.com","admin",True),
    ("admin@wmg.com","wrongpassword", False),
    ("wrongemail@wmg.com","admin", False),
])

#this tests the login functionality for a correct and incorrect combination

def test_login(email,password,expected):   
    assert User.login(email,password) == expected

