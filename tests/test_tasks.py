from invoke import Context
import pytest
from unittest.mock import patch
import sys
from io import StringIO
import re
import docker

# Import the tasks
from tasks import help, hello, netspeed, dockerinfo, dockertest

@pytest.fixture
def invoke_context():
    return Context()

def test_help(invoke_context):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        help(invoke_context)
        output = fake_out.getvalue().strip()
        assert re.search(r'Tool Box', output)

def test_hello_default(invoke_context):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        hello(invoke_context)
        output = fake_out.getvalue().strip()
        assert output == "Hello world!"

def test_netspeed(invoke_context):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        netspeed(invoke_context)
        output = fake_out.getvalue().strip()
        # Assuming a successful speedtest would print ping, upload, and download speeds.
        assert re.search(r'PING', output)
        assert re.search(r'UPLOAD', output)
        assert re.search(r'DOWNLOAD', output)

def test_dockerinfo(invoke_context):
    # Mocking docker.from_env() function and its return value
    mock_client = docker.APIClient(version='auto')
    mock_info = {
        'Name': 'Mock Docker',
        'Architecture': 'x86_64',
        'OperatingSystem': 'Ubuntu 18.04.3 LTS',
        'ServerVersion': '20.10.8',
        'Images': 10,
        'Containers': 5,
        'ContainersRunning': 3,
    }
    with patch.object(docker, 'from_env', return_value=mock_client):
        with patch('docker.APIClient.info', return_value=mock_info):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                dockerinfo(invoke_context)
                output = fake_out.getvalue().strip()
                assert re.search(r'Mock Docker', output)
                assert re.search(r'x86_64', output)
                assert re.search(r'Ubuntu', output)
                assert re.search(r'20.10.8', output)
                # Similarly, assert for other info attributes

if __name__ == "__main__":
    pytest.main([sys.argv[0]])
