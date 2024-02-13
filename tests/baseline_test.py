# test_with_pytest.py
import random

def test_always_passes():
    if random.randint(1,3) > 2:
        assert True
    else:
        assert False

# def test_always_fails():
#     assert False
