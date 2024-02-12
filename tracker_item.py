from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient
from .user import User
from .utils import loadable

if TYPE_CHECKING:
	from .tracker import Tracker

class TrackerItem:
	"""Represents a tracker item in codeBeamer."""
	if TYPE_CHECKING:
		_description: str | None
		_description_format: str | None
		_created_at: datetime | None
		_created_by: User | None
		_modified_at: datetime | None
		_modified_by: User | None
		_parent: TrackerItem | None
		_version: int | None
		_assigned_to: list[User] | None
		_closed_at: datetime | None
		_tracker: Tracker | None
		_children: list[TrackerItem] | None
		_custom_fields: list[dict[str, Any]] | None # TODO: Field(Custom)
		_priority: dict[str, Any] | None # TODO: Field(ChoiceOption)
		_status: dict[str, Any] | None # TODO: Field(ChoiceOption)
		_categories: list[dict[str, Any]] | None # TODO: Field(ChoiceOption)
		_subjects: list[dict[str, Any]] | None # TODO: Field(ChoiceOption)
		_resolutions: list[dict[str, Any]] | None # TODO: Field(ChoiceOption)
		_severities: list[dict[str, Any]] | None # TODO: Field(ChoiceOption)
		_teams: list[dict[str, Any]] | None # TODO: Field(ChoiceOption)
		_versions: list[dict[str, Any]] | None # TODO: Versions
		_ordinal: int | None
		_type_name: str | None
		_comments: list[dict[str, Any]] | None # TODO: Comments
		_tags: list[dict[str, Any]] | None # TODO: Tags
		# TODO: There are more base fields than this such as owners, platforms, etc
		_loaded: bool

	def __init__(self, id: int, name: str, *args, **kwargs):
		# TODO: Figure out how to handle parent in a similar way to tracker
		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# Want to try and get this regardless of type since it can come from the Tracker class
		self._tracker = kwargs.get('tracker')
		# type only appears in GET /trackers/{trackerId}/items
		_type = kwargs.get('type')
		if isinstance(_type, str):
			# if type is present then no other information is present
			self._description = None
			self._description_format = None
			self._created_at = None
			self._created_by = None
			self._modified_at = None
			self._modified_by = None
			self._parent = None
			self._version = None
			self._assigned_to = None
			self._closed_at = None
			self._children = None
			self._custom_fields = None
			self._priority = None
			self._status = None
			self._categories = None
			self._subjects = None
			self._resolutions = None
			self._severities = None
			self._teams = None
			self._versions = None
			self._ordinal = None
			self._type_name = None
			self._comments = None
			self._tags = None
			self._loaded = False
		else:
			self._description = kwargs.get('description')
			self._description_format = kwargs.get('descriptionFormat')
			self._created_at = datetime.strptime(kwargs.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._created_by = User(**kwargs.get('createdBy'), client=self._client)
			self._modified_at = datetime.strptime(kwargs.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._modified_by = User(**kwargs.get('modifiedBy'), client=self._client)
			self._parent = TrackerItem(**kwargs.get('parent'), client=self._client)
			self._version = kwargs.get('version')
			self._assigned_to = kwargs.get('assignedTo')
			self._closed_at = datetime.strptime(kwargs.get('closedAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._children = [TrackerItem(**ti, client=self._client) for ti in kwargs.get('children', [])]
			self._custom_fields = kwargs.get('customFields')
			self._priority = kwargs.get('priority')
			self._status = kwargs.get('status')
			self._categories = kwargs.get('categories')
			self._subjects = kwargs.get('subjects')
			self._resolutions = kwargs.get('resolutions')
			self._severities = kwargs.get('severities')
			self._teams = kwargs.get('teams')
			self._versions = kwargs.get('versions')
			self._ordinal = kwargs.get('ordinal')
			self._type_name = kwargs.get('typeName')
			self._comments = kwargs.get('comments')
			self._tags = kwargs.get('tags')
			self._loaded = True

	@property
	def id(self) -> int:
		""""""
		return self._id

	@property
	def name(self) -> str:
		""""""
		return self._name
	
	@property
	@loadable
	def tracker(self) -> Tracker:
		""""""
		return self._tracker

	@property
	@loadable
	def description(self) -> str | None:
		""""""
		return self._description

	@property
	@loadable
	def description_format(self) -> str | None:
		""""""
		return self._description_format

	@property
	@loadable
	def created_at(self) -> datetime | None:
		""""""
		return self._created_at

	@property
	@loadable
	def created_by(self) -> User | None:
		""""""
		return self._created_by

	@property
	@loadable
	def modified_at(self) -> datetime | None:
		""""""
		return self._modified_at

	@property
	@loadable
	def modified_by(self) -> User | None:
		""""""
		return self._modified_by

	@property
	@loadable
	def parent(self) -> TrackerItem | None:
		""""""
		return self._parent

	@property
	@loadable
	def version(self) -> int | None:
		""""""
		return self._version

	@property
	@loadable
	def assigned_to(self) -> list[User] | None:
		""""""
		return self._assigned_to

	@property
	@loadable
	def closed_at(self) -> datetime | None:
		""""""
		return self._closed_at

	@property
	@loadable
	def children(self) -> list[TrackerItem] | None:
		""""""
		return self._children

	@property
	@loadable
	def custom_fields(self) -> list[dict[str, Any]] | None:
		""""""
		return self._custom_fields

	@property
	@loadable
	def priority(self) -> list[dict[str, Any]] | None:
		""""""
		return self._priority

	@property
	@loadable
	def status(self) -> list[dict[str, Any]] | None:
		""""""
		return self._status

	@property
	@loadable
	def categories(self) -> list[dict[str, Any]] | None:
		""""""
		return self._categories

	@property
	@loadable
	def subjects(self) -> list[dict[str, Any]] | None:
		""""""
		return self._subjects

	@property
	@loadable
	def resolutions(self) -> list[dict[str, Any]] | None:
		""""""
		return self._resolutions

	@property
	@loadable
	def severities(self) -> list[dict[str, Any]] | None:
		""""""
		return self._severities

	@property
	@loadable
	def teams(self) -> list[dict[str, Any]] | None:
		""""""
		return self._teams

	@property
	@loadable
	def versions(self) -> list[dict[str, Any]] | None:
		""""""
		return self._versions

	@property
	@loadable
	def ordinal(self) -> int | None:
		""""""
		return self._ordinal

	@property
	@loadable
	def type_name(self) -> str | None:
		""""""
		return self._type_name

	@property
	@loadable
	def comments(self) -> list[dict[str, Any]] | None:
		""""""
		return self._comments

	@property
	@loadable
	def tags(self) -> list[dict[str, Any]] | None:
		""""""
		return self._tags
	
	def _load(self):
		"""Loads the rest of the items's data. When an item is fetched using 
		`Tracker.get_items` only the ID and Name of the item are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the item information if it is 
		needed."""