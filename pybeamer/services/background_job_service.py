from ..api_client import APIClient

class BackgroundJobService:
	"""Service layer for Background Job REST operations."""

	def __init__(self, client: APIClient):
		self._client = client