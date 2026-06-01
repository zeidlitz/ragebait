import requests

from typing import Any


class ClientException(Exception):
    pass


class OllamaClient:
    def __init__(self, model, host, port, protocol):
        self.model = model
        self.api_host = host
        self.api_port = port
        self.api_protocol = protocol
        self.api_url = f"{self.api_protocol}://{self.api_host}:{self.api_port}"

    def get_completion(self, system_prompt, prompt):
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": prompt,
            "stream": False,
        }
        url = self.api_url + "/api/generate"
        response = self.post(url, payload)
        if response.status_code not in [200]:
            raise ClientException(f"could not get completion {response.text}")
        try:
            return response.json().get("response")
        except KeyError as e:
            raise ClientException(f"could not extract completion response {e}")

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
