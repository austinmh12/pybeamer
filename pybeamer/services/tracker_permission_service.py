from ..api_client import APIClient

class TrackerPermissionService:
	"""Service layer for Tracker Permission REST operations."""

	def __init__(self, client: APIClient):
		self._client = client