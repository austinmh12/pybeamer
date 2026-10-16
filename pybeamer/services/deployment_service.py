from ..api_client import APIClient

class DeploymentService:
	"""Service layer for Deployment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client