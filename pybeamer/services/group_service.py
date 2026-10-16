from ..api_client import APIClient

class GroupService:
	"""Service layer for Group REST operations."""

	def __init__(self, client: APIClient):
		self._client = client