from ..api_client import APIClient
from ..models import Tracker, Report

TrackerLike = str | int | Tracker
ReportLike = str | int | Report

class TrackerReportService:
	"""Service layer for Tracker Report REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/trackers/{trackerId}/reports
	def get_tracker_reports(self, tracker: TrackerLike): ...
	# POST /v3/trackers/{trackerId}/reports
	def create_tracker_report(self, tracker: TrackerLike, **kwargs): ...
	# DELETE /v3/trackers/{trackerId}/reports/{reportId}
	def delete_tracker_report(self, tracker: TrackerLike, report: ReportLike): ...
	# PUT /v3/trackers/{trackerId}/reports/{reportId}
	def update_tracker_report(self, tracker: TrackerLike, report: ReportLike, **kwargs): ...
	# GET /v3/trackers/{trackerId}/reports/{reportId}/items
	def get_tracker_report_items(self, tracker: TrackerLike, report: ReportLike): ...
	# GET /v3/trackers/{trackerId}/reports/{reportId}/results
	def get_tracker_report_results(self, tracker: TrackerLike, report: ReportLike): ...