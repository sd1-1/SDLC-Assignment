import sys
sys.path.append("..")
from user.user import *
import pytest


@pytest.mark.parametrize("list,expected", [
    ([1,2,3],0.8164965809277263),
    ([9, 10, 12, 13, 13, 13, 15, 15, 16, 16, 18, 22, 23, 24, 24, 25],5.11737237261468),
    ([1, 3, 4, 5, 7, 10, 12, 58], 17.528548142958105),
])

#this tests the mean functionality which is used for quiz results page

def test_std_dev(list,expected):   
    assert calculate_std_dev(list) == expected

