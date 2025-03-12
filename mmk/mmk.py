from resources.country import CountryAPI


class MmkAPIService:
    def __init__(self, base_url: str = None, api_key: str = None):
        self._base_url = base_url
        self._api_key = api_key
        self._config = {"base_url": self._base_url, "api_key": self._api_key}

        self._country = CountryAPI(self._config)

    @property
    def country(self):
        return self._country
