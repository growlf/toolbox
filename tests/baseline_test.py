# test_with_pytest.py
import os
def test_always_passes():
    assert True

# def test_always_fails():
#     assert False

def test_proxy_environment_variables():
    assert 'http_proxy' in os.environ
    assert 'https_proxy' in os.environ