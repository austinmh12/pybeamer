from __future__ import annotations
from typing import Any

from loguru import logger

from .api_client import APIClient
from .models import Project, User, Tracker, TrackerItem
from .utils import clamp, pages
from .services import *

class Codebeamer:
	"""
	Public entry point for the Codebeamer API.
	
	This class is intentionally thin:
	- instantiates and owns APIClient
	- exposes API services
	"""
	def __init__(self, url: str, username: str, password: str, *args, **kwargs):
		self._client = APIClient(url, username, password, *args, **kwargs)

		# Services
		self._associations: AssociationService | None = None
		self._attachments: AttachmentService | None = None
		self._background_jobs: BackgroundJobService | None = None
		self._baselines: BaselineService | None = None
		self._branches: BranchesService | None = None
		self._deployments: DeploymentService | None = None
		self._exports: ExportService | None = None
		self._groups: GroupService | None = None
		self._migrations: MigrationService | None = None
		self._projects: ProjectService | None = None
		self._reports: ReportService | None = None
		self._repository_items: RepositoryItemService | None = None
		self._roles: RoleService | None = None
		self._system_admin: SystemAdministratorService | None = None
		self._system: SystemService | None = None
		self._test_management: TestManagementService | None = None
		self._test_run: TestRunService | None = None
		self._traceability: TraceabilityService | None = None
		self._tracker_item_attachments: TrackerItemAttachmentService | None = None
		self._tracker_item_comments: TrackerItemCommentService | None = None
		self._tracker_item_move: TrackerItemMoveService | None = None
		self._tracker_items: TrackerItemService | None = None
		self._tracker_permissions: TrackerPermissionService | None = None
		self._tracker_reports: TrackerReportService | None = None
		self._trackers: TrackerItem | None = None
		self._tracker_tree: TrackerTreeService | None = None
		self._users: UserService | None = None
		self._wiki_comments: WikiCommentService | None = None
		self._wiki: WikiService | None = None
		self._working_set_permissions: WorkingSetPermissionService | None = None
		self._working_sets: WorkingSetService | None = None

	############
	# Services #
	############
	@property
	def associations(self) -> AssociationService:
		if self._associations is None:
			self._associations = AssociationService(self._client)
		return self._associations
	
	@property
	def attachments(self) -> AttachmentService:
		if self._attachments is None:
			self._attachments = AttachmentService(self._client)
		return self._attachments
	
	@property
	def background_jobs(self) -> BackgroundJobService:
		if self._background_jobs is None:
			self._background_jobs = BackgroundJobService(self._client)
		return self._background_jobs
	
	@property
	def baselines(self) -> BaselineService:
		if self._baselines is None:
			self._baselines = BaselineService(self._client)
		return self._baselines
	
	@property
	def branches(self) -> BranchesService:
		if self._branches is None:
			self._branches = BranchesService(self._client)
		return self._branches
	
	@property
	def deployments(self) -> DeploymentService:
		if self._deployments is None:
			self._deployments = DeploymentService(self._client)
		return self._deployments
	
	@property
	def exports(self) -> ExportService:
		if self._exports is None:
			self._exports = ExportService(self._client)
		return self._exports
	
	@property
	def groups(self) -> GroupService:
		if self._groups is None:
			self._groups = GroupService(self._client)
		return self._groups
	
	@property
	def migrations(self) -> MigrationService:
		if self._migrations is None:
			self._migrations = MigrationService(self._client)
		return self._migrations
	
	@property
	def projects(self) -> ProjectService:
		if self._projects is None:
			self._projects = ProjectService(self._client)
		return self._projects
	
	@property
	def reports(self) -> ReportService:
		if self._reports is None:
			self._reports = ReportService(self._client)
		return self._reports
	
	@property
	def repository_items(self) -> RepositoryItemService:
		if self._repository_items is None:
			self._repository_items = RepositoryItemService(self._client)
		return self._repository_items
	
	@property
	def roles(self) -> RoleService:
		if self._roles is None:
			self._roles = RoleService(self._client)
		return self._roles
	
	@property
	def system_admin(self) -> SystemAdministratorService:
		if self._system_admin is None:
			self._system_admin = SystemAdministratorService(self._client)
		return self._system_admin
	
	@property
	def system(self) -> SystemService:
		if self._system is None:
			self._system = SystemService(self._client)
		return self._system
	
	@property
	def test_management(self) -> TestManagementService:
		if self._test_management is None:
			self._test_management = TestManagementService(self._client)
		return self._test_management
	
	@property
	def test_run(self) -> TestRunService:
		if self._test_run is None:
			self._test_run = TestRunService(self._client)
		return self._test_run
	
	@property
	def traceability(self) -> TraceabilityService:
		if self._traceability is None:
			self._traceability = TraceabilityService(self._client)
		return self._traceability
	
	@property
	def tracker_item_attachments(self) -> TrackerItemAttachmentService:
		if self._tracker_item_attachments is None:
			self._tracker_item_attachments = TrackerItemAttachmentService(self._client)
		return self._tracker_item_attachments
	
	@property
	def tracker_item_comments(self) -> TrackerItemCommentService:
		if self._tracker_item_comments is None:
			self._tracker_item_comments = TrackerItemCommentService(self._client)
		return self._tracker_item_comments
	
	@property
	def tracker_item_move(self) -> TrackerItemMoveService:
		if self._tracker_item_move is None:
			self._tracker_item_move = TrackerItemMoveService(self._client)
		return self._tracker_item_move
	
	@property
	def tracker_items(self) -> TrackerItemService:
		if self._tracker_items is None:
			self._tracker_items = TrackerItemService(self._client)
		return self._tracker_items
	
	@property
	def tracker_permissions(self) -> TrackerPermissionService:
		if self._tracker_permissions is None:
			self._tracker_permissions = TrackerPermissionService(self._client)
		return self._tracker_permissions
	
	@property
	def tracker_reports(self) -> TrackerReportService:
		if self._tracker_reports is None:
			self._tracker_reports = TrackerReportService(self._client)
		return self._tracker_reports
	
	@property
	def trackers(self) -> TrackerItem:
		if self._trackers is None:
			self._trackers = TrackerItem(self._client)
		return self._trackers
	
	@property
	def tracker_tree(self) -> TrackerTreeService:
		if self._tracker_tree is None:
			self._tracker_tree = TrackerTreeService(self._client)
		return self._tracker_tree
	
	@property
	def users(self) -> UserService:
		if self._users is None:
			self._users = UserService(self._client)
		return self._users
	
	@property
	def wiki_comments(self) -> WikiCommentService:
		if self._wiki_comments is None:
			self._wiki_comments = WikiCommentService(self._client)
		return self._wiki_comments
	
	@property
	def wiki(self) -> WikiService:
		if self._wiki is None:
			self._wiki = WikiService(self._client)
		return self._wiki
	
	@property
	def working_set_permissions(self) -> WorkingSetPermissionService:
		if self._working_set_permissions is None:
			self._working_set_permissions = WorkingSetPermissionService(self._client)
		return self._working_set_permissions
	
	@property
	def working_sets(self) -> WorkingSetService:
		if self._working_sets is None:
			self._working_sets = WorkingSetService(self._client)
		return self._working_sets
	

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