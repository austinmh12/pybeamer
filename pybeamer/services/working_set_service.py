from ..api_client import APIClient

class WorkingSetService:
	"""Service layer for Working Set REST operations."""

	def __init__(self, client: APIClient):
		self._client = client