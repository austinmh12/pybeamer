from ..api_client import APIClient

class TrackerItemAttachmentService:
	"""Service layer for Tracker Item Attachment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client