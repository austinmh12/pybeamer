from __future__ import annotations
from typing import Any

from loguru import logger
from datetime import datetime

from ..api_client import APIClient
from .user import User
from .tracker import Tracker
from ..utils import lazy, parse_date

class Project:
	"""Represents a project in codeBeamer."""

	def __init__(self, id: int, name: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._client: APIClient = kwargs.get('client')
		self._trackers: list[Tracker] = list()
		self._loaded: bool = False

	############
	# Identity #
	############
	@property
	def id(self) -> int:
		"""The ID of the project."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the project."""
		return self._name

	###############
	# Lazy-loaded #
	###############
	@property
	@lazy
	def description(self) -> str | None:
		"""The project description."""
		return self._description

	@property
	@lazy
	def description_format(self) -> str | None:
		"""The format of the project description."""
		return self._description_format

	@property
	@lazy
	def version(self) -> int | None:
		"""The project version."""
		return self._version

	@property
	@lazy
	def key_name(self) -> str | None:
		"""The project key identifier."""
		return self._key_name

	@property
	@lazy
	def category(self) -> str | None:
		"""The category of the project."""
		return self._category

	@property
	@lazy
	def closed(self) -> bool | None:
		"""Flag for whether the project is closed or not."""
		return self._closed

	@property
	@lazy
	def deleted(self) -> bool | None:
		"""Flag for whether the project is deleted or not."""
		return self._deleted

	@property
	@lazy
	def template(self) -> bool | None:
		"""Flag for whether the project is a template or not."""
		return self._template

	@property
	@lazy
	def created_at(self) -> datetime | None:
		"""The datetime the project was created at."""
		return self._created_at

	@property
	@lazy
	def created_by(self) -> User | None:
		"""The user that created the project."""
		return self._created_by

	@property
	@lazy
	def modified_at(self) -> datetime | None:
		"""The datetime the project was last modified."""
		return self._modified_at

	@property
	@lazy
	def modified_by(self) -> User | None:
		"""The user that last modified the project."""
		return self._modified_by

	###########
	# Loading #
	###########
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
		self._created_at = parse_date(data.get('createdAt'))
		self._created_by = User(**data.get('createdBy'), client=self._client)
		self._modified_at = parse_date(data.get('modifiedAt'))
		self._modified_by = User(**data.get('modifiedBy'), client=self._client)

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