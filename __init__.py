from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)
from loguru import logger
logger.disable('pybeamer')

version = '0.1.0'

from .client import Codebeamer
from .projects import Project

__all__ = [
	'Codebeamer',
	'Project',
]