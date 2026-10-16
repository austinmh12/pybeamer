from ..api_client import APIClient

class BranchesService:
	"""Service layer for Branch REST operations."""

	def __init__(self, client: APIClient):
		self._client = client