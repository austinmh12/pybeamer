from __future__ import annotations
from typing import Any

from loguru import logger
from math import ceil

from .rest_client import RestClient
from .projects import Project
from .user import User

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
		`Project` — A project if one exists."""
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

	def get_users(self, page: int = 0, page_size: int = 25) -> list[User]:
		"""Fetches all the users in the system.

		Params:
		page — The page number to fetch if you want a specific page of users. If 0 then all users are fetched. — int(0)
		page_size — The number of results per page of users. Must be between 1 and 500. — int(25) 
		
		Returns:
		list[`User`] — A list of users in the system."""
		fetch_all = page == 0
		if fetch_all:
			page = 1
		page_size = max(1, min(500, page_size)) # Clamp page_size between 1 and 500
		params = {'page': page, 'pageSize': page_size}
		users: list[User] = []
		user_data = self._client.get('users', params=params)
		total_pages = ceil(user_data['total'] / page_size)
		users.extend([User(**u, client=self._client) for u in user_data['users']])
		if fetch_all:
			while params['page'] < total_pages:
				params['page'] += 1
				user_data = self._client.get('users', params=params)
				users.extend([User(**u, client=self._client) for u in user_data['users']])
		return users
	
	def get_user(self, user: str | int) -> User | None:
		"""Fetches a specific user from the system.
		
		Params:
		user — The name, email, or ID of the user to fetch. — str | int
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`User` — A user if one exists."""
		if isinstance(user, str):
			if '@' in user:
				return self._get_user_by_email(user)
			return self._get_user_by_name(user)
		elif isinstance(user, int):
			return self._get_user_by_id(user)
		else:
			raise TypeError(f'expected str or int, got {type(user)}')
		
	def _get_user_by_id(self, id: int) -> User | None:
		try:
			user = User(**self._client.get(f'users/{id}'), client=self._client)
			return user
		except:
			return
		
	def _get_user_by_name(self, name: str) -> User | None:
		try:
			user = User(**self._client.get('users/findByName', params={'name': name}), client=self._client)
			return user
		except:
			return
		
	def _get_user_by_email(self, email: str) -> User | None:
		try:
			user = User(**self._client.get('users/findByEmail', params={'email': email}), client=self._client)
			return user
		except:
			return