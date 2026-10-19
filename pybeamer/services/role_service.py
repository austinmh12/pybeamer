from ..api_client import APIClient
from ..models import Role

class RoleService:
	"""Service layer for Role REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_roles(self) -> list[Role]: ...
	def get_by_id(self, id: int) -> Role | None: ...

	###########
	# Helpers #
	###########
	def get_role(self, role: str | int | Role) -> Role | None: ...
	def get_by_name(self, name: str) -> Role | None: ...