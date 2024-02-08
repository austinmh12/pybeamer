from __future__ import annotations
from typing import TYPE_CHECKING, Any

from loguru import logger
from datetime import datetime

from .rest_client import RestClient

class User:
	"""Represents a user in codeBeamer."""
	if TYPE_CHECKING:
		_email: str | None
		_first_name: str | None
		_last_name: str | None
		_title: str | None
		_company: str | None
		_address: str | None
		_zip: int | None
		_city: str | None
		_state: str | None
		_country: str | None
		_date_format: str | None
		_time_zone: str | None
		_language: str | None
		_phone: str | None
		_skills: list[str] | None
		_registry_date: datetime | None
		_last_login_date: datetime | None
		_status: str | None

	def __init__(self, id: int, name: str, **kwargs):
		self._id: int = id
		self._name: str = name
		self._email: str | None = kwargs.get('email') # Not present for system users
		self._client: RestClient = kwargs.get('client')
		# type only appears in GET /projects
		if kwargs.get('type'):
			# if type is present then no other information is present
			self._first_name = None
			self._last_name = None
			self._title = None
			self._company = None
			self._address = None
			self._zip = None
			self._city = None
			self._state = None
			self._country = None
			self._date_format = None
			self._time_zone = None
			self._language = None
			self._phone = None
			self._skills = None
			self._registry_date = None
			self._last_login_date = None
			self._status = None
		else:
			self._first_name = kwargs.get('firstName')
			self._last_name = kwargs.get('lastName')
			self._title = kwargs.get('title')
			self._company = kwargs.get('company')
			self._address = kwargs.get('address')
			self._zip = kwargs.get('zip')
			self._city = kwargs.get('city')
			self._state = kwargs.get('state')
			self._country = kwargs.get('country')
			self._date_format = kwargs.get('dateFormat')
			self._time_zone = kwargs.get('timeZone')
			self._language = kwargs.get('language')
			self._phone = kwargs.get('phone')
			self._skills = kwargs.get('skills')
			self._registry_date = datetime.strptime(kwargs.get('registryDate'), '%Y-%m-%dT%H:%M:%S.%f')
			self._last_login_date = datetime.strptime(kwargs.get('lastLoginDate'), '%Y-%m-%dT%H:%M:%S.%f')
			self._status = kwargs.get('status')

	@property
	def id(self) -> int:
		"""The ID of the user."""
		return self._id

	@property
	def name(self) -> str:
		"""The username of the user."""
		return self._name

	@property
	def email(self) -> str | None:
		"""The email of the user."""
		return self._email

	@property
	def first_name(self) -> str | None:
		"""The first name of the user."""
		return self._first_name

	@property
	def last_name(self) -> str | None:
		"""The last name of the user."""
		return self._last_name

	@property
	def title(self) -> str | None:
		"""The title of the user."""
		return self._title

	@property
	def company(self) -> str | None:
		"""The user's company."""
		return self._company

	@property
	def address(self) -> str | None:
		"""The user's address."""
		return self._address

	@property
	def zip(self) -> int | None:
		"""The user's zip code."""
		return self._zip

	@property
	def city(self) -> str | None:
		"""The user's city."""
		return self._city

	@property
	def state(self) -> str | None:
		"""The user's state."""
		return self._state

	@property
	def country(self) -> str | None:
		"""The user's country."""
		return self._country

	@property
	def date_format(self) -> str | None:
		"""The date format for the user. Determines the browser date's display."""
		return self._date_format

	@property
	def time_zone(self) -> str | None:
		"""The user's time zone."""
		return self._time_zone

	@property
	def language(self) -> str | None:
		"""The user's language. Either 'en' or 'de'."""
		return self._language

	@property
	def phone(self) -> str | None:
		"""The user's phone number."""
		return self._phone

	@property
	def skills(self) -> str | None:
		"""The user's skills."""
		return self._skills

	@property
	def registry_date(self) -> datetime | None:
		"""The datetime the user registered."""
		return self._registry_date

	@property
	def last_login_date(self) -> datetime | None:
		"""The datetime the user last logged in."""
		return self._last_login_date

	@property
	def status(self) -> str | None:
		"""The status of the user account."""
		return self._status

	def load(self):
		"""Loads the rest of the user's data. When a user is fetched using 
		`Codebeamer.get_users` only the ID, Name, and Email of the user are retrieved. 
		This prevents a lot of extra data that's not needed from being sent. Thus, 
		this method exists to flush out the rest of the user information if it is 
		needed."""
		if self.registry_date:
			logger.info('User already loaded, ignoring...')
			return
		user_data: dict[str, Any] = self._client.get(f'users/{self.id}')
		self._first_name = user_data.get('firstName')
		self._last_name = user_data.get('lastName')
		self._title = user_data.get('title')
		self._company = user_data.get('company')
		self._address = user_data.get('address')
		self._zip = user_data.get('zip')
		self._city = user_data.get('city')
		self._state = user_data.get('state')
		self._country = user_data.get('country')
		self._date_format = user_data.get('dateFormat')
		self._time_zone = user_data.get('timeZone')
		self._language = user_data.get('language')
		self._phone = user_data.get('phone')
		self._skills = user_data.get('skills')
		self._registry_date = datetime.strptime(user_data.get('registryDate'), '%Y-%m-%dT%H:%M:%S.%f')
		self._last_login_date = datetime.strptime(user_data.get('lastLoginDate'), '%Y-%m-%dT%H:%M:%S.%f')
		self._status = user_data.get('status')

	def __repr__(self) -> str:
		return f'User(id={self.id}, name={self.name})'
	
	def __str__(self) -> str:
		return self.name
	
	def __eq__(self, o: object) -> bool:
		return isinstance(o, User) and self.id == o.id
	
	def __lt__(self, o: object) -> bool:
		return isinstance(o, User) and self.id < o.id