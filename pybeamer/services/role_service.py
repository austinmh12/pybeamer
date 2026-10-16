from ..api_client import APIClient

class RoleService:
	"""Service layer for Role REST operations."""

	def __init__(self, client: APIClient):
		self._client = client