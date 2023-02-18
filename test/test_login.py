
import sys
sys.path.append("..")
from flask import Flask
import json
from user.user import User
import pytest

def test_login():
    assert User.login("admin@wmg.com","admin") == True