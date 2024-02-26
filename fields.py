from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient
from .utils import loadable, clamp, pages

if TYPE_CHECKING:
	from .tracker import Tracker

# ? Should this be a base class and break into sub classes?
# ? Or shoud get_options just be implemented and return [] if type != 'ChoiceField'
class FieldDefinition:
	"""Represents a field in a tracker in codeBeamer."""
	if TYPE_CHECKING:
		_tracker: Tracker | None
		_description: str | None
		_formula: str | None
		_hidden: bool | None
		_hide_if_dependency_formula: str | None
		_legacy_rest_name: str | None
		_mandatory_if_dependency_formula: str | None
		_mandatory_in_statuses: list[dict[str, Any]] | None # TODO: Status
		_multiple_values: bool | None
		_options: list[ChoiceValue] | None
		_shared_fields: list[FieldDefinition] | None
		_title: str | None
		_tracker_item_field: str | None
		_value_model: str | None
		_reference_type: str | None
		_type: str
		_loaded: bool

	def __init__(self, id: int, name: str, *args, **kwargs):
		# Initial setup of the object
		prop_defaults = {k: None for k in self.__class__.__annotations__}
		self.__dict__.update(prop_defaults)
		self._loaded = False

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
		if self._type != 'FieldReference':
			self._load(kwargs)

	@property
	def id(self) -> int:
		"""The ID of the field."""
		return self._id
	
	@property
	def name(self) -> str:
		"""The name of the field."""
		return self._name
	
	@property
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
	def shared_fields(self) -> list[FieldDefinition] | None:
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

	def _load(self, data: dict[str, Any] = None):
		"""Loads the rest of the field's data. When a field is fetched using 
		`Tracker.get_fields` only the ID and Name of the field are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the field information if it is 
		needed."""
		if self._loaded:
			logger.info('Field already loaded, ignoring...')
			return
		if not data:
			data: dict[str, Any] = self._client.get(f'trackers/{self.tracker.id}/fields/{self.id}')
		self._description = data.get('description')
		self._formula = data.get('formula')
		self._hidden = data.get('hidden')
		self._hide_if_dependency_formula = data.get('hideIfDependencyFormula')
		self._legacy_rest_name = data.get('legacyRestName')
		self._mandatory_if_dependency_formula = data.get('mandatoryIfDependencyFormula')
		self._mandatory_in_statuses = data.get('mandatoryInStatuses')
		self._multiple_values = data.get('multipleValues')
		options = data.get('options')
		self._options = [ChoiceValue(**o) for o in options] if options else None
		self._shared_fields = [FieldDefinition(**f, client=self._client) for f in data.get('sharedFields', [])]
		self._title = data.get('title')
		self._tracker_item_field = data.get('trackerItemField')
		self._value_model = data.get('valueModel')
		self._loaded = True

	def get_choice(self, choice: str | int) -> ChoiceValue:
		"""Fetches a specific choice value from the list of available choices on this field.
		
		Params:
		choice — The name or ID of the choice value to fetch. — str | int
		
		Returns:
		`ChoiceValue` — An available choice if one exists."""
		if self._type != 'OptionChoiceField':
			return None
		if isinstance(choice, str):
			choice_dict = {c.name: c for c in self._options}
		elif isinstance(choice, int):
			choice_dict = {c.id: c for c in self._options}
		else:
			raise TypeError(f'expected str or int, got {type(choice)}')
		return choice_dict.get(choice)

	def __repr__(self) -> str:
		return f'Field(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, FieldDefinition) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, FieldDefinition) and self.id < o.id
	
class Field:
	"""Represents a field on an item in codeBeamer."""
	if TYPE_CHECKING:
		_value: ChoiceValue | str | int | datetime | None

	def __new__(cls, *args, **kwargs):
		# Return correct subclass based on type param
		other: Field = None
		match kwargs.get('type'):
			case 'IntegerFieldValue':
				other = IntegerField
			case 'ChoiceFieldValue':
				other = ChoiceField
			case 'TextFieldValue':
				other = TextField
			case 'ColorFieldValue':
				other = ColorField
			case 'WikiTextFieldValue':
				other = WikiTextField
			case 'DateFieldValue':
				other = DateField
			case _:
				logger.error(kwargs.get('type'))
		inst = super().__new__(other)
		# logger.debug(f'Field returning {type(inst)}')
		return inst

	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		self._id: int = fieldId
		self._name: str = name
		self._type: str = kwargs.get('type')
		self._shared_field_names: list[str] = kwargs.get('sharedFieldNames')
		self._editable: bool = kwargs.get('editable')
		self._client: RestClient = kwargs.get('client')
		self._item_id: int = kwargs.get('item_id')

	@property
	def id(self) -> str:
		""""""
		return self._id

	@property
	def name(self) -> str:
		""""""
		return self._name

	@property
	def type(self) -> str:
		""""""
		return self._type

	@property
	def shared_field_names(self) -> str:
		""""""
		return self._shared_field_names
	
	@property
	def value(self):
		pass

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, Field) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, Field) and self.id < o.id
	
	def __hash__(self) -> int:
		return hash(self.id)

