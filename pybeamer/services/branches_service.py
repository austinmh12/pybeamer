from ..api_client import APIClient
from ..models import TrackerItem

class BranchesService:
	"""Service layer for Branch REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_branch_tracker_item(self, branch: int, item: int) -> TrackerItem: ...