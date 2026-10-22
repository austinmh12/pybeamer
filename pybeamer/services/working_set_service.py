from ..api_client import APIClient
from ..models import Project, Tracker

ProjectLike = str | int | Project
TrackerLike = str | int | Tracker

class WorkingSetService:
	"""Service layer for Working Set REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/projects/{projectId}/working-sets
	def get_project_level_working_sets(self, project: ProjectLike): ...
	# GET /v3/trackers/{trackerId}/working-sets
	def get_working_sets(self, tracker: TrackerLike): ...
	# GET /v3/working-sets/{workingSetId}
	def get_working_set(self, working_set: int): ...
	# GET /v3/working-sets/{workingSetId}/trackers
	def get_working_set_trackers(self, working_set: int) -> list[Tracker]: ...
	# POST /v3/working-sets/items-mapping
	def map_working_set_tracker_items(self, **kwargs): ...