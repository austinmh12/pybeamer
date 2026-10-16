from ..api_client import APIClient

class TrackerReportService:
	"""Service layer for Tracker Report REST operations."""

	def __init__(self, client: APIClient):
		self._client = client