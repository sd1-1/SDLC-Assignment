import sys
sys.path.append("..")
from user.user import *
import pytest




@pytest.mark.parametrize("hash,expected", [
    ("password123","ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f"),
    ("admin","8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"),
    ("testing123","b822f1cd2dcfc685b47e83e3980289fd5d8e3ff3a82def24d7d1d68bb272eb32"),
])

#this tests the hash functionality which is used for the password inputted into the website

def test_hash(hash,expected):   
    assert hash_password(hash) == expected

