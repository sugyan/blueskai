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
    profiles: list[Profile]


settings = Settings(
    profiles=[
        Profile(
            file=(Path(__file__).parent.parent / "profiles" / "00.md").resolve(),
            bsky_identifier=os.environ["BLUESKY_IDENTIFIER_0"],
            bsky_app_password=os.environ["BLUESKY_APP_PASSWORD_0"],
        ),
    ]
)
