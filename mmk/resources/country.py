from mmk.constants import MmkEndpoint
from mmk.resources.base_resource import BaseResource


class CountryAPI(BaseResource):
    """
    MMK API for country.
    """

    def __init__(self, config: dict[str, str]):
        super().__init__(config)

    def list(self, **kwargs):
        """
        Provides a list of countries.
        see: https://app.swaggerhub.com/apis-docs/mmksystems/bm-api/2.1.2#/Booking/getCountries
        """
        return self.httpClient.get(MmkEndpoint.COUNTRIES.value, **kwargs)

    def get_by_id(self, country_id: int, **kwargs):
        """
        Gets a specific country by ID.
        see: https://app.swaggerhub.com/apis-docs/mmksystems/bm-api/2.1.2#/Booking/getCountryById
        """
        return self.httpClient.get(
            MmkEndpoint.COUNTRY.value.format(country_id=country_id, **kwargs)
        )
