from ..api_client import APIClient

class MigrationService:
	"""Service layer for Migration REST operations."""

	def __init__(self, client: APIClient):
		self._client = client