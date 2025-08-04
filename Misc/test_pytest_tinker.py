import pytest_tinker, pytest, requests

@pytest.mark.parametrize('values, expected_sum', [
    ([], 0),
    ([1, 2], 3),
    ([1, 2, 3], 6),
    ([2, -2], 0),
    ([0, 1, 0.1], 1.1),
    ([1.5, -0.5], 1.0)
])

def test_numerical_sum(values, expected_sum):
    assert pytest_tinker.numerical_sum(values) == expected_sum

def test_numerical_sum_invalid_input():
    with pytest.raises(TypeError):
        pytest_tinker.numerical_sum("I am technically an iterable")  # type: ignore

# successful response
def test_get_weather_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'latitude': 0.0,
        'longitude': 0.0,
        'generationtime_ms': 0.030994415283203125,
        'utc_offset_seconds': 0,
        'timezone': 'GMT',
        'timezone_abbreviation': 'GMT',
        'elevation': 0.0,
        'hourly_units': {'time': 'iso8601', 'temperature_2m': '�F'},
        'hourly': {'time': ['2025-07-31T21:00'], 'temperature_2m': [74.6]}
    }

    mock_get = mocker.patch('requests.get', return_value=mock_response)

    data = pytest_tinker.get_weather(0.0, 0.0, 1)

    expected_data = {
        'latitude': 0.0,
        'longitude': 0.0,
        'generationtime_ms': 0.030994415283203125,
        'utc_offset_seconds': 0,
        'timezone': 'GMT',
        'timezone_abbreviation': 'GMT',
        'elevation': 0.0,
        'hourly_units': {'time': 'iso8601', 'temperature_2m': '�F'},
        'hourly': {'time': ['2025-07-31T21:00'], 'temperature_2m': [74.6]}
    }

    expected_url = (
        'https://api.open-meteo.com/v1/forecast?latitude=0.0&longitude=0.0'
        '&hourly=temperature_2m&temperature_unit=fahrenheit&forecast_hours=1'
    )

    assert data == expected_data
    mock_get.assert_called_once_with(expected_url)

# fail to get a response
def test_get_weather_fail_to_find(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {}

    mock_get = mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        pytest_tinker.get_weather()