from functools import lru_cache

from pydantic_settings import BaseSettings
import requests

BASE_URL = "https://adventofcode.com/2025/day/{day}/input"


class AoCSettings(BaseSettings):
    session_cookie: str = "session_cookie"

    class Config:
        env_file = ".env"


class AoCInputDataFetcher:
    def __init__(self, settings: AoCSettings | None = None):
        if settings is None:
            settings = AoCSettings()

        self.session_cookie = settings.session_cookie

    def fetch(self, day: int) -> str:
        url = BASE_URL.format(day=day)
        cookies = {"session": self.session_cookie}
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        return response.text


fetcher = AoCInputDataFetcher()


@lru_cache(maxsize=128)
def fetch(day: int) -> list[str]:
    print(f"fetching data for day {day}")
    data = fetcher.fetch(day=day)
    return data.splitlines()
