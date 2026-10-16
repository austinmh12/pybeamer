from ..api_client import APIClient

class ReportService:
	"""Service layer for Report REST operations."""

	def __init__(self, client: APIClient):
		self._client = client