from ..api_client import APIClient

class WorkingSetPermissionService:
	"""Service layer for Working Set Permission REST operations."""

	def __init__(self, client: APIClient):
		self._client = client