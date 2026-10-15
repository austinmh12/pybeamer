from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)
from loguru import logger
logger.disable('pybeamer')

version = '0.0.1'

from .codebeamer import Codebeamer
from .models import *