import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

from litestar.data_extractors import ResponseExtractorField, RequestExtractorField
from litestar.serialization import decode_json, encode_json
from litestar.utils.module_loader import module_to_os_path
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

BASE_DIR = module_to_os_path()


@dataclass
class AppSettings:
    NAME: str = "itmo-info-bot"
    VERSION: str = "0.1.0"
    DEBUG: bool = field(default_factory=lambda: json.loads(os.getenv("DEBUG", "false")))
    TEST: bool = field(default_factory=lambda: json.loads(os.getenv("TEST", "false")))

    def __post_init__(self):
        pyproject_path = Path(BASE_DIR).parent.parent / "pyproject.toml"
        with open(pyproject_path) as file:
            from app.lib.utils.pyproject import decode, PyProject
            content: PyProject = decode(file.read())
            self.NAME = content.tool['poetry']['name']
            self.VERSION = content.tool['poetry']['version']


@dataclass
class LogSettings:
    EXCLUDE_PATHS: str = r"\A(?!x)x"
    HTTP_EVENT: str = "HTTP"
    INCLUDE_COMPRESSED_BODY: bool = False
    LEVEL: int = field(default_factory=lambda: int(os.getenv("LOG_LEVEL", "10")))
    REQUEST_FIELDS: list[RequestExtractorField] = field(
        default_factory=lambda: ["method", "path", "path_params", "query", "body"])
    RESPONSE_FIELDS: list[ResponseExtractorField] = field(default_factory=lambda: ["status_code"])
    JSON: bool = field(default_factory=lambda: json.loads(os.getenv("LOG_JSON", "false")))


@dataclass
class Settings:
    app: AppSettings = field(default_factory=AppSettings)
    log: LogSettings = field(default_factory=LogSettings)
    
    @classmethod
    def from_env(cls, env_name=".env") -> "Settings":
        env_path = Path(f"{os.curdir}/{env_name}")
        if env_path.is_file():
            from dotenv import load_dotenv

            load_dotenv(env_path)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
