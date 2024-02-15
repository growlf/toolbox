# test_with_pytest.py
from unittest.mock import patch
from tasks import netspeed

def test_always_passes():
    assert True

# def test_always_fails():
#     assert False

# Test the netspeed task with mocked speedtest results
@patch('tasks.speedtest.Speedtest')
def test_netspeed(mock_speedtest, capsys):
    mock_speedtest.return_value.results.ping = 10
    mock_speedtest.return_value.results.upload = 1024 * 1024 * 50  # 50 Mbps
    mock_speedtest.return_value.results.download = 1024 * 1024 * 150  # 150 Mbps
    
    netspeed(None, verbose=0)
    captured = capsys.readouterr()
    assert "PING" in captured.out
    assert "UPLOAD" in captured.out
    assert "DOWNLOAD" in captured.out