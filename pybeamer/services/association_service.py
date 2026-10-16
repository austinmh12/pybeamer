from typing import Any

from ..api_client import APIClient
from ..models import Association

class AssociationService:
	"""Service layer for Association REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	def create_association(self, **kwargs): ...
	def delete_association(self, association: str | int | Association): ...
	def get_association(self, association: str | int | Association) -> Association | None: ...
	def update_association(self, association: str | int | Association, **updates): ...
	def get_association_history(self, association: str | int | Association) -> list[dict[str, Any]]: ... # TODO: AssociationHistory
	def get_association_types(self) -> list[dict[str, Any]]: ... # TODO: AssociationType
	def get_association_type(self, type: str | int) -> dict[str, Any]: ... # TODO: AssociationType