from ..api_client import APIClient

class TestRunService:
	"""Service layer for Test Run REST operations."""

	def __init__(self, client: APIClient):
		self._client = client