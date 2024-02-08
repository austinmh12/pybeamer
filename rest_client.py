from __future__ import annotations
from loguru import logger

from typing import Any
from requests import Session, Response
from requests.exceptions import HTTPError
from urllib.parse import urlencode

class RestClient:
	default_headers = {'Content-Type': 'application/json'}

	def __init__(
		self,
		url: str,
		username: str,
		password: str,
		timeout: int = 60,
		api_root: str = '',
		session: Session = None
	):
		self.url: str = url
		self.timeout: int = timeout
		self.api_root: str = api_root
		if session is None:
			self._session: Session = Session()
		else:
			self._session: Session = session
		if username and password:
			self._session_auth = {'username': username, 'password': password}
		self._session.auth = (username, password)

	def resource_url(self, resource: str) -> str:
		return '/'.join([self.api_root, resource])

	@staticmethod
	def url_joiner(url: str, path: str) -> str:
		return '/'.join(s.strip('/') for s in [url, path])
	
	def request(
		self,
		method: str = 'GET',
		path: str = '/',
		data: dict[str, Any] | None = None,
		json_: dict[str, Any] | None = None,
		flags: list[str] | None = None,
		params: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		files: dict[str, Any] | None = None,
	) -> dict[str, Any] | str:
		# TODO: Need to handle 429 tooManyRequests responses
		path = self.resource_url(path)
		url = self.url_joiner(self.url, path)
		if params or flags:
			url += '?'
		if params:
			url += urlencode(params or {})
		if flags:
			url += ('&' if params else '') + '&'.join(flags or [])
		headers = headers or self.default_headers
		response = self._session.request(
			method=method,
			url=url,
			headers=headers,
			data=data,
			json=json_,
			timeout=self.timeout,
			files=files,
			verify=False
		)
		logger.debug(f'HTTP: {method} {path} -> {response.status_code} {response.reason}')
		logger.debug(f'HTTP: Response text -> {response.text}')
		try:
			if response.text:
				response_content = response.json()
			else:
				response_content = response.content
		except ValueError:
			response_content = response.content
		try:
			response.raise_for_status()
		except HTTPError as err:
			pass # For now
		return response_content
	
	def get(
		self,
		path: str,
		data: dict[str, Any] | None = None,
		flags: list[str] | None = None,
		params: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		not_json_response: bool | None = None,
	) -> str | Response:
		resp = self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers)
		if not_json_response:
			return resp.content
		else:
			try:
				return resp
			except Exception as e:
				return

	def post(
		self,
		path: str,
		data: dict[str, Any] | None = None,
		json_: dict[str, Any] | None = None,
		params: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		files: dict[str, Any] | None = None,
	) -> Response | None:
		try:
			return self.request('POST', path=path, data=data, json_=json_, headers=headers, files=files, params=params)
		except ValueError:
			return None
		
	def put(
		self,
		path: str,
		data: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		files: dict[str, Any] | None = None,
		json_: dict[str, Any] | None = None
	) -> Response:
		try:
			return self.request('PUT', path=path, data=data, json_=json_, headers=headers, files=files)
		except ValueError:
			return None

	def delete(
		self,
		path: str,
		data: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		params: dict[str, Any] | None = None,
		json_: dict[str, Any] | None = None
	) -> None:
		self.request('DELETE', path=path, data=data, headers=headers, params=params, json_=json_)

	def patch(
		self,
		path: str,
		data: dict[str, Any] | None = None,
		headers: dict[str, Any] | None = None,
		params: dict[str, Any] | None = None,
		files: dict[str, Any] | None = None,
		json_: dict[str, Any] | None = None
	) -> Response:
		try:
			return self.request('PATCH', path=path, data=data, json_=json_, headers=headers, params=params, files=files)
		except ValueError:
			return None
