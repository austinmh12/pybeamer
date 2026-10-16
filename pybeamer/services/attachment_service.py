from typing import Any

from ..api_client import APIClient
from ..models import Attachment

class AttachmentService:
	"""Service layer for Attachment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def delete_attachment(self, attachment: str | int | Attachment): ...
	def get_attachment(self, attachment: str | int | Attachment) -> Attachment | None: ...
	def get_attachment_content(self, attachment: str | int | Attachment) -> bytes | None: ...
	def update_attachment(self, attachment: str | int | Attachment, content: bytes): ... # TODO: content: HasRead or Pathlike or something along those lines
	def get_attachment_history(self, attachment: str | int | Attachment) -> list[dict[str, Any]]: ... # TODO: AttachmentHistory
	def restore_attachment(self, attachment: str | int | Attachment, version: int): ...