from typing import Any

from ..models import Project, User, Tracker
from ..api_client import APIClient

class ProjectService:
	"""Service layer for Project REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	##################
	# Default Method #
	##################
	def __call__(self, *, project: str | int = None) -> list[Project]:
		if project:
			return self.get_project(project)
		return self.get_projects()

	############
	# Projects #
	############
	def get_projects(self) -> list[Project]:
		"""Fetches all the projects in """
		...

	def get_project(self, project: str | int) -> Project | None:
		...

	def get_by_id(self, id: int) -> Project | None:
		...

	def get_by_name(self, name: str) -> Project | None:
		...

	def get_by_key(self, key: str) -> Project | None:
		...

	###########
	# Members #
	###########
	def get_members(self) -> list[User]:
		...

	def get_member(self, member: str | int) -> User | None:
		...

	def get_member_by_id(self, id: int) -> User | None:
		...

	def get_member_by_name(self, name: str) -> User | None:
		...

	