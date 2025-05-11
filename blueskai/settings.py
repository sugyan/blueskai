import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Profile:
    file: Path
    bsky_identifier: str
    bsky_app_password: str


@dataclass
class Settings:
    brave_api_key: str
    profiles: list[Profile]


settings = Settings(
    brave_api_key=os.environ["BRAVE_API_KEY"],
    profiles=[
        Profile(
            file=(Path(__file__).parent.parent / "profiles" / "00.md").resolve(),
            bsky_identifier=os.environ["BLUESKY_IDENTIFIER_0"],
            bsky_app_password=os.environ["BLUESKY_APP_PASSWORD_0"],
        ),
        Profile(
            file=(Path(__file__).parent.parent / "profiles" / "01.md").resolve(),
            bsky_identifier=os.environ["BLUESKY_IDENTIFIER_1"],
            bsky_app_password=os.environ["BLUESKY_APP_PASSWORD_1"],
        ),
    ],
)
