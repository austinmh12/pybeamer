from ..api_client import APIClient

class TrackerItemService:
	"""Service layer for Tracker Item REST operations."""

	def __init__(self, client: APIClient):
		self._client = client