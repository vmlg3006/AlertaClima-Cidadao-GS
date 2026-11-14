import os
from dotenv import load_dotenv

load_dotenv()


def database_config():
    uri = os.getenv('MONGO_URI', '').strip()
    if not uri:
        raise RuntimeError('Configure MONGO_URI no arquivo .env.')
    return uri, os.getenv('MONGO_DB', 'alertaclima')
