from typing import Any

from ..api_client import APIClient
from ..models import Tracker

TrackerLike = str | int | Tracker

class TrackerItemMoveService:
	"""Service layer for Tracker Item Move REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def move_item(self, **kwargs): ... # TODO: args
	def get_default_field_mapping(self, source: TrackerLike, target: TrackerLike) -> list[dict[str, Any]]: ... # TODO: FieldMapping