import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Profile:
    file: Path
    bsky_identifier: str
    bsky_app_password: str
    mcp_servers: set[str]


@dataclass
class Settings:
    tz: str
    expertise_mcp_url: str
    profiles: list[Profile]


settings = Settings(
    tz="Asia/Tokyo",
    expertise_mcp_url=os.environ["EXPERTISE_MCP_URL"],
    profiles=[
        Profile(
            file=(Path(__file__).parent.parent / "profiles" / "00.md").resolve(),
            bsky_identifier=os.environ["BLUESKY_IDENTIFIER_0"],
            bsky_app_password=os.environ["BLUESKY_APP_PASSWORD_0"],
            mcp_servers={"bsky"},
        ),
        Profile(
            file=(Path(__file__).parent.parent / "profiles" / "01.md").resolve(),
            bsky_identifier=os.environ["BLUESKY_IDENTIFIER_1"],
            bsky_app_password=os.environ["BLUESKY_APP_PASSWORD_1"],
            mcp_servers={"bsky", "expertise"},
        ),
    ],
)
