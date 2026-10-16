from ..api_client import APIClient

class WikiCommentService:
	"""Service layer for Wiki Comment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client