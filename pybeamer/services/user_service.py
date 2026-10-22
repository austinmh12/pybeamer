from ..api_client import APIClient
from ..models import User

UserLike = str | int | User

class UserService:
	"""Service layer for User REST operations."""

	def __init__(self, client: APIClient):
		self._client = client

	#############
	# Endpoints #
	#############
	# GET /v3/users
	def get_users(self) -> list[User]: ...
	# GET /v3/users/{userId}
	def get_user(self, user: UserLike) -> User | None: ...
	# GET /v3/users/findByEmail
	def get_user_by_email(self, email: str) -> User | None: ...
	# GET /v3/users/findByName
	def get_user_by_name(self, name: str) -> User | None: ...
	# POST /v3/users/search
	def search_users(self, **kwargs) -> list[User]: ...