from ..api_client import APIClient

class TrackerTreeService:
	"""Service layer for Tracker Tree REST operations."""

	def __init__(self, client: APIClient):
		self._client = client