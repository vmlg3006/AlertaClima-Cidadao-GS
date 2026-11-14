from unittest.mock import patch
import pytest
from app.api import criar_app
from app.validacao import validar

EXEMPLO = {'bairro':'Pinheiros','cidade':'São Paulo','latitude':-23.56,'longitude':-46.70,'limite_calor':32}


def test_validacao_correta():
    assert validar(EXEMPLO)['limite_calor'] == 32


@pytest.mark.parametrize('campo,valor', [('latitude', 999), ('limite_calor', 10), ('bairro', ''), ('longitude', 'nan')])
def test_validacao_rejeita(campo, valor):
    with pytest.raises(ValueError):
        validar({**EXEMPLO, campo:valor})


def test_get_lista():
    app = criar_app()
    with patch('app.api.database.listar', return_value=[]):
        resposta = app.test_client().get('/api/alertas')
    assert resposta.status_code == 200 and resposta.json == []


def test_post_cria():
    app = criar_app()
    with patch('app.api.database.criar', return_value=3):
        resposta = app.test_client().post('/api/alertas', json=EXEMPLO)
    assert resposta.status_code == 201 and resposta.json['id'] == 3


def test_put_atualiza():
    app = criar_app()
    with patch('app.api.database.atualizar', return_value=True):
        resposta = app.test_client().put('/api/alertas/3', json=EXEMPLO)
    assert resposta.status_code == 200


def test_delete_exclui():
    app = criar_app()
    with patch('app.api.database.excluir', return_value=True):
        resposta = app.test_client().delete('/api/alertas/3')
    assert resposta.status_code == 204


def test_clima_com_mock():
    app = criar_app()
    with patch('app.api.database.buscar', return_value=EXEMPLO), patch('app.api.consultar', return_value={'temperatura':34, 'horario':'2026-11-09T14:00'}):
        resposta = app.test_client().get('/api/alertas/3/clima')
    assert resposta.status_code == 200 and resposta.json['risco'] is True


def test_post_invalido():
    resposta = criar_app().test_client().post('/api/alertas', json={})
    assert resposta.status_code == 400
