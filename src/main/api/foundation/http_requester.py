from collections.abc import Callable

from src.main.api.foundation.endpoint import Endpoint


class HTTPRequester:
    def __init__(self, request_spec: dict | None, response_spec: Callable, endpoint: Endpoint):
        self.endpoint = endpoint
        self.request_spec = request_spec
        self.response_spec = response_spec
