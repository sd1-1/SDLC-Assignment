import sys
sys.path.append("..")
from user.user import *
import pytest


@pytest.mark.parametrize("list,expected", [
    ([1,2,3],2),
    ([9, 10, 12, 13, 13, 13, 15, 15, 16, 16, 18, 22, 23, 24, 24, 25],16.75),
    ([1, 3, 4, 5, 7, 10, 12, 58], 12.5),
])

#this tests the mean functionality which is used for quiz results page

def test_mean(list,expected):   
    assert calculate_mean(list) == expected

