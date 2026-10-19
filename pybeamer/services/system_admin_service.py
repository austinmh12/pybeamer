from typing import Any

from ..api_client import APIClient

class SystemAdministratorService:
	"""Service layer for System Administrator REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_audit_permissions(self) -> list[dict[str, Any]]: ... # TODO: AuditPermissions