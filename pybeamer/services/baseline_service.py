from ..api_client import APIClient

class BaselineService:
	"""Service layer for Baseline REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def create_baseline(self, **kwargs): ... # TODO: args