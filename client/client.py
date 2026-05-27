import requests

from typing import Any

class ClientException(Exception):
    pass

class OllamaClient:
    def __init__(self, config: dict):
        self.api_host = config.get("llm_url")
        self.api_port = config.get("llm_port")
        self.api_protocol = config.get("llm_protocol")
        self.api_url = f"{self.api_protocol}://{self.api_host}:{self.api_port}/"

    def _headers(self):
        return {
                "Content-Type": "application/json",
                }

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        try:
            response = requests.request(method, url, headers=self._headers(), **kwargs)
            return response
        except requests.RequestException as e:
            raise ClientException(f"failed to complete request {e}")

    def get(self, url: str) -> requests.Response:
        return self._request("GET", url)

    def post(self, url: str, payload: Any) -> requests.Response:
        return self._request("POST", url, json=payload)
