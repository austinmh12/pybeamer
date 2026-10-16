from ..api_client import APIClient

class AttachmentService:
	"""Service layer for Attachment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client