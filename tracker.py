from __future__ import annotations
from typing import TYPE_CHECKING, Any

from datetime import datetime
from loguru import logger

from .rest_client import RestClient
from .user import User

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

	def __init__(self, id: int, name: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		# Want to try and get this regardless of type since it can come from the Project class
		self._project = kwargs.get('project')
		# type only appears in GET /projects/{trackerId}/trackers
		_type = kwargs.get('type')
		if isinstance(_type, str):
			# if type is present then no other information is present
			self._description = None
			self._description_format = None
			self._key_name = None
			self._version = None
			self._created_at = None
			self._created_by = None
			self._modified_at = None
			self._modified_by = None
			self._type = None
			self._deleted = None
			self._hidden = None
			self._color = None
			self._using_workflow = None
			self._only_workflow_can_create_new_referring_item = None
			self._using_quick_transitions = None
			self._default_show_ancestor_items = None
			self._default_show_descendant_items = None
			self._available_as_template = None
			self._shared_in_working_set = None
		else:
			self._description = kwargs.get('description')
			self._description_format = kwargs.get('descriptionFormat')
			self._key_name = kwargs.get('keyName')
			self._version = kwargs.get('version')
			self._created_at = datetime.strptime(kwargs.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._created_by = User(**kwargs.get('createdBy'), client=self._client)
			self._modified_at = datetime.strptime(kwargs.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
			self._modified_by = User(**kwargs.get('modifiedBy'), client=self._client)
			self._type = kwargs.get('type')
			self._deleted = kwargs.get('deleted')
			self._hidden = kwargs.get('hidden')
			self._color = kwargs.get('color')
			self._using_workflow = kwargs.get('usingWorkflow')
			self._only_workflow_can_create_new_referring_item = kwargs.get('onlyWorkflowCanCreateNewReferringItem')
			self._using_quick_transitions = kwargs.get('usingQuickTransitions')
			self._default_show_ancestor_items = kwargs.get('defaultShowAncestorItems')
			self._default_show_descendant_items = kwargs.get('defaultShowDescendantItems')
			self._available_as_template = kwargs.get('availableAsTemplate')
			self._shared_in_working_set = kwargs.get('sharedInWorkingSet')

	@property
	def id(self) -> int:
		"""The ID of the tracker."""
		return self._id

	@property
	def name(self) -> str:
		"""The name of the tracker."""
		return self._name

	@property
	def description(self) -> str | None:
		"""The description of the tracker."""
		return self._description

	@property
	def description_format(self) -> str | None:
		"""The format of the tracker's description."""
		return self._description_format

	@property
	def key_name(self) -> str | None:
		"""The tracker's key name."""
		return self._key_name

	@property
	def version(self) -> int | None:
		"""The version of the tracker."""
		return self._version

	@property
	def created_at(self) -> datetime | None:
		"""The datetime the tracker was created."""
		return self._created_at

	@property
	def created_by(self) -> User | None:
		"""The user that created the tracker."""
		return self._created_by

	@property
	def modified_at(self) -> datetime | None:
		"""The datetime the tracker was last modified at."""
		return self._modified_at

	@property
	def modified_by(self) -> User | None:
		"""The user that last modified the tracker."""
		return self._modified_by

	@property
	def type(self) -> dict[str, Any] | None: # TODO: TrackerType 
		"""The type of tracker."""
		return self._type

	@property
	def deleted(self) -> bool | None:
		"""Flag for whether the tracker has been deleted or not."""
		return self._deleted

	@property
	def hidden(self) -> bool | None:
		"""Flag for whether the tracker has been hidden or not."""
		return self._hidden

	@property
	def color(self) -> str | None:
		"""The tracker's default color."""
		return self._color

	@property
	def using_workflow(self) -> bool | None:
		"""Flag for whether the tracker is using a workflow or not."""
		return self._using_workflow

	@property
	def only_workflow_can_create_new_referring_item(self) -> bool | None:
		"""Flag for whether the workflow is the only way to create items that reference other items."""
		return self._only_workflow_can_create_new_referring_item

	@property
	def using_quick_transitions(self) -> bool | None:
		"""Flag for whether the tracker uses quick transitions."""
		return self._using_quick_transitions

	@property
	def default_show_ancestor_items(self) -> bool | None:
		"""Flag for whether the tracker shows ancestors of items."""
		return self._default_show_ancestor_items

	@property
	def default_show_descendant_items(self) -> bool | None:
		"""Flag for whether the tracker shows descendants of items."""
		return self._default_show_descendant_items

	@property
	def project(self) -> Project | None:
		"""The project the tracker belongs to."""
		return self._project

	@property
	def available_as_template(self) -> bool | None:
		"""Flag for whether the tracker is a template tracker."""
		return self._available_as_template

	@property
	def shared_in_working_set(self) -> bool | None:
		"""Flag for whether this tracker is sharable in a working set."""
		return self._shared_in_working_set

	def load(self):
		"""Loads the rest of the tracker's data. When a tracker is fetched using 
		`Project.get_trackers` only the ID and Name of the tracker are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the tracker information if it is 
		needed."""
		if self.key_name:
			logger.info('Tracker already loaded, ignoring...')
			return
		tracker_data: dict[str, Any] = self._client.get(f'trackers/{self.id}')
		self._description = tracker_data.get('description')
		self._description_format = tracker_data.get('descriptionFormat')
		self._key_name = tracker_data.get('keyName')
		self._version = tracker_data.get('version')
		self._created_at = datetime.strptime(tracker_data.get('createdAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._created_by = User(**tracker_data.get('createdBy'), client=self._client)
		self._modified_at = datetime.strptime(tracker_data.get('modifiedAt'), '%Y-%m-%dT%H:%M:%S.%f')
		self._modified_by = User(**tracker_data.get('modifiedBy'), client=self._client)
		self._type = tracker_data.get('type')
		self._deleted = tracker_data.get('deleted')
		self._hidden = tracker_data.get('hidden')
		self._color = tracker_data.get('color')
		self._using_workflow = tracker_data.get('usingWorkflow')
		self._only_workflow_can_create_new_referring_item = tracker_data.get('onlyWorkflowCanCreateNewReferringItem')
		self._using_quick_transitions = tracker_data.get('usingQuickTransitions')
		self._default_show_ancestor_items = tracker_data.get('defaultShowAncestorItems')
		self._default_show_descendant_items = tracker_data.get('defaultShowDescendantItems')
		self._available_as_template = tracker_data.get('availableAsTemplate')
		self._shared_in_working_set = tracker_data.get('sharedInWorkingSet')

	def __repr__(self) -> str:
		return f'Tracker(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, Tracker) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, Tracker) and self.id < o.id