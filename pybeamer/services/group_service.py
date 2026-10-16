from ..api_client import APIClient
from ..models import Group, User

class GroupService:
	"""Service layer for Group REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def get_groups(self) -> list[Group]: ...

	def get_group(self, group: int | str | Group) -> Group | None:
		if isinstance(group, Group):
			return group
		elif isinstance(group, int):
			return self.get_by_id(group)
		elif isinstance(group, str):
			return self.get_by_name(group)
		raise TypeError(f'expected str or int, got {type(group)}')

	def get_by_id(self, id: int) -> Group | None: ...

	def get_by_name(self, name: str) -> Group | None:
		return {g.name: g for g in self.get_groups()}.get(name, None)
	
	def get_group_members(self, group: int | str | Group) -> list[User]: ...