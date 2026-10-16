from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger

from . import Project, Tracker

class Baseline:
	"""Represents a baseline in codebeamer."""

	if TYPE_CHECKING:
		_description: str
		_description_format: str
		_id: int
		_name: str
		_project: Project
		_tracker: Tracker | None

	def __init__(self, id: int, name: str, **kwargs):
		self._id = id
		self._name = name
		...

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
	def name(self) -> str:
		return self._name

	@property
	def project(self) -> Project:
		return self._project

	@property
	def tracker(self) -> Tracker | None:
		return self._tracker
	
	def _load(self):
		...
