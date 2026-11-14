from functools import lru_cache
from pymongo import MongoClient, ReturnDocument
from app.config import database_config


@lru_cache(maxsize=1)
def banco():
    uri, nome = database_config()
    cliente = MongoClient(uri, serverSelectionTimeoutMS=6000)
    cliente.admin.command('ping')
    return cliente[nome]


def inicializar():
    banco().alertas.create_index('id', unique=True)


def _limpar(documento):
    if documento is None:
        return None
    return {chave: valor for chave, valor in documento.items() if chave != '_id'}


def listar():
    return [_limpar(item) for item in banco().alertas.find({}, {'_id': 0}).sort('id', -1).limit(100)]


def buscar(identificador):
    return _limpar(banco().alertas.find_one({'id': identificador}))


def criar(dados):
    contador = banco().contadores.find_one_and_update(
        {'_id': 'alertas'}, {'$inc': {'sequencia': 1}}, upsert=True,
        return_document=ReturnDocument.AFTER)
    identificador = contador['sequencia']
    banco().alertas.insert_one({'id': identificador, **dados})
    return identificador


def atualizar(identificador, dados):
    resultado = banco().alertas.update_one({'id': identificador}, {'$set': dados})
    return resultado.matched_count > 0


def excluir(identificador):
    resultado = banco().alertas.delete_one({'id': identificador})
    return resultado.deleted_count > 0
