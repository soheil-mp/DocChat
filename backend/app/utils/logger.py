import logging
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        filename=f'logs/docuchat_{datetime.now().strftime("%Y%m%d")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__) 