from loguru import logger
from math import ceil
from string import ascii_uppercase, ascii_lowercase

def loadable(func):
	"""Decorator for calling load on property getter functions. Class must have a 
	_loaded bool variable and a _load() function with no arguments. This is really just an 
	internal decorator."""

	def _loadable(*args, **kwargs):
		logger.trace(f'func: {func}, args: {args}, kwargs: {kwargs}')
		cls = args[0]
		is_loaded: bool = cls._loaded
		logger.trace(is_loaded)
		if is_loaded:
			return func(cls)
		else:
			cls._load()
			return func(cls)
	
	return _loadable

def clamp(value: int, minimum: int, maximum: int) -> int:
	return max(minimum, min(maximum, value))

def pages(amount: int, size: int) -> int:
	return ceil(amount / size)

def snake_to_camel(value: str) -> str:
	"""Converts snake_case to camelCase."""
	translation_dict = {f'_{l}': u for u, l in zip(ascii_uppercase, ascii_lowercase)}
	translation = str.maketrans(translation_dict)
	return value.translate(translation)

def snake_to_title(value: str) -> str:
	"""Converts snake_case to Title Case."""
	return ' '.join([w.capitalize() for w in value.split('_')])