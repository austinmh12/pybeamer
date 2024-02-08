from __future__ import annotations
from typing import Any

from loguru import logger

from .rest_client import RestClient
from .projects import Project

class Codebeamer:
	"""The Codebeamer API client"""
	def __init__(self, url: str, username: str, password: str, *args, **kwargs):
		self._client: RestClient = RestClient(url, username, password, api_root='cb/api/v3', *args, **kwargs)

	def get_projects(self) -> list[Project]:
		"""Fetches all the projects in the system.
		
		Returns:
		list[`Project`] — A list of projects in the system."""
		return [Project(**p, client=self._client) for p in self._client.get('projects')]
	
	def get_project(self, project: str | int) -> Project | None:
		"""Fetches a specific project in the system.
		
		Params:
		project — The name or ID of the project to fetch. — str | int
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Project` | — A project if one exists."""
		if isinstance(project, str):
			return self._get_project_by_name(project)
		elif isinstance(project, int):
			return self._get_project_by_id(project)
		else:
			raise TypeError(f'expected str or int, got {type(project)}')
		
	def _get_project_by_id(self, id: int) -> Project | None:
		try:
			project = Project(**self._client.get(f'projects/{id}'), client=self._client)
			return project
		except:
			return
		
	def _get_project_by_name(self, name: str) -> Project | None:
		project = {p.name: p for p in self.get_projects()}.get(name)
		if project is None:
			return
		project.load()
		return project
	
	def get_project_by_key(self, key: str) -> Project | None:
		search: list[dict[str, Any]] = self._client.post('projects/search', json_={'keyName': key})
		if search['total'] == 0:
			return
		return Project(**search['projects'][0], client=self._client)
