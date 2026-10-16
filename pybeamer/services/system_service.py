from ..api_client import APIClient

class SystemService:
	"""Service layer for System REST operations."""

	def __init__(self, client: APIClient):
		self._client = client