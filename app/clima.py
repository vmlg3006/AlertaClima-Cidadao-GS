import requests

URL = 'https://api.open-meteo.com/v1/forecast'


def consultar(latitude, longitude):
    # Consulta dados públicos; tempo limite impede que a aplicação fique travada.
    resposta = requests.get(URL, params={
        'latitude': float(latitude), 'longitude': float(longitude),
        'current': 'temperature_2m', 'timezone': 'auto'
    }, timeout=6)
    resposta.raise_for_status()
    dados = resposta.json()
    atual = dados.get('current', {})
    temperatura = atual.get('temperature_2m')
    if not isinstance(temperatura, (int, float)) or isinstance(temperatura, bool):
        raise ValueError('Resposta meteorológica inválida.')
    return {'temperatura': temperatura, 'horario': atual.get('time', '')}
