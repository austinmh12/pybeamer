from ..api_client import APIClient
from ..models import Project

class RepositoryItemService:
	"""Service layer for Repository Item REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def create_external_scm_repository(self, project: str | int | Project, **kwargs): ... # TODO: args
	def update_external_scm_repository_item(self, project: str | int | Project, item: int, **kwargs): ... # TODO: args