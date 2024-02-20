from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient
from .user import User
from .tracker import Tracker
from .utils import loadable

class Project:
	"""Represents a project in codeBeamer."""

	if TYPE_CHECKING:
		_description: str | None
		_description_format: str | None
		_version: int | None
		_key_name: str | None
		_category: str | None
		_closed: bool | None
		_deleted: bool | None
		_template: bool | None
		_created_at: datetime | None
		_created_by: User | None
		_modified_at: datetime | None
		_modified_by: User | None
		_trackers: list[Tracker]
		_loaded: bool

	def __init__(self, id: int, name: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# type only appears in GET /projects
		if not kwargs.get('type'):
			# if type is present then no other information is present
			self._load(kwargs)
		else:
			prop_defaults = {k: None for k in self.__class__.__annotations__}
			self.__dict__.update(prop_defaults)
			self._trackers = list()
			self._loaded = False

	@property
	def id(self) -> int:
		"""The ID of the project."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the project."""
		return self._name

	@property
	@loadable
	def description(self) -> str | None:
		"""The project description."""
		return self._description

	@property
	@loadable
	def description_format(self) -> str | None:
		"""The format of the project description."""
		return self._description_format

	@property
	@loadable
	def version(self) -> int | None:
		"""The project version."""
		return self._version

	@property
	@loadable
	def key_name(self) -> str | None:
		"""The project key identifier."""
		return self._key_name

	@property
	@loadable
	def category(self) -> str | None:
		"""The category of the project."""
		return self._category

	@property
	@loadable
	def closed(self) -> bool | None:
		"""Flag for whether the project is closed or not."""
		return self._closed

	@property
	@loadable
	def deleted(self) -> bool | None:
		"""Flag for whether the project is deleted or not."""
		return self._deleted

	@property
	@loadable
	def template(self) -> bool | None:
		"""Flag for whether the project is a template or not."""
		return self._template

	@property
	@loadable
	def created_at(self) -> datetime | None:
		"""The datetime the project was created at."""
		return self._created_at

	@property
	@loadable
	def created_by(self) -> User | None:
		"""The user that created the project."""
		return self._created_by

	@property
	@loadable
	def modified_at(self) -> datetime | None:
		"""The datetime the project was last modified."""
		return self._modified_at

	@property
	@loadable
	def modified_by(self) -> User | None:
		"""The user that last modified the project."""
		return self._modified_by

	def _load(self, data: dict[str, Any] = None):
		"""Loads the rest of the project's data. When a project is fetched using 
		`Codebeamer.get_projects` only the ID and Name of the project are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the project information if it is 
		needed."""
		if self._loaded:
			logger.info('Project already loaded, ignoring...')
			return
		if not data:
			data: dict[str, Any] = self._client.get(f'projects/{self.id}')
		logger.debug(data)
		self._description = data.get('description')
		self._description_format = data.get('descriptionFormat')
		self._version = data.get('version')
		self._key_name = data.get('keyName')
		self._category = data.get('category')
		self._closed = data.get('closed')
		self._deleted = data.get('deleted')
		self._template = data.get('template')
		self._created_at = datetime.strptime(data.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._created_by = User(**data.get('createdBy'), client=self._client)
		self._modified_at = datetime.strptime(data.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._modified_by = User(**data.get('modifiedBy'), client=self._client)
		self._trackers = list()
		self._loaded = True

	def get_trackers(self) -> list[Tracker]:
		"""Fetches all the trackers in this project.
		
		Returns:
		list[`Tracker`] — All the trackers under this project."""
		return [Tracker(**t, client=self._client, project=self) for t in self._client.get(f'projects/{self.id}/trackers')]

	def get_tracker(self, tracker: str | int) -> Tracker | None:
		"""Fetches a specific tracker from the project.
		
		Params:
		tracker — The name or ID of the tracker to fetch. — str | int
		
		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Tracker` — The tracker if it exists under the project."""
		if not self._trackers:
			self._trackers = self.get_trackers()
		if isinstance(tracker, int):
			trackers = {t.id: t for t in self._trackers}
		elif isinstance(tracker, str):
			trackers = {t.name: t for t in self._trackers}
		else:
			raise TypeError(f'expected str or int, got {type(tracker)}')
		return trackers.get(tracker)
	
	def create_tracker(
		self,
		name: str,
		key_name: str,
		**kwargs
	) -> Tracker:
		"""Create a tracker in the current project."""
		# TODO: Defaults for the rest of the arguments that are mandatory

	def __repr__(self) -> str:
		return f'Project(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, Project) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, Project) and self.id < o.id