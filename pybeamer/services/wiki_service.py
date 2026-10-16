from ..api_client import APIClient

class WikiService:
	"""Service layer for Wiki REST operations."""

	def __init__(self, client: APIClient):
		self._client = client