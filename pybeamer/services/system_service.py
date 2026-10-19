from typing import Any

from ..api_client import APIClient

class SystemService:
	"""Service layer for System REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_maintenance_status(self) -> list[dict[str, Any]]: ... # TODO: MaintenanceStatus
	def set_maintenance_status(self, **kwargs): ... # TODO: args