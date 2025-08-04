import typing, requests

def numerical_sum(values: typing.Iterable[typing.Union[float, int]]) -> typing.Union[float, int]:
    total= 0
    for val in values:
        total += val
    return total

def get_weather(latitude: float = 0.0, longitude: float = 0.0, forecast_hours: int = 1) -> dict:
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&temperature_unit=fahrenheit&forecast_hours={forecast_hours}'

    response = requests.get(url)

    if response.status_code != 200:
        raise requests.HTTPError(f"Error receiving data from {url}: {response.status_code}")
    
    else:
        info = response.json()
        return info
