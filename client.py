from __future__ import annotations
from typing import Any

from loguru import logger

from .rest_client import RestClient
from .projects import Project
from .user import User
from .tracker import Tracker
from .tracker_item import TrackerItem
from .utils import clamp, pages

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
		page_size = clamp(page_size, 1, 500) # Clamp page_size between 1 and 500
		params = {'page': page, 'pageSize': page_size}
		users: list[User] = []
		user_data = self._client.get('users', params=params)
		total_pages = pages(user_data['total'], page_size)
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
		
	def get_tracker(self, tracker: str | int) -> Tracker | None:
		"""Fetches a specific tracker from the system.
		
		Params:
		tracker — The name or ID of the tracker to fetch. — str | int
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Tracker` — The tracker if it exists."""
		if isinstance(tracker, int):
			return self._get_tracker_by_id(tracker)
		elif isinstance(tracker, str):
			return self._get_tracker_by_name(tracker)
		else:
			raise TypeError(f'expected str or int, got {type(tracker)}')
		
	def _get_tracker_by_id(self, id: int) -> Tracker | None:
		try:
			tracker = Tracker(**self._client.get(f'trackers/{id}'), client=self._client)
			return tracker
		except Exception as e:
			logger.exception(e)
			return
	
	def _get_tracker_by_name(self, name: str) -> Tracker | None:
		# Trackers aren't searchable outside of projects, so all the projects have
		# to be fetched, each project needs to get it's trackers, then the dict needs
		# to be made.
		trackers = {t.name: t for p in self.get_projects() for t in p.get_trackers()}
		logger.debug(list(trackers.keys()))
		return trackers.get(name)
	
	def get_tracker_item(self, id: int) -> TrackerItem | None:
		"""Fetches a specific tracker item.
		
		Params:
		id — The ID of the item to fetch. — int
		
		Returns:
		`TrackerItem` — The tracker item if it exists."""
		try:
			item = TrackerItem(**self._client.get(f'items/{id}'), client=self._client)
			return item
		except Exception as e:
			logger.exception(e)
			return
		
	def get_item(self, id: int) -> TrackerItem | None:
		"""Alias for `Codebeamer.get_tracker_item`."""
		return self.get_tracker_item(id)
	
	def search_tracker_items(self, query: str, page: int = 0, page_size: int = 25) -> list[TrackerItem]:
		"""Search for items using a cbQL query string.
		
		Params:
		query — The query string to search with. — str
		page — The page number to fetch if you want a specific page of users. If 0 then all users are fetched. — int(0)
		page_size — The number of results per page of users. Must be between 1 and 500. — int(25)
		
		Returns:
		list[`TrackerItem`] — A list of items that match the query."""
		fetch_all = page == 0
		if fetch_all:
			page = 1
		page_size = clamp(page_size, 1, 500) # Clamp page_size between 1 and 500
		data = {'page': page, 'pageSize': page_size, 'queryString': query}
		items: list[TrackerItem] = []
		item_data = self._client.post('items/query', json_=data)
		total_pages = pages(item_data['total'], page_size)
		items.extend([TrackerItem(**ti, client=self._client) for ti in item_data['items']])
		if fetch_all:
			while data['page'] < total_pages:
				data['page'] += 1
				item_data = self._client.post('items/query', json_=data)
				items.extend([TrackerItem(**ti, client=self._client) for ti in item_data['items']])
		return items

	def search_items(self, query: str, page: int = 0, page_size: int = 25) -> list[TrackerItem]:
		"""Alias for `Codebeamer.search_tracker_items`"""
		return self.search_tracker_items(query=query, page=page, page_size=page_size)