from typing import Any

from ..api_client import APIClient
from ..models import TrackerItem

ItemLike = str | int | TrackerItem

class TrackerItemCommentService:
	"""Service layer for Tracker Item Comment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def delete_item_comments(self, item: ItemLike): ...
	def get_item_comments(self, item: ItemLike) -> list[dict[str, Any]]: ... # TODO: Comment
	def add_item_comment(self, item: ItemLike, comment: str): ...
	def delete_item_comment(self, item: ItemLike, id: int): ...
	def get_item_comment(self, item: ItemLike, id: int): ...
	def reply_to_item_comment(self, item: ItemLike, id: int, comment: str): ...
	def edit_item_comment(self, item: ItemLike, id: int, comment: str): ...