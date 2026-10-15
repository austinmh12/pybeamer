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
		"""Fetches all the projects in Codebeamer.
		
		Returns:
		list[`Project`] — A list of projects in Codebeamer."""
		return [Project(**p, client=self._client) for p in self._client.get('projects')]

	def get_project(self, project: str | int | Project) -> Project | None:
		"""Fetches a specific project from Codebeamer.
		
		Params:
		project — The name or ID of the project to fetch. — str | int | `Project`
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Project` — A project if one exists or if the input was a `Project` isntance."""
		if isinstance(project, Project):
			return project
		elif isinstance(project, str):
			return self.get_by_name(project)
		elif isinstance(project, int):
			return self.get_by_id(project)
		raise TypeError(f'expected str or int, got {type(project)}')

	def get_by_id(self, id: int) -> Project | None:
		"""Fetches a specific project from Codebeamer with the given ID.
		
		Params:
		id — The ID of the project to fetch. — int
		
		Returns:
		`Project` — A project if one exists with a matching ID."""
		#! Need to error check this as fetching a project without a valid ID will raise
		return Project(**self._client.get(f'projects/{id}'), client=self._client)

	def get_by_name(self, name: str) -> Project | None:
		"""Fetches a specific project from Codebeamer with the given name.
		
		Params:
		name — The name of the project to fetch. — str
		
		Returns:
		`Project` — A project if one exists with a matching name."""
		return {p.name: p for p in self()}.get(name)

	def get_by_key(self, key: str) -> Project | None:
		"""Fetches a specific project from Codebeamer with the given key.
		
		Params:
		key — The key of the project to fetch. — str
		
		Returns:
		`Project` — A project if one exists with a matching key."""
		search: list[dict[str, Any]] = self._client.post('projects/search', json_={'keyName': key})
		if search['total'] == 0:
			return
		return Project(**search['projects'][0], client=self._client)

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

	def get_member_project_permissions(self, member: str | int | User) -> dict[str, str]: # TODO: Permissions
		...

	############
	# Trackers #
	############
	def get_trackers(self, project: str | int | Project) -> list[Tracker]:
		"""Fetches all the trackers under this project.
		
		Returns:
		list[`Tracker`] — All the trackers in the current project."""
		project = self.get_project(project)
		return [Tracker(**t, client=self._client, project=project) for t in self._client.get(f'projects/{project.id}/trackers')]

	def get_tracker(
		self,
		project: str | int | Project,
		tracker: str | int
	) -> Tracker | None:
		"""Fetches a specific tracker from the project.
		
		Params:
		tracker — The name or ID of the tracker to fetch. — str | int
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Tracker` — The tracker if it exists under the project."""
		if isinstance(tracker, int):
			return {t.id: t for t in self.get_trackers(project)}.get(tracker)
		elif isinstance(tracker, str):
			return {t.name: t for t in self.get_trackers(project)}.get(tracker)
		raise TypeError(f'expected str or int, got {type(tracker)}')
	
	def create_tracker(
		self,
		project: str | int | Project,
		name: str,
		key_name: str,
		**kwargs
	) -> Tracker:
		"""Create a tracker in the current project."""
		# TODO: Defaults for the rest of the arguments that are mandatory

	def search_trackers(
		self,
		project: str | int | Project,
		key_name: str,
		deleted: bool = False,
		hidden: bool = False,
		**kwargs # TODO: types: list[dict[str, str | int]]
	) -> list[Tracker]:
		...

	#############
	# Wikipages #
	#############
	def get_wiki_pages(self, project: str | int | Project) -> list[dict[str, Any]]: # TODO: WikiOutline
		...

	##########
	# Deploy #
	##########
	def deploy_configuration(
		self,
		project: str | int | Project,
		project_file_id: int,
		configuration_file_id: int,
		configuration_file_password: str
	):
		...