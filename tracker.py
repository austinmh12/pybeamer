from __future__ import annotations
from typing import TYPE_CHECKING, Any, get_args

from datetime import datetime
from loguru import logger

from .rest_client import RestClient
from .user import User
from .tracker_item import TrackerItem
from .fields import FieldDefinition, Field
from .utils import loadable, clamp, pages, snake_to_camel

if TYPE_CHECKING:
	from .projects import Project

class Tracker:
	"""Represents a tracking in codeBeamer."""
	if TYPE_CHECKING:
		_description: str | None
		_description_format: str | None
		_key_name: str | None
		_version: int | None
		_created_at: datetime | None
		_created_by: User | None
		_modified_at: datetime | None
		_modified_by: User | None
		_type: dict[str, Any] | None # TODO: TrackerType
		_deleted: bool | None
		_hidden: bool | None
		_color: str | None
		_using_workflow: bool | None
		_only_workflow_can_create_new_referring_item: bool | None
		_using_quick_transitions: bool | None
		_default_show_ancestor_items: bool | None
		_default_show_descendant_items: bool | None
		_project: Project | None
		_available_as_template: bool | None
		_shared_in_working_set: bool | None
		_loaded: bool

	def __init__(self, id: int, name: str, **kwargs):
		# Initial setup of the object
		prop_defaults = {k: None for k in self.__class__.__annotations__}
		self.__dict__.update(prop_defaults)
		self._loaded = False

		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# Want to try and get this regardless of type since it can come from the Project class
		self._project = kwargs.get('project')
		# type only appears in GET /projects/{projectId}/trackers
		_type = kwargs.get('type')
		if not isinstance(_type, str):
			# if type is a str then no other information is present
			self._load(kwargs)

	@property
	def id(self) -> int:
		"""The ID of the tracker."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the tracker."""
		return self._name

	@property
	@loadable
	def description(self) -> str | None:
		"""The description of the tracker."""
		return self._description

	@property
	@loadable
	def description_format(self) -> str | None:
		"""The format of the tracker's description."""
		return self._description_format

	@property
	@loadable
	def key_name(self) -> str | None:
		"""The tracker's key name."""
		return self._key_name

	@property
	@loadable
	def version(self) -> int | None:
		"""The version of the tracker."""
		return self._version

	@property
	@loadable
	def created_at(self) -> datetime | None:
		"""The datetime the tracker was created."""
		return self._created_at

	@property
	@loadable
	def created_by(self) -> User | None:
		"""The user that created the tracker."""
		return self._created_by

	@property
	@loadable
	def modified_at(self) -> datetime | None:
		"""The datetime the tracker was last modified at."""
		return self._modified_at

	@property
	@loadable
	def modified_by(self) -> User | None:
		"""The user that last modified the tracker."""
		return self._modified_by

	@property
	@loadable
	def type(self) -> dict[str, Any] | None: # TODO: TrackerType 
		"""The type of tracker."""
		return self._type

	@property
	@loadable
	def deleted(self) -> bool | None:
		"""Flag for whether the tracker has been deleted or not."""
		return self._deleted

	@property
	@loadable
	def hidden(self) -> bool | None:
		"""Flag for whether the tracker has been hidden or not."""
		return self._hidden

	@property
	@loadable
	def color(self) -> str | None:
		"""The tracker's default color."""
		return self._color

	@property
	@loadable
	def using_workflow(self) -> bool | None:
		"""Flag for whether the tracker is using a workflow or not."""
		return self._using_workflow

	@property
	@loadable
	def only_workflow_can_create_new_referring_item(self) -> bool | None:
		"""Flag for whether the workflow is the only way to create items that reference other items."""
		return self._only_workflow_can_create_new_referring_item

	@property
	@loadable
	def using_quick_transitions(self) -> bool | None:
		"""Flag for whether the tracker uses quick transitions."""
		return self._using_quick_transitions

	@property
	@loadable
	def default_show_ancestor_items(self) -> bool | None:
		"""Flag for whether the tracker shows ancestors of items."""
		return self._default_show_ancestor_items

	@property
	@loadable
	def default_show_descendant_items(self) -> bool | None:
		"""Flag for whether the tracker shows descendants of items."""
		return self._default_show_descendant_items

	@property
	@loadable
	def project(self) -> Project | None:
		"""The project the tracker belongs to."""
		return self._project

	@property
	@loadable
	def available_as_template(self) -> bool | None:
		"""Flag for whether the tracker is a template tracker."""
		return self._available_as_template

	@property
	@loadable
	def shared_in_working_set(self) -> bool | None:
		"""Flag for whether this tracker is sharable in a working set."""
		return self._shared_in_working_set

	def _load(self, data: dict[str, Any] = None):
		"""Loads the rest of the tracker's data. When a tracker is fetched using 
		`Project.get_trackers` only the ID and Name of the tracker are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the tracker information if it is 
		needed."""
		if self._loaded:
			logger.info('Tracker already loaded, ignoring...')
			return
		if not data:
			data: dict[str, Any] = self._client.get(f'trackers/{self.id}')
		from .projects import Project
		if not isinstance(self._project, Project):
			self._project = Project(**data.get('project'), client=self._client)
		self._description = data.get('description')
		self._description_format = data.get('descriptionFormat')
		self._key_name = data.get('keyName')
		self._version = data.get('version')
		self._created_at = datetime.strptime(data.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._created_by = User(**data.get('createdBy'), client=self._client)
		modified_at = data.get('modifiedAt')
		self._modified_at = datetime.strptime(modified_at, '%Y-%m-%dT%H:%M:%S.%f') if modified_at else None
		modified_by = data.get('modifiedBy')
		self._modified_by = User(**modified_by, client=self._client) if modified_by else None
		self._type = data.get('type')
		self._deleted = data.get('deleted')
		self._hidden = data.get('hidden')
		self._color = data.get('color')
		self._using_workflow = data.get('usingWorkflow')
		self._only_workflow_can_create_new_referring_item = data.get('onlyWorkflowCanCreateNewReferringItem')
		self._using_quick_transitions = data.get('usingQuickTransitions')
		self._default_show_ancestor_items = data.get('defaultShowAncestorItems')
		self._default_show_descendant_items = data.get('defaultShowDescendantItems')
		self._available_as_template = data.get('availableAsTemplate')
		self._shared_in_working_set = data.get('sharedInWorkingSet')
		self._loaded = True

	def get_tracker_items(self, page: int = 0, page_size: int = 25) -> list[TrackerItem]:
		"""Fetches all the items in this tracker.

		Params:
		page — The page number to fetch if you want a specific page of items. If 0 then all items are fetched. — int(0)
		page_size — The number of results per page. Must be between 1 and 500. — int(25)
		
		Returns:
		list[`TrackerItem`] — A list of the items in this tracker."""
		fetch_all = page == 0
		if fetch_all:
			page = 1
		page_size = clamp(page_size, 1, 500) # Clamp page_size between 1 and 500
		params = {'page': page, 'pageSize': page_size}
		items: list[TrackerItem] = []
		item_data = self._client.get(f'trackers/{self.id}/items', params=params)
		total_pages = pages(item_data['total'], page_size)
		items.extend([TrackerItem(**ti, client=self._client, tracker=self) for ti in item_data['itemRefs']])
		if fetch_all:
			while params['page'] < total_pages:
				params['page'] += 1
				item_data = self._client.get(f'trackers/{self.id}/items', params=params)
				items.extend([TrackerItem(**ti, client=self._client, tracker=self) for ti in item_data['itemRefs']])
		return items
	
	def get_items(self, page: int = 0, page_size: int = 25) -> list[TrackerItem]:
		"""Alias for get_tracker_items."""
		return self.get_tracker_items(page=page, page_size=page_size)
	
	def get_fields(self) -> list[FieldDefinition]:
		"""Fetches the available field names for this tracker.
		
		Returns:
		list[`Field`] — A list of fields in this tracker."""
		return [FieldDefinition(**f, client=self._client, tracker=self) for f in self._client.get(f'trackers/{self.id}/fields')]

	def get_field(self, field: str | int) -> FieldDefinition | None:
		"""Fetches detailed information about the field for the tracker.
		
		Params:
		field — The name or ID of the field to fetch. — str | int

		Raises:
		TypeError — A type other than str or int was provided.
		
		Returns:
		`Field` — The field if it exists."""
		if isinstance(field, int):
			return self._get_field_by_id(field)
		elif isinstance(field, str):
			return self._get_field_by_name(field)
		else:
			raise TypeError(f'expected str or int, got {type(field)}')

	def _get_field_by_id(self, id: int) -> FieldDefinition | None:
		try:
			field = FieldDefinition(**self._client.get(f'trackers/{self.id}/fields/{id}'), client=self._client, tracker=self)
			return field
		except Exception as e:
			logger.exception(e)
			return

	def _get_field_by_name(self, name: str) -> FieldDefinition | None:
		fields = {f.name: f for f in self.get_fields()}
		return fields.get(name)
	
	def get_children(self) -> list[TrackerItem]:
		"""Get the immediate descendents of the tracker."""
		# TODO

	def create_tracker_item(
		self,
		name: str,
		description: str,
		description_format: str = 'PlainText',
		parent_id: int = None,
		reference_id: int = None,
		position: str = None,
		**kwargs,
	) -> TrackerItem:
		"""Creates a new tracker item in the current tracker."""
		params = {}
		if parent_id:
			params['parentItemId'] = parent_id
		if reference_id:
			params['referenceItemId'] = reference_id
		if position and position.upper() in ['BEFORE', 'AFTER', 'BELOW']:
			params['position'] = position.upper()
		# ! Need to grab system fields into the top level data level.
		# TODO: Make the second variable of this the API name
		system_fields = {k[1:]: v for k, v in TrackerItem.__annotations__.items()} # remove the _ leading the param
		# ! Need to put non-system fields in the customFields section as a list of Fields
		# Bare minimum required to create the item
		data = {
			'name': name,
			'description': description,
			'descriptionFormat': description_format
		}
		for field, value in kwargs.items():
			if field in system_fields:
				# Needs to go in the top level data
				field_arg_types = get_args(system_fields[field])
				if any([
					str in field_arg_types,
					int in field_arg_types,
					datetime in field_arg_types
				]):
					# Need to convert the system field name from snake_case to camelCase for the JSON
					data[snake_to_camel(field)] = value
				elif Field in field_arg_types:
					# Need to get the type of field from the FieldDefinition using the provided name
					# Build the field json and add it
					field_json = {}
					data[snake_to_camel(field)] = field_json
				elif list[Field] in field_arg_types:
					# Need to get the type of field from the FieldDefinition using the provided name
					# Build the field json and add it
					field_jsons = []
					for val in value:
						field_json = {}
						field_jsons.append(field_json)
					data[snake_to_camel(field)] = field_json
				else:
					# At the moment this is dict[str, Any] but those will be other types
					# ! Not Implemented ATM
					pass
			else:
				# Needs to go in customFields
				if 'customFields' not in data:
					data['customFields'] = []
				# Need field ID, field Name, and field Type
				field_json = {
					'fieldId': 0,
					'name': snake_to_camel(field), # ! NO, it will have to be snake_case to Title Case
					'value': value,
					'type': '*FieldValue' # * would be Choice, Bool, Integer, Text, etc.
				}
				data['customFields'].append(field_json)
		try:
			item = self._client.post(f'trackers/{self.id}/items', json_=data, params=params)
			return TrackerItem(**item, client=self._client, tracker=self)
		except Exception as e:
			logger.exception(e)
			raise e

	def __repr__(self) -> str:
		return f'Tracker(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, Tracker) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, Tracker) and self.id < o.id