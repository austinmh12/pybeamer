from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from . import User

class BackgroundJob:
	"""Represents a background job in codeBeamer."""

	if TYPE_CHECKING:
		_background_job_status: str
		_background_job_type: str
		_created_at: datetime
		_description: str
		_finished_at: datetime
		_id: int
		_status_info: dict[str, Any] # TODO: BackgroundJobStatus
		_steps: list[dict[str, Any]] # TODO: list[BackgroundJobStep]
		_submitted_by: User

	def __init__(self, id: int, **kwargs):
		self._id = id
		...

	@property
	def background_job_status(self) -> str:
		return self._background_job_status

	@property
	def background_job_type(self) -> str:
		return self._background_job_type

	@property
	def created_at(self) -> datetime:
		return self._created_at

	@property
	def description(self) -> str:
		return self._description

	@property
	def finished_at(self) -> datetime:
		return self._finished_at

	@property
	def id(self) -> int:
		return self._id

	@property
	def status_info(self) -> dict[str, Any]:
		return self._status_info

	@property
	def steps(self) -> list[dict[str, Any]]:
		return self._steps

	@property
	def submitted_by(self) -> User:
		return self._submitted_by