class ChoiceField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		self._value: list[ChoiceValue] = [ChoiceValue(**cv) for cv in kwargs.get('values')]
		# Caching for the choices since they won't change on an item
		self._choices: list[ChoiceValue] = None

	@property
	def value(self) -> str:
		""""""
		return self._value

	@value.setter
	def value(self, v: ChoiceValue | list[ChoiceValue]):
		if not self._editable:
			raise Exception('Not editable')
		if isinstance(v, ChoiceValue):
			v = [v]
		for _v in v:
			if not isinstance(_v, ChoiceValue):
				raise TypeError(f'expected ChoiceValue, got {type(_v)}')
			# Should be cached since the user would need to get choices first
			available_choices = self.get_choices()
			if _v not in available_choices:
				raise ValueError(f'{_v} is not an available choice')
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'values': [_v.json for _v in v]
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)

	def get_choices(self) -> list[ChoiceValue]:
		"""Fetches all the available choices for this field on an item."""
		# ! Decision here is to just get all of them and not allow the user to paginate
		if not self._choices:
			page = 1
			page_size = 500
			params = {'page': page, 'pageSize': page_size}
			choices: list[ChoiceValue] = []
			choice_data = self._client.get(f'items/{self._item_id}/fields/{self.id}/options', params=params)
			total_pages = pages(choice_data['total'], page_size)
			choices.extend([ChoiceValue(**cv) for cv in choice_data['references']])
			while params['page'] < total_pages:
				params['page'] += 1
				choice_data = self._client.get(f'items/{self.id}/children', params=params)
				choices.extend([ChoiceValue(**cv) for cv in choice_data['references']])
			self._choices = choices
		return self._choices
	
	def get_choice(self, choice: str | int) -> ChoiceValue:
		"""Fetches a specific choice value from the list of available choices on this field.
		
		Params:
		choice — The name or ID of the choice value to fetch. — str | int
		
		Returns:
		`ChoiceValue` — An available choice if one exists."""
		choices = self.get_choices()
		if isinstance(choice, str):
			choice_dict = {c.name: c for c in choices}
		elif isinstance(choice, int):
			choice_dict = {c.id: c for c in choices}
		else:
			raise TypeError(f'expected str or int, got {type(choice)}')
		return choice_dict.get(choice)

class ChoiceValue:
	def __init__(self, id: int, name: str, type: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._type: str = type
		# For UserReference types
		self._email: str | None = kwargs.get('email')

	@property
	def id(self) -> int:
		""""""
		return self._id

	@property
	def name(self) -> str:
		""""""
		return self._name

	@property
	def type(self) -> str:
		""""""
		return self._type

	@property
	def email(self) -> str:
		""""""
		return self._email
	
	@property
	def json(self) -> dict[str, Any]:
		"""JSON representation of the choice value"""
		ret = {'id': self.id, 'name': self.name, 'type': 'ChoiceOptionReference'}
		if self.email:
			ret['email'] = self.email
		return ret

	def __repr__(self) -> str:
		return f'ChoiceValue(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, ChoiceValue) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, ChoiceValue) and self.id < o.id
	
	def __hash__(self) -> int:
		return hash(self.id)

class IntegerField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		self._value: int | None = kwargs.get('value')

	@property
	def value(self) -> int:
		""""""
		return self._value

	@value.setter
	def value(self, v: int):
		if not self._editable:
			raise Exception('Not editable')
		if not isinstance(v, int):
			raise TypeError(f'expected int, got {type(v)}')
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'value': v
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)

class TextField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		self._value: str | None = kwargs.get('value')

	@property
	def value(self) -> str:
		""""""
		return self._value

	@value.setter
	def value(self, v: str):
		if not self._editable:
			raise Exception('Not editable')
		v = str(v)
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'value': v
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)

class ColorField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		self._value: str | None = kwargs.get('value')

	@property
	def value(self) -> str:
		""""""
		return self._value

	@value.setter
	def value(self, v: str):
		if not self._editable:
			raise Exception('Not editable')
		# !LOOKUP value probably needs to be in #RRBBGG format
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'value': v
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)

class WikiTextField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		self._value: str | None = kwargs.get('value')

	@property
	def value(self) -> str:
		""""""
		return self._value

	@value.setter
	def value(self, v: str):
		if not self._editable:
			raise Exception('Not editable')
		v = str(v)
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'value': v
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)

class DateField(Field):
	def __init__(self, fieldId: int, name: str, *args, **kwargs):
		super().__init__(fieldId, name, *args, **kwargs)
		value = kwargs.get('value')
		self._value: datetime | None = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f') if value else None

	@property
	def value(self) -> datetime:
		""""""
		return self._value

	@value.setter
	def value(self, v: datetime):
		if not self._editable:
			raise Exception('Not editable')
		if not isinstance(v, datetime):
			raise TypeError(f'expected datetime, got {type(v)}')
		self._value = v
		data = {
			'fieldValues': [
				{
					'fieldId': self.id,
					'name': self.name,
					'type': self.type,
					'value': v.strftime('%Y-%m-%dT%H:%M:%S.%f')
				}
			]
		}
		self._client.put(f'items/{self._item_id}/fields?quietMode=true', json_=data)
