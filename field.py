from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger

from .rest_client import RestClient
from .utils import loadable

if TYPE_CHECKING:
	from .tracker import Tracker

class Field:
	"""Represents a field in codeBeamer."""
	if TYPE_CHECKING:
		_tracker: Tracker | None
		_description: str | None
		_formula: str | None
		_hidden: bool | None
		_hide_if_dependency_formula: str | None
		_legacy_rest_name: str | None
		_mandatory_if_dependency_formula: str | None
		_mandatory_in_statuses: list[dict[str, Any]] | None # TODO: Status
		_shared_fields: list[Field] | None
		_title: str | None
		_tracker_item_field: str | None
		_value_model: str | None
		_type: str
		_loaded: bool

	def __init__(self, id: int, name: str, *args, **kwargs):
		self._id: int = id
		self._name: str = name
		self._client: RestClient = kwargs.get('client')
		from .tracker import Tracker
		tracker = kwargs.get('tracker')
		if tracker:
			self._tracker = tracker
		else:
			tracker_id = kwargs.get('trackerId')
			try:
				tracker = Tracker(**self._client.get(f'trackers/{tracker_id}'), client=self._client)
				self._tracker = tracker
			except:
				self._tracker = None
		# type is always present but is FieldReference when lazy loaded
		self._type = kwargs.get('type')
		if self._type == 'FieldReference':
			self._description = None
			self._formula = None
			self._hidden = None
			self._hide_if_dependency_formula = None
			self._legacy_rest_name = None
			self._mandatory_if_dependency_formula = None
			self._mandatory_in_statuses = None
			self._shared_fields = None
			self._title = None
			self._tracker_item_field = None
			self._value_model = None
			self._loaded = False
		else:
			self._description = kwargs.get('description')
			self._formula = kwargs.get('formula')
			self._hidden = kwargs.get('hidden')
			self._hide_if_dependency_formula = kwargs.get('hideIfDependencyFormula')
			self._legacy_rest_name = kwargs.get('legacyRestName')
			self._mandatory_if_dependency_formula = kwargs.get('mandatoryIfDependencyFormula')
			self._mandatory_in_statuses = kwargs.get('mandatoryInStatuses')
			self._shared_fields = [Field(**f, client=self._client) for f in kwargs.get('sharedFields', [])]
			self._title = kwargs.get('title')
			self._tracker_item_field = kwargs.get('trackerItemField')
			self._value_model = kwargs.get('valueModel')
			self._loaded = True

	@property
	def id(self) -> int:
		"""The ID of the field."""
		return self._id
	
	@property
	def name(self) -> str:
		"""The name of the field."""
		return self._name
	
	@property
	@loadable
	def tracker(self) -> Tracker | None:
		"""The tracker the field belongs to."""
		return self._tracker
	
	@property
	@loadable
	def description(self) -> str | None:
		""""""
		return self._description

	@property
	@loadable
	def formula(self) -> str | None:
		""""""
		return self._formula

	@property
	@loadable
	def hidden(self) -> bool | None:
		""""""
		return self._hidden

	@property
	@loadable
	def hide_if_dependency_formula(self) -> str | None:
		""""""
		return self._hide_if_dependency_formula

	@property
	@loadable
	def legacy_rest_name(self) -> str | None:
		""""""
		return self._legacy_rest_name

	@property
	@loadable
	def mandatory_if_dependency_formula(self) -> str | None:
		""""""
		return self._mandatory_if_dependency_formula

	@property
	@loadable
	def mandatory_in_statuses(self) -> list[dict[str, Any]] | None:
		""""""
		return self._mandatory_in_statuses

	@property
	@loadable
	def shared_fields(self) -> list[Field] | None:
		""""""
		return self._shared_fields

	@property
	@loadable
	def title(self) -> str | None:
		""""""
		return self._title

	@property
	@loadable
	def tracker_item_field(self) -> str | None:
		""""""
		return self._tracker_item_field

	@property
	@loadable
	def value_model(self) -> str | None:
		""""""
		return self._value_model

	def _load(self):
		"""Loads the rest of the field's data. When a field is fetched using 
		`Tracker.get_fields` only the ID and Name of the field are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the field information if it is 
		needed."""
		if self._loaded:
			logger.info('Field already loaded, ignoring...')
			return
		field_data: dict[str, Any] = self._client.get(f'trackers/{self.tracker.id}/item/{self.id}')
		self._description = field_data.get('description')
		self._formula = field_data.get('formula')
		self._hidden = field_data.get('hidden')
		self._hide_if_dependency_formula = field_data.get('hideIfDependencyFormula')
		self._legacy_rest_name = field_data.get('legacyRestName')
		self._mandatory_if_dependency_formula = field_data.get('mandatoryIfDependencyFormula')
		self._mandatory_in_statuses = field_data.get('mandatoryInStatuses')
		self._shared_fields = [Field(**f, client=self._client) for f in field_data.get('sharedFields', [])]
		self._title = field_data.get('title')
		self._tracker_item_field = field_data.get('trackerItemField')
		self._value_model = field_data.get('valueModel')
		self._loaded = True