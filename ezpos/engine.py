
import requests

class EzPOSEngine:
    def __init__(self, ip_adress: str):
        self.headers = {
            "Content-Type": "application/json",
            "Content-Length": "0",
        }
        self.ip_adress = ip_adress
        self.base_url = f"http://{self.ip_adress}"

    def make_request(self, endpoint: str, method: str = "GET", data: dict = None):
        url = f"{self.base_url}{endpoint}"
        if method.upper() == "POST":
            response = requests.post(url, json=data, headers=self.headers)
        else:
            response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            print(response.request.url, response.request.body)
            response.raise_for_status()