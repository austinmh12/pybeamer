from ..api_client import APIClient

class AssociationService:
	"""Service layer for Association REST operations."""

	def __init__(self, client: APIClient):
		self._client = client