import sys
sys.path.append("..")
from user.user import *
import pytest




@pytest.mark.parametrize("email,password,expected", [
    ("admin@wmg.com","admin",True),
    ("admin@wmg.com","wrongpassword", False),
    ("wrongemail@wmg.com","admin", False),
])

#this tests the login functionality for a correct and incorrect combination

def test_log_in(email,password,expected):   
    assert log_in(email,password) == expected

