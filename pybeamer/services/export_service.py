from typing import Any

from ..api_client import APIClient
from ..models import TrackerItem, Project

class ExportService:
	"""Service layer for Export REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def export_to_word(self, **kwargs): ... # TODO: args
	def get_tracker_items(self, **kwargs) -> list[TrackerItem]: ... # TODO: args
	def get_tracker_item_reviews(self, **kwargs) -> list[dict[str, Any]]: ... # TODO: TrackerItemReview
	def export_project_to_zip(self, project: str | int | Project) -> bytes: ...