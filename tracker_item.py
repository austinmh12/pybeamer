from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient
from .user import User
from .fields import Field, FieldDefinition
from .utils import loadable, clamp, pages

if TYPE_CHECKING:
	from .tracker import Tracker

class TrackerItem:
	"""Represents a tracker item in codeBeamer."""
	if TYPE_CHECKING:
		_accrued_millis: int | None
		_areas: list[dict[str, Any]] | None # TODO: Area
		_assigned_at: datetime | None
		_end_date: datetime | None
		_estimated_millis: int | None
		_formality: dict[str, Any] | None # TODO: Formality
		_owners: list[User] | None
		_platforms: list[dict[str, Any]] | None # TODO: Platform
		_release_method: dict[str, Any] | None # TODO: ReleaseMethod
		_spent_millis: int | None
		_start_date: datetime | None
		_story_points: int | None
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
		_custom_fields: list[Field] | None
		_priority: Field | None
		_status: Field | None
		_categories: list[Field] | None
		_subjects: list[Field] | None
		_resolutions: list[Field] | None
		_severities: list[Field] | None
		_teams: list[Field] | None
		_versions: list[dict[str, Any]] | None # TODO: Version
		_ordinal: int | None
		_type_name: str | None
		_comments: list[dict[str, Any]] | None # TODO: Comment
		_tags: list[dict[str, Any]] | None # TODO: Tag
		_fields: list[Field]
		_loaded: bool

	def __init__(self, id: int, name: str, *args, **kwargs):
		# TODO: Refactor everything after client into _load()
		# Initial setup of the object
		prop_defaults = {k: None for k in self.__class__.__annotations__}
		self.__dict__.update(prop_defaults)
		# Want these to have standard values
		self._fields = list() 
		self._loaded = False

		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# Want to try and get this regardless of type since it can come from the Tracker class
		self._tracker = kwargs.get('tracker')
		# Want to try and get this regardless of type since it can come from the TrackerItem class
		parent = kwargs.get('parent')
		if isinstance(parent, TrackerItem):
			self._parent = parent
		elif isinstance(parent, dict):
			self._parent = TrackerItem(**parent, client=self._client)
		else:
			self._parent = None
		# type only appears in GET /trackers/{trackerId}/items
		_type = kwargs.get('type')
		if not isinstance(_type, str):
			self._load(kwargs)

	@property
	def id(self) -> int:
		"""The ID of the item."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the item."""
		return self._name
	
	@property
	@loadable
	def tracker(self) -> Tracker:
		"""The tracker the item belongs to."""
		from .tracker import Tracker
		if self._tracker is not None and not isinstance(self._tracker, Tracker):
			self._tracker = Tracker(**self._tracker, client=self._client)
		return self._tracker

	@property
	@loadable
	def description(self) -> str | None:
		"""The item's description."""
		return self._description

	@property
	@loadable
	def description_format(self) -> str | None:
		"""The format of the item's description."""
		return self._description_format

	@property
	@loadable
	def created_at(self) -> datetime | None:
		"""The datetime the item was created at."""
		return self._created_at

	@property
	@loadable
	def created_by(self) -> User | None:
		"""The user who created the item."""
		return self._created_by

	@property
	@loadable
	def modified_at(self) -> datetime | None:
		"""The datetime the item was last modified at."""
		return self._modified_at

	@property
	@loadable
	def modified_by(self) -> User | None:
		"""The user that last modified the item."""
		return self._modified_by

	@property
	@loadable
	def parent(self) -> TrackerItem | None:
		"""The parent item to this item."""
		return self._parent

	@property
	@loadable
	def version(self) -> int | None:
		"""The current version of the item."""
		return self._version

	@property
	@loadable
	def assigned_to(self) -> list[User] | None:
		"""A list of users this item is assigned to."""
		return self._assigned_to

	@property
	@loadable
	def closed_at(self) -> datetime | None:
		"""The datetime this item was closed."""
		return self._closed_at

	@property
	@loadable
	def children(self) -> list[TrackerItem] | None:
		"""A list of this item's children. Only has the first 25 until `TrackerItem.get_children` is called."""
		return self._children

	@property
	@loadable
	def custom_fields(self) -> list[Field] | None:
		"""A list of all the custom fields on this item."""
		return self._custom_fields

	@property
	@loadable
	def priority(self) -> Field | None:
		"""The item's priority."""
		return self._priority

	@property
	@loadable
	def status(self) -> Field | None:
		"""The status of the item."""
		return self._status

	@property
	@loadable
	def categories(self) -> list[Field] | None:
		"""A list of categories for this item."""
		return self._categories

	@property
	@loadable
	def subjects(self) -> list[Field] | None:
		"""A list of subjects for this item."""
		return self._subjects

	@property
	@loadable
	def resolutions(self) -> list[Field] | None:
		"""A list of the resolutions for this item."""
		return self._resolutions

	@property
	@loadable
	def severities(self) -> list[Field] | None:
		"""A list of the severities for this item."""
		return self._severities

	@property
	@loadable
	def teams(self) -> list[Field] | None:
		"""A list of the teams for this item."""
		return self._teams

	@property
	@loadable
	def versions(self) -> list[dict[str, Any]] | None:
		"""A list of the historical versions of this item."""
		return self._versions

	@property
	@loadable
	def ordinal(self) -> int | None:
		"""The position of this item relative to it's siblings."""
		return self._ordinal

	@property
	@loadable
	def type_name(self) -> str | None:
		"""The type of the item."""
		return self._type_name

	@property
	@loadable
	def comments(self) -> list[dict[str, Any]] | None:
		"""A list of the comments on this item."""
		return self._comments

	@property
	@loadable
	def tags(self) -> list[dict[str, Any]] | None:
		"""A list of applied tags for this item."""
		return self._tags
	
	@property
	@loadable
	def accrued_millis(self) -> int | None:
		"""The total accrued work time on this item in milliseconds."""
		return self._accrued_millis

	@property
	@loadable
	def areas(self) -> list[dict[str]] | None:
		"""A list of the areas this item applies to."""
		return self._areas

	@property
	@loadable
	def assigned_at(self) -> datetime | None:
		"""The datetime the item was assigned."""
		return self._assigned_at

	@property
	@loadable
	def end_date(self) -> datetime | None:
		"""The datetime work on this item ended."""
		return self._end_date

	@property
	@loadable
	def estimated_millis(self) -> int | None:
		"""The total estimated time of work for this item in milliseconds."""
		return self._estimated_millis

	@property
	@loadable
	def formality(self) -> dict[str, Any] | None:
		"""The formality of this item."""
		return self._formality

	@property
	@loadable
	def owners(self) -> list[User] | None:
		"""A list of the users that own this item."""
		return self._owners

	@property
	@loadable
	def platforms(self) -> list[dict[str, Any]] | None:
		"""The platforms for the item."""
		return self._platforms

	@property
	@loadable
	def release_method(self) -> dict[str, Any] | None:
		"""The release method for the item."""
		return self._release_method

	@property
	@loadable
	def spent_millis(self) -> int | None:
		"""The total time spent working on this item in milliseconds."""
		return self._spent_millis

	@property
	@loadable
	def start_date(self) -> datetime | None:
		"""The datetime work started on this item."""
		return self._start_date

	@property
	@loadable
	def story_points(self) -> int | None:
		"""The number of story points assigned to this item."""
		return self._story_points
	
	@property
	def json(self) -> dict[str, Any]:
		"""JSON representation of the item."""
		# TODO

	def _load(self, data: dict[str, Any] = None):
		"""Loads the rest of the items's data. When an item is fetched using 
		`Tracker.get_items` only the ID and Name of the item are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the item information if it is 
		needed."""
		if self._loaded:
			logger.info('Item already loaded, ignoring...')
			return
		if not data:
			data: dict[str, Any] = self._client.get(f'items/{self.id}')
		from .tracker import Tracker
		if not isinstance(self._tracker, Tracker):
			self._tracker = Tracker(**data.get('tracker'), client=self._client)
		
		# Cache field data first
		self._fields = self.get_fields()
		
		# Rest of the system fields
		self._accrued_millis = data.get('accruedMillis')
		self._areas = data.get('areas')
		assigned_at = data.get('assignedAt')
		self._assigned_at = datetime.strptime(assigned_at, '%Y-%m-%dT%H:%M:%S.%f') if assigned_at else None
		end_date = data.get('endDate')
		self._end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%f') if end_date else None
		self._estimated_millis = data.get('estimatedMillis')
		self._formality = data.get('formality')
		self._owners = data.get('owners')
		self._platforms = data.get('platforms')
		self._release_method = data.get('releaseMethod')
		self._spent_millis = data.get('spentMillis')
		start_date = data.get('startDate')
		self._start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%f') if start_date else None
		self._story_points = data.get('storyPoints')
		self._description = data.get('description')
		self._description_format = data.get('descriptionFormat')
		self._created_at = datetime.strptime(data.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._created_by = User(**data.get('createdBy'), client=self._client)
		self._modified_at = datetime.strptime(data.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._modified_by = User(**data.get('modifiedBy'), client=self._client)

		# Want to link parents together
		parent = data.get('parent')
		if isinstance(parent, TrackerItem):
			self._parent = parent
		elif isinstance(parent, dict):
			self._parent = TrackerItem(**parent, client=self._client, tracker=self._tracker)
		else:
			self._parent = None
		
		self._version = data.get('version')
		self._assigned_to = data.get('assignedTo')
		closed_at = data.get('closedAt')
		self._closed_at = datetime.strptime(closed_at, '%Y-%m-%dT%H:%M:%S.%f') if closed_at else None
		self._children = [TrackerItem(**ti, client=self._client, parent=self, tracker=self._tracker) for ti in data.get('children', [])]
		
		# Fetch the field from the cached fields on load.
		custom_fields: list[dict[str, Any]] = data.get('customFields')
		self._custom_fields = []
		for custom_field in custom_fields:
			field = self.get_field(custom_field.get('id'))
			if field:
				self._custom_fields.append(field)
		
		# These are all fields that exist in the _fields prop but no editable information is provided
		# Fetch them from the _fields property to get that info
		self._priority = Field(**data.get('priority'), client=self._client, item_id=self.id)
		priority_ref = self._fields[self._fields.index(self._priority)]
		if priority_ref:
			self._priority._editable = priority_ref._editable
		self._status = Field(**data.get('status'), client=self._client, item_id=self.id)
		status_ref = self._fields[self._fields.index(self._status)]
		if status_ref:
			self._status._editable = status_ref._editable

		# ! These list[Field] props are actually not lists, but ChoiceFields
		# TODO above
		self._categories = [Field(**c, client=self._client, item_id=self.id) for c in data.get('categories')]
		self._subjects = [Field(**s, client=self._client, item_id=self.id) for s in data.get('subjects')]
		self._resolutions = [Field(**r, client=self._client, item_id=self.id) for r in data.get('resolutions')]
		self._severities = [Field(**s, client=self._client, item_id=self.id) for s in data.get('severities')]
		self._teams = [Field(**t, client=self._client, item_id=self.id) for t in data.get('teams')]
		
		self._versions = data.get('versions')
		self._ordinal = data.get('ordinal')
		self._type_name = data.get('typeName')
		self._comments = data.get('comments')
		self._tags = data.get('tags')
		self._loaded = True

	def get_children(self, page: int = 0, page_size: int = 25) -> list[TrackerItem]:
		"""Fetches all the child items of the current item. Updates the `TrackerItem.children` field 
		as well.

		Params:
		page — The page number to fetch if you want a specific page of items. If 0 then all items are fetched. — int(0)
		page_size — The number of results per page. Must be between 1 and 500. — int(25)
		
		Returns:
		list[`TrackerItem`] — A list of the child items to this item."""
		fetch_all = page == 0
		if fetch_all:
			page = 1
		page_size = clamp(page_size, 1, 500) # Clamp page_size between 1 and 500
		params = {'page': page, 'pageSize': page_size}
		items: list[TrackerItem] = []
		item_data = self._client.get(f'items/{self.id}/children', params=params)
		total_pages = pages(item_data['total'], page_size)
		items.extend([TrackerItem(**ti, client=self._client, tracker=self) for ti in item_data['itemRefs']])
		if fetch_all:
			while params['page'] < total_pages:
				params['page'] += 1
				item_data = self._client.get(f'items/{self.id}/children', params=params)
				items.extend([TrackerItem(**ti, client=self._client, tracker=self.tracker, parent=self) for ti in item_data['itemRefs']])
		self._children.extend(items)
		self._children = list(set(self._children))
		return items

	def update_children(self, mode: str):
		"""Insert, replace, or remove children from the item."""
		# PATCH items/{self.id}/children

	def add_child(self, item: int | TrackerItem):
		"""Add an item as a child to this item."""
		# POST items/{self.id}/children

	def get_fields(self) -> list[Field]:
		"""Gets the field information for the item. This groups the fields into four 
		categories: editable, editable table, read-only, and read-only table fields."""
		# GET items/{self.id}/fields
		fields: list[Field] = []
		field_data: dict[str, Any] = self._client.get(f'items/{self.id}/fields')
		fields.extend([Field(**f, client=self._client, editable=True, item_id=self.id) for f in field_data['editableFields']])
		fields.extend([Field(**f, client=self._client, editable=False, item_id=self.id) for f in field_data['readOnlyFields']])
		return fields
	
	def get_field(self, field: str | int) -> Field:
		"""Gets the field on the item."""
		if not self._fields:
			self._fields = self.get_fields()
		if isinstance(field, int):
			field_dict = {f.id: f for f in self._fields}
		elif isinstance(field, str):
			field_dict = {f.name: f for f in self._fields}
		else:
			raise TypeError
		return field_dict.get(field)
	
	def update_field(self, field: str | int, value: Any):
		"""Shortcut for calling `TrackerItem.get_field(field)` then `Field.value = value` with 
		the added benefit of updating the item's cached fields so `TrackerItem.refresh` doesn't 
		need to be called to see the updated value."""
		field: Field = self.get_field(field)
		field.value = value
		self._fields.remove(field)
		self._fields.append(field)

	def get_field_definition(self, field: str | int) -> FieldDefinition:
		"""Fetches a specific field from the tracker this item is in."""
		return self.tracker.get_field(field)
	
	def refresh(self):
		"""Refreshes all the information on the item."""
		self._load()

	def delete(self):
		"""Deletes the current tracker item."""
		self._client.delete(f'items/{self.id}')

	def update(self):
		"""Updates the current item. Best used when updating multiple fields at the same time."""
		# TODO: This will bypass `Field.value` and access `Field._value` directly, doing it's own type checking
		# self.json needs to be done first because you have to PUT the entire object

	def create_association(self, other: TrackerItem):
		"""Creates an association with the other tracker item."""
		# TODO
		# ? These aren't upstream/downstream references, but the "relates to" type things

	def remove_association(self, other: TrackerItem):
		"""Removes an association with the other tracker item."""
		# TODO

	def __repr__(self) -> str:
		return f'TrackerItem(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, TrackerItem) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, TrackerItem) and self.id < o.id
	
	def __hash__(self) -> int:
		return hash(self.id)