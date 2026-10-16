from ..api_client import APIClient

class SystemAdministratorService:
	"""Service layer for System Administrator REST operations."""

	def __init__(self, client: APIClient):
		self._client = client