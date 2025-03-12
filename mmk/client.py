import requests
import logging
from json.decoder import JSONDecodeError

from exceptions import MmkAPIException

logger = logging.getLogger(__name__)


class SimpleHttpClient:
    def __init__(
        self,
        config: dict[str, str] = None,
        connection_pool_size: int = 5,
        debug: bool = False,
        timeout=10,  # in seconds
    ):
        if not config:
            raise ValueError("config is required")
        self.api_key = config.get("api_key")
        self.endpoint = config.get("base_url")
        self._connection_pool_size = connection_pool_size
        self._session = None
        self.timeout = timeout
        if debug:
            from http.client import HTTPConnection

            HTTPConnection.debuglevel = 1
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True

    def _create_session(self):
        self._session = requests.Session()
        if self._connection_pool_size > 0:
            adapter = requests.adapters.HTTPAdapter(
                pool_connections=self._connection_pool_size,
                pool_maxsize=self._connection_pool_size,
            )
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

    def _request(
        self,
        method: str,
        path: str,
        data: object = None,
        json: bool = True,
        headers: object = None,
        **kwargs,
    ):
        if self._session is None:
            self._create_session()
        url = self.endpoint + path
        headers = self._get_headers(headers=headers, json=json)

        if not kwargs.get("timeout", None):
            kwargs["timeout"] = self.timeout

        try:
            logger.info(f"Request: {method} {url}")
            if data and json:
                result = self._session.request(
                    method, url, headers=headers, json=data, **kwargs
                )
            elif data and not json:
                result = self._session.request(
                    method, url, headers=headers, data=data, **kwargs
                )
            else:
                result = self._session.request(method, url, headers=headers, **kwargs)

            if not result.ok:
                if result.status_code == 404:
                    raise MmkAPIException(
                        "Not found: " + url,
                        result.status_code,
                        {"message": "Resource not found."}
                    )
                if result.status_code == 500:
                    raise MmkAPIException(
                        "Internal server error: " + url,
                        result.status_code,
                    )
                try:
                    error_data = result.text or "MMK API error"
                    raise MmkAPIException(
                        error_data,
                        result.status_code,
                        error_data,
                    )
                except JSONDecodeError:
                    raise MmkAPIException("JSON Decode error", result.status_code)
            response_json = result.json()
            return response_json

        except requests.exceptions.ConnectTimeout as e:
            raise MmkAPIException(str(e))
        except requests.exceptions.Timeout as e:
            raise MmkAPIException(str(e))
        except requests.exceptions.ConnectionError as e:
            raise MmkAPIException(str(e))
        except requests.exceptions.RequestException as e:
            raise MmkAPIException(
                "General request error",
                None,
                {"message": str(e)}
            )

    def _get_headers(self, headers: object = None, json: bool = True):
        if headers is None:
            headers = {}
        if json:
            headers["Content-Type"] = "application/json"
        headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def get(self, path, **kwargs):
        return self._request("get", path, **kwargs)

    def post(self, path, data, **kwargs):
        return self._request("post", path, data, **kwargs)

    def put(self, path, data, **kwargs):
        return self._request("put", path, data, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("delete", path, **kwargs)

    def patch(self, path, data, **kwargs):
        return self._request("patch", path, data, **kwargs)
