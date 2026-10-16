from ..api_client import APIClient

class TraceabilityService:
	"""Service layer for Traceability REST operations."""

	def __init__(self, client: APIClient):
		self._client = client