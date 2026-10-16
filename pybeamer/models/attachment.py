from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from ..rest_client import RestClient
from ..utils import loadable

from . import User

class Attachment:
	"""Represents an attachment in codeBeamer."""

	if TYPE_CHECKING:
		_created_at: datetime
		_created_by: User
		_description: str
		_description_format: str
		_id: int
		_modified_at: datetime
		_modified_by: User
		_name: str
		_sha_512: str
		_size: int
		_version: int

	def __init__(self, id: int, name: str, **kwargs):
		self._id = id
		self._name = name
		self._client: RestClient = kwargs.get('client')
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
	def description_format(self) -> str:
		return self._description_format

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

	@property
	def sha_512(self) -> str:
		return self._sha_512

	@property
	def size(self) -> int:
		return self._size

	@property
	def version(self) -> int:
		return self._version

	def _load(self, data: dict[str, Any]):
		...

	def delete(self):
		...

	def content(self):
		...

	def update(self):
		...

	def history(self):
		...

	def restore(self):
		...