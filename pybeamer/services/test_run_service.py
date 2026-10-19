from ..api_client import APIClient

class TestRunService:
	"""Service layer for Test Run REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def update_test_run_results(self, test: int): ...
	def create_automated_test_set(self, **kwargs): ...
	def create_test_run(self, **kwargs): ...
	def create_test_run_from_test_set(self, **kwargs): ...