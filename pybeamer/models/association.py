from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from ..rest_client import RestClient
from ..utils import loadable

from . import User, TrackerItem

class Association:
	"""Represents an association in codeBeamer."""

	if TYPE_CHECKING:
		_baseline_id: int
		_bi_directional_propagation: bool
		_created_at: datetime
		_created_by: User | None
		_description: str
		_description_format: str # Enum of PlainText, Html, Wiki
		_from: TrackerItem # {id: int, name: str, type: str}
		_id: int
		_name: str
		_propagating_dependencies: bool
		_propagating_suspects: bool
		_reverse_propagation: bool
		_to: TrackerItem # Same as _from
		_url: str
		# _type: Same as _from, used for loading?

	def __init__(self, id: int, name: str, **kwargs):
		self._id = id
		self._name = name
		self._client: RestClient = kwargs.get('client')
		...

	@property
	def baseline_id(self) -> int:
		return self._baseline_id

	@property
	def bi_directional_propagation(self) -> bool:
		return self._bi_directional_propagation

	@property
	def created_at(self) -> datetime:
		return self._created_at

	@property
	def created_by(self) -> User:
		return self._created_by

	@property
	def description(self) -> str:
		return self._description

	@property
	def description_format(self) -> str:
		return self._description_format

	@property
	def from_(self) -> TrackerItem:
		return self._from

	@property
	def id(self) -> int:
		return self._id

	@property
	def name(self) -> str:
		return self._name

	@property
	def propagating_dependencies(self) -> bool:
		return self._propagating_dependencies

	@property
	def propagating_suspects(self) -> bool:
		return self._propagating_suspects

	@property
	def reverse_propagation(self) -> bool:
		return self._reverse_propagation

	@property
	def to(self) -> TrackerItem:
		return self._to

	@property
	def url(self) -> str:
		return self._url
	
	def _load(self, data: dict[str, Any] = None):
		...

	def delete(self):
		...

	def update(self):
		...

	def history(self):
		...