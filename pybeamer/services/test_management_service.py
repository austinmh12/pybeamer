from ..api_client import APIClient

class TestManagementService:
	"""Service layer for Test Management REST operations."""

	def __init__(self, client: APIClient):
		self._client = client