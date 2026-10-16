from ..api_client import APIClient

class UserService:
	"""Service layer for User REST operations."""

	def __init__(self, client: APIClient):
		self._client = client