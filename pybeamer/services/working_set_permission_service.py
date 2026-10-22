from ..api_client import APIClient

class WorkingSetPermissionService:
	"""Service layer for Working Set Permission REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# POST /v3/workingset/{workingSetId}/permission
	def set_working_set_permissions(self, working_set: int, **kwargs): ...