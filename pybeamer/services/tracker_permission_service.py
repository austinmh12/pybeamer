from ..api_client import APIClient
from ..models import Tracker, Role

TrackerLike = str | int | Tracker
RoleLike = str | int | Role

class TrackerPermissionService:
	"""Service layer for Tracker Permission REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/trackers/{trackerId}/permissions
	def get_tracker_permissions(self, tracker: TrackerLike): ...
	# DELETE /v3/trackers/{trackerId}/roles/{roleId}/permissions
	def delete_tracker_role_permissions(self, tracker: TrackerLike, role: RoleLike): ...
	# PUT /v3/trackers/{trackerId}/roles/{roleId}/permissions
	def set_tracker_role_permissions(self, tracker: TrackerLike, role: RoleLike): ...
	# GET /v3/trackers/permissions
	def get_available_tracker_permissions(self): ...
	# GET /v3/trackers/permissions/{trackerPermissionId}
	def get_tracker_permission(self, permission: int): ...