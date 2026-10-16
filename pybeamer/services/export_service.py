from ..api_client import APIClient

class ExportService:
	"""Service layer for Export REST operations."""

	def __init__(self, client: APIClient):
		self._client = client