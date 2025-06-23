import aiohttp
import asyncio

class EzPOSEngineAsync:
    def __init__(self, ip_adress: str):
        self.headers = {
            "Content-Type": "application/json",
            "Content-Length": "0",
        }
        self.ip_adress = ip_adress
        self.base_url = f"http://{self.ip_adress}"

    async def make_request(self, endpoint: str, method: str = "GET", data: dict = None):
        url = f"{self.base_url}{endpoint}"

        async with aiohttp.ClientSession() as session:
            try:
                if method.upper() == "POST":
                    async with session.post(url, json=data, headers=self.headers) as response:
                        return await self._handle_response(response)
                else:
                    async with session.get(url) as response:
                        return await self._handle_response(response)
            except aiohttp.ClientError as e:
                print(f"Request error: {e}")
                raise

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if response.status == 200:
            return await response.json()
        else:
            body = await response.text()
            print(f"Failed request: {response.url} | Body: {body}")
            response.raise_for_status()
