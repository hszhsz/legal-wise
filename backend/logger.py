import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("legal_wise")
handler = RotatingFileHandler(
    'app.log', maxBytes=10485760, backupCount=3
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)