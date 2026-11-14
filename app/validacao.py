import math


def validar(dados):
    if not isinstance(dados, dict):
        raise ValueError('Envie um objeto JSON.')
    campos = ('bairro', 'cidade', 'latitude', 'longitude', 'limite_calor')
    if any(campo not in dados for campo in campos):
        raise ValueError('Preencha todos os campos.')
    bairro, cidade = dados['bairro'], dados['cidade']
    if not all(isinstance(x, str) and 2 <= len(x.strip()) <= 80 for x in (bairro, cidade)):
        raise ValueError('Bairro e cidade devem ter entre 2 e 80 caracteres.')
    if any(any(ord(c) < 32 for c in x) for x in (bairro, cidade)):
        raise ValueError('Texto inválido.')
    try:
        if any(isinstance(dados[k], bool) for k in ('latitude', 'longitude', 'limite_calor')):
            raise ValueError()
        lat, lon, limite = (float(dados[k]) for k in ('latitude', 'longitude', 'limite_calor'))
    except (ValueError, TypeError, OverflowError):
        raise ValueError('Coordenadas e limite devem ser números.') from None
    if not all(math.isfinite(x) for x in (lat, lon, limite)):
        raise ValueError('Os números devem ser finitos.')
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError('Latitude ou longitude fora do intervalo.')
    if not (20 <= limite <= 50):
        raise ValueError('O limite de calor deve ficar entre 20 e 50 °C.')
    return {'bairro': bairro.strip(), 'cidade': cidade.strip(), 'latitude': lat,
            'longitude': lon, 'limite_calor': limite}
