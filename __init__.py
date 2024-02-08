from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)
from loguru import logger
logger.disable('aerowiki')

version = '0.1.0'

__all__ = [
	
]