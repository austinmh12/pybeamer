from ..api_client import APIClient

class TrackerTreeService:
	"""Service layer for Tracker Tree REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/trackers/tree
	def get_tracker_tree(self): ...
	# POST /v3/trackers/tree/update
	def update_tracker_tree(self): ...