from mmk.client import SimpleHttpClient


class BaseResource:
    def __init__(self, config: dict[str, str]):
        debug = config.get('debug', False)
        self.httpClient = SimpleHttpClient(config=config, debug=debug)
