from ..api_client import APIClient

class RepositoryItemService:
	"""Service layer for Repository Item REST operations."""

	def __init__(self, client: APIClient):
		self._client = client