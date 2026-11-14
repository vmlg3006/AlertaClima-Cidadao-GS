import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logger = logging.getLogger('alertaclima')
logger.setLevel(logging.INFO)
if not logger.handlers:
    pasta = Path(__file__).resolve().parent.parent / 'logs'
    pasta.mkdir(exist_ok=True)
    handler = RotatingFileHandler(pasta / 'acoes.log', maxBytes=500000, backupCount=2, encoding='utf-8')
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(handler)
