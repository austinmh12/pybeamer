from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient

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
		_created_by: dict[str, Any] | None # TODO: Replace with User
		_modified_at: datetime | None
		_modified_by: dict[str, Any] | None # TODO: Replace with User

	def __init__(self, id: int, name: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# type only appears in GET /projects
		if kwargs.get('type'):
			# if type is present then no other information is present
			self._description = None
			self._description_format = None
			self._version = None
			self._key_name = None
			self._category = None
			self._closed = None
			self._deleted = None
			self._template = None
			self._created_at = None
			self._created_by = None
			self._modified_at = None
			self._modified_by = None
		else:
			self._description = kwargs.get('description')
			self._description_format = kwargs.get('descriptionFormat')
			self._version = kwargs.get('version')
			self._key_name = kwargs.get('keyName')
			self._category = kwargs.get('category')
			self._closed = kwargs.get('closed')
			self._deleted = kwargs.get('deleted')
			self._template = kwargs.get('template')
			self._created_at = datetime.strptime(kwargs.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._created_by = kwargs.get('createdBy')
			self._modified_at = datetime.strptime(kwargs.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._modified_by = kwargs.get('modifiedBy')

	@property
	def id(self) -> int:
		"""The ID of the project."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the project."""
		return self._name

	@property
	def description(self) -> str | None:
		"""The project description."""
		return self._description

	@property
	def description_format(self) -> str | None:
		"""The format of the project description."""
		return self._description_format

	@property
	def version(self) -> int | None:
		"""The project version."""
		return self._version

	@property
	def key_name(self) -> str | None:
		"""The project key identifier."""
		return self._key_name

	@property
	def category(self) -> str | None:
		"""The category of the project."""
		return self._category

	@property
	def closed(self) -> bool | None:
		"""Flag for whether the project is closed or not."""
		return self._closed

	@property
	def deleted(self) -> bool | None:
		"""Flag for whether the project is deleted or not."""
		return self._deleted

	@property
	def template(self) -> bool | None:
		"""Flag for whether the project is a template or not."""
		return self._template

	@property
	def created_at(self) -> datetime | None:
		"""The datetime the project was created at."""
		return self._created_at

	@property
	def created_by(self) -> dict[str, Any] | None: # TODO: Replace with User
		"""The user that created the project."""
		return self._created_by

	@property
	def modified_at(self) -> datetime | None:
		"""The datetime the project was last modified."""
		return self._modified_at

	@property
	def modified_by(self) -> dict[str, Any] | None: # TODO: Replace with User
		"""The user that last modified the project."""
		return self._modified_by

	def load(self):
		"""Loads the rest of the project's data. When a project is fetched using 
		`Codebeamer.get_projects` only the ID and Name of the project are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the project information if it is 
		needed."""
		if self.created_at:
			logger.info('Project already loaded, ignoring...')
			return
		project_data: dict[str, Any] = self._client.get(f'projects/{self.id}')
		logger.debug(project_data)
		self._description = project_data.get('description')
		self._description_format = project_data.get('descriptionFormat')
		self._version = project_data.get('version')
		self._key_name = project_data.get('keyName')
		self._category = project_data.get('category')
		self._closed = project_data.get('closed')
		self._deleted = project_data.get('deleted')
		self._template = project_data.get('template')
		self._created_at = project_data.get('createdAt')
		self._created_by = project_data.get('createdBy')
		self._modified_at = project_data.get('modifiedAt')
		self._modified_by = project_data.get('modifiedBy')

	def __repr__(self) -> str:
		return f'Project(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, Project) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, Project) and self.id < o.id