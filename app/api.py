from decimal import Decimal
import requests
from flask import Flask, jsonify, request, send_from_directory
from pymongo.errors import PyMongoError
from app import database
from app.clima import consultar
from app.logs import logger
from app.validacao import validar


def criar_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.config['MAX_CONTENT_LENGTH'] = 8192
    app.json.ensure_ascii = False

    @app.get('/')
    def pagina():
        return send_from_directory(app.static_folder, 'index.html')

    @app.get('/api/alertas')
    def listar_alertas():
        registros = database.listar()
        logger.info('LISTAR | sucesso')
        return jsonify([formatar(x) for x in registros]), 200

    @app.post('/api/alertas')
    def criar_alerta():
        dados = validar(request.get_json(silent=True))
        identificador = database.criar(dados)
        logger.info('CRIAR | id=%s | sucesso', identificador)
        return jsonify({'id': identificador, 'mensagem': 'Alerta criado.'}), 201

    @app.put('/api/alertas/<int:identificador>')
    def atualizar_alerta(identificador):
        dados = validar(request.get_json(silent=True))
        if not database.atualizar(identificador, dados):
            logger.info('ATUALIZAR | id=%s | nao_encontrado', identificador)
            return jsonify({'erro': 'Alerta não encontrado.'}), 404
        logger.info('ATUALIZAR | id=%s | sucesso', identificador)
        return jsonify({'mensagem': 'Alerta atualizado.'}), 200

    @app.delete('/api/alertas/<int:identificador>')
    def excluir_alerta(identificador):
        if not database.excluir(identificador):
            logger.info('EXCLUIR | id=%s | nao_encontrado', identificador)
            return jsonify({'erro': 'Alerta não encontrado.'}), 404
        logger.info('EXCLUIR | id=%s | sucesso', identificador)
        return '', 204

    @app.get('/api/alertas/<int:identificador>/clima')
    def clima_alerta(identificador):
        registro = database.buscar(identificador)
        if registro is None:
            return jsonify({'erro': 'Alerta não encontrado.'}), 404
        clima = consultar(registro['latitude'], registro['longitude'])
        limite = float(registro['limite_calor'])
        logger.info('CONSULTAR_CLIMA | id=%s | sucesso', identificador)
        return jsonify({**clima, 'limite_calor': limite,
                        'risco': clima['temperatura'] >= limite,
                        'aviso': 'Limite de calor atingido' if clima['temperatura'] >= limite else 'Abaixo do limite'}), 200

    @app.errorhandler(ValueError)
    def erro_validacao(erro):
        logger.warning('VALIDACAO | rejeitada')
        return jsonify({'erro': str(erro)}), 400

    @app.errorhandler(PyMongoError)
    def erro_banco(erro):
        logger.error('BANCO | falha | tipo=%s', type(erro).__name__)
        return jsonify({'erro': 'Serviço temporariamente indisponível.'}), 503

    @app.errorhandler(requests.RequestException)
    def erro_clima(erro):
        logger.warning('CLIMA | indisponivel | tipo=%s', type(erro).__name__)
        return jsonify({'erro': 'Não foi possível consultar o clima agora.'}), 502

    @app.errorhandler(413)
    def erro_tamanho(erro):
        return jsonify({'erro': 'Requisição muito grande.'}), 413

    @app.errorhandler(404)
    def erro_rota(erro):
        return jsonify({'erro': 'Rota não encontrada.'}), 404

    @app.errorhandler(Exception)
    def erro_inesperado(erro):
        logger.error('SISTEMA | erro_interno | tipo=%s', type(erro).__name__)
        return jsonify({'erro': 'Erro interno. Tente novamente.'}), 500

    return app


def formatar(registro):
    return {chave: float(valor) if isinstance(valor, Decimal) else valor
            for chave, valor in registro.items()}
