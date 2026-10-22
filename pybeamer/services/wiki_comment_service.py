from ..api_client import APIClient

class WikiCommentService:
	"""Service layer for Wiki Comment REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/wikipages/{wikiId}/attachments
	def get_wikipage_attachments(self, wiki: int): ...
	# POST /v3/wikipages/{wikiId}/comments
	def add_wikipage_comment(self, wiki: int, comment: str, **kwargs): ...