from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from ..rest_client import RestClient
from ..utils import loadable

from . import User

class Group:
	"""Represents a group in codebeamer."""

	if TYPE_CHECKING:
		_created_at: datetime
		_created_by: User
		_description: str
		_id: int
		_modified_at: datetime
		_modified_by: User
		_name: str

	def __init__(self, id: int, name: str, **kwargs):
		self._id = id
		self._name = name
		...

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
	def id(self) -> int:
		return self._id

	@property
	def modified_at(self) -> datetime:
		return self._modified_at

	@property
	def modified_by(self) -> User:
		return self._modified_by

	@property
	def name(self) -> str:
		return self._name
	
	def _load(self, data: dict[str, Any] = None):
		...

	def get_members(self) -> list[User]:
		...