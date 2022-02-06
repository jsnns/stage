from email import header
import json
from typing import Mapping
from requests import get, post, put
import aiohttp
import asyncio


class BlitzClient:
    def __init__(self, ip: str = None):
        self.ip = ip
        self.lights: Mapping[str, int] = {}

        self.connect()

        # get data
        self._lights()
        # self._entertainment_areas()

    def save_token(self, token: str, client_key: str = None):
        with open("config.json", "w") as f:
            f.write(json.dumps({"token": token, "client_key": client_key}))

    def get_token(self):
        try:
            with open("config.json", "r") as f:
                data = json.loads(f.read())
                return data["token"], data["client_key"]
        except (FileNotFoundError, KeyError):
            return None, None

    def connect(self):
        token, client_key = self.get_token()
        if token and client_key:
            self.token = token
            self.client_key = client_key
            return

        result = post(
            f"http://{self.ip}/api",
            json={"devicetype": "Blitz", "generateclientkey": True},
        )

        try:
            data = result.json()
            print(data)
            self.token = data[0]["success"]["username"]
            self.save_token(self.token)
        except KeyError:
            raise Exception("Failed to connect to Bridge. Did you press the button?")

    def get_app_id(self):
        print(self.token)
        headers = get(
            f"https://{self.ip}/auth/v1",
            headers={"hue-application-key": self.token},
            verify=False,
        ).headers
        self.app_id = headers["hue-application-id"]
        return self.app_id

    def get(self, url: str = None, base="api"):
        return get(
            f"https://{self.ip}/{base}/{self.token}/{url}",
            headers={"hue-application-key": self.token},
            verify=False,
        ).json()

    def put(self, url: str = None, data: Mapping = None):
        return put(
            f"https://{self.ip}/api/{self.token}/{url}",
            headers={"hue-application-key": self.token},
            verify=False,
            json=data,
        )

    def get_light(self, name: str = None):
        return self.get(f"lights/{self.lights[name]}")

    def set_light(self, name: str = None, **kwargs):
        async def send():
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"http://{self.ip}/api/{self.token}/lights/{self.lights[name]}/state",
                    json=kwargs,
                ) as response:
                    pass

        asyncio.run(send())

    def _entertainment_areas(self):
        self.entertainment_areas = {}

        areas = get(
            f"https://{self.ip}/clip/v2/resource/entertainment_configuration",
            headers={"hue-application-key": self.token},
            verify=False,
        ).json()["data"]

        for area in areas:
            self.entertainment_areas[area["name"]] = area["id"]

        return self.entertainment_areas

    def _lights(self, url: str = None):
        for light_id, light_info in self.get("lights").items():
            self.lights[light_info["name"]] = int(light_id)

    def start_streaming(self, name: str = None):
        return put(
            f"https://{self.ip}/clip/v2/resource/entertainment_configuration/{self.entertainment_areas[name]}",
            headers={"hue-application-key": self.token},
            verify=False,
            json={
                "action": "start",
            },
        ).json()["data"]
