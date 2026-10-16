from ..api_client import APIClient

class TrackerItemCommentService:
	"""Service layer for Tracker Item Comment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client