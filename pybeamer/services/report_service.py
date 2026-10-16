from ..api_client import APIClient
from ..models import Report, ReportResult, ReportItem

class ReportService:
	"""Service layer for Report REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def create_report(self, **kwargs) -> Report: ... # TODO: args
	def update_report_settings(self, report: int, **kwargs): ... # TODO: args
	def get_report_items(self, report: int) -> list[ReportItem]: ...
	def get_report_results(self, report: int) -> ReportResult: ...