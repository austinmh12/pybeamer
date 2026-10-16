from ..api_client import APIClient

class TrackerItemMoveService:
	"""Service layer for Tracker Item Move REST operations."""

	def __init__(self, client: APIClient):
		self._client = client