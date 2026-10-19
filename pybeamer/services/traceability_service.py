from ..api_client import APIClient

class TraceabilityService:
	"""Service layer for Traceability REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_traceability_items(self): ...
	def get_traceability_relations(self): ...