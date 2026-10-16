from ..api_client import APIClient
from ..models import BackgroundJob

class BackgroundJobService:
	"""Service layer for Background Job REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_background_job(self, job: int) -> BackgroundJob | None: ...
	def update_working_set(self, **kwargs): ... # TODO: args