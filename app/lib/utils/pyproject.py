from typing import Any

import msgspec


class Base(
    msgspec.Struct,
    omit_defaults=True,
    forbid_unknown_fields=True,
    rename="kebab",
):
    pass


class BuildSystem(Base):
    requires: list[str] = []
    build_backend: str | None = None
    backend_path: list[str] = []


class Readme(Base):
    file: str | None = None
    text: str | None = None
    content_type: str | None = None


class License(Base):
    file: str | None = None
    text: str | None = None


class Contributor(Base):
    name: str | None = None
    email: str | None = None


class Project(Base):
    name: str | None = None
    version: str | None = None
    description: str | None = None
    readme: str | Readme | None = None
    license: str | License | None = None
    authors: list[Contributor] = []
    maintainers: list[Contributor] = []
    keywords: list[str] = []
    classifiers: list[str] = []
    urls: dict[str, str] = {}
    requires_python: str | None = None
    dependencies: list[str] = []
    optional_dependencies: dict[str, list[str]] = {}
    scripts: dict[str, str] = {}
    gui_scripts: dict[str, str] = {}
    entry_points: dict[str, dict[str, str]] = {}
    dynamic: list[str] = []


class PyProject(Base):
    build_system: BuildSystem | None = None
    project: Project | None = None
    tool: dict[str, dict[str, Any]] = {}


def decode(data: bytes | str) -> PyProject:
    return msgspec.toml.decode(data, type=PyProject)


def encode(msg: PyProject) -> bytes:
    return msgspec.toml.encode(msg)
