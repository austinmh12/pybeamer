from loguru import logger

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