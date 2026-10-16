from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger

from . import FieldDefinition, TrackerItem

class Report:
	"""Represents a collection of report settings in codebeamer."""

	if TYPE_CHECKING:
		_cb_ql: str
		_columns: list[ReportColumn]
		_description: str
		_name: str
		_report_id: int
		_show_all_children: bool
		_show_ancestors: bool
		_show_descendants: bool

	def __init__(self, id: int, name: str, **kwargs):
		self._report_id = id
		self._name = name
		...

	@property
	def cb_ql(self) -> str:
		return self._cb_ql

	@property
	def columns(self) -> list[ReportColumn]:
		return self._columns

	@property
	def description(self) -> str:
		return self._description

	@property
	def name(self) -> str:
		return self._name

	@property
	def report_id(self) -> int:
		return self._report_id

	@property
	def show_all_children(self) -> bool:
		return self._show_all_children

	@property
	def show_ancestors(self) -> bool:
		return self._show_ancestors

	@property
	def show_descendants(self) -> bool:
		return self._show_descendants
	
	def update(self):
		...

	def get_items(self, page: int = 0, page_size: int = 25) -> list[ReportItem]:
		...

	def get_results(self, page: int = 0, page_size: int = 25) -> ReportResult:
		...

class ReportColumn:
	"""Represents a resizable column in a report."""

	if TYPE_CHECKING:
		_column_index: int
		_column_width_percentage: float
		_field: FieldDefinition
		_name: str | None
		_type: str | None

	def __init__(self, **kwargs):
		...

	@property
	def column_index(self) -> int:
		return self._column_index

	@property
	def column_width_percentage(self) -> float:
		return self._column_width_percentage

	@property
	def field(self) -> FieldDefinition:
		return self._field
	
	@property
	def name(self) -> str | None:
		return self._name
	
	@property
	def field_type(self) -> str | None:
		return self._type

class ReportItem:
	"""Represents an item from a report."""

	if TYPE_CHECKING:
		_is_real_result: bool
		_item: TrackerItem
		_outline_level: int
	
	def __init__(self, **kwargs):
		...

	@property
	def is_real_result(self) -> bool:
		return self._is_real_result

	@property
	def item(self) -> TrackerItem:
		return self._item

	@property
	def outline_level(self) -> int:
		return self._outline_level

class ReportResult:
	"""Report data model"""
	
	if TYPE_CHECKING:
		_cb_ql: str
		_columns: list[ReportColumn]
		_data: ReportGroup
		_paging_information: dict[str, Any]
		_report: Report
		_show_all_children: bool

	def __init__(self, **kwargs):
		...

	@property
	def cb_ql(self) -> str:
		return self._cb_ql

	@property
	def columns(self) -> list[ReportColumn]:
		return self._columns

	@property
	def data(self) -> ReportGroup:
		return self._data

	@property
	def paging_information(self) -> dict[str, Any]:
		return self._paging_information

	@property
	def report(self) -> Report:
		return self._report

	@property
	def show_all_children(self) -> bool:
		return self._show_all_children

class ReportGroup:
	"""A report group which can contain rows or other groups."""

	if TYPE_CHECKING:
		_aggregates: list[ReportAggregate]
		_count: int
		_grouping_value: str
		_grouping_value_id: int
		_header: str
		_type: str

	def __init__(self, **kwargs):
		...

	@property
	def aggregates(self) -> list[ReportAggregate]:
		return self._aggregates

	@property
	def count(self) -> int:
		return self._count

	@property
	def grouping_value(self) -> str:
		return self._grouping_value

	@property
	def grouping_value_id(self) -> int:
		return self._grouping_value_id

	@property
	def header(self) -> str:
		return self._header

	@property
	def type(self) -> str:
		return self._type

class ReportAggregate:
	"""Aggregated values for a column of a group."""

	if TYPE_CHECKING:
		_average: float
		_column_ref: str
		_maximum: float
		_minimum: float
		_sum: float

	def __init__(self, **kwargs):
		...

	@property
	def average(self) -> float:
		return self._average

	@property
	def column_ref(self) -> str:
		return self._column_ref

	@property
	def maximum(self) -> float:
		return self._maximum

	@property
	def minimum(self) -> float:
		return self._minimum

	@property
	def sum(self) -> float:
		return self._sum