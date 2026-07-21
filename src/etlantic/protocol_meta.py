"""Typed interoperability metadata for stability-critical protocol boundaries.

Protocol execution and compile contexts keep ``metadata`` as a
:class:`~collections.abc.Mapping` for back-compat. Prefer
:class:`ExecutionContextMeta` / :class:`CompileArtifactMeta` (or
:func:`coerce_context_meta` / :func:`coerce_compile_meta`) when reading or
emitting structured interop fields. Extension bags should use the namespaces
enforced by :func:`~etlantic.extensions.validate_extension_metadata`
(``etlantic.`` / ``plugin:``), or be empty.
"""

from __future__ import annotations

from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator,
    model_validator,
)

from etlantic.extensions import validate_extension_metadata

_KNOWN_META_KEYS = frozenset(
    {"engine", "protocol_version", "vocabulary_version", "extensions"}
)


class ExtensionMetadata(RootModel[dict[str, Any]]):
    """Dict-like extension bag with namespace validation.

    Keys must use extension namespaces (``etlantic.`` or ``plugin:``), or the
    bag may be empty. See :func:`~etlantic.extensions.validate_extension_metadata`.
    """

    root: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _validate_keys(self) -> ExtensionMetadata:
        validate_extension_metadata(self.root, path="ExtensionMetadata", strict=True)
        return self

    def __iter__(self) -> Iterator[str]:  # type: ignore[override]
        return iter(self.root)

    def __getitem__(self, key: str) -> Any:
        return self.root[key]

    def __len__(self) -> int:
        return len(self.root)

    def __contains__(self, key: object) -> bool:
        return key in self.root

    def get(self, key: str, default: Any = None) -> Any:
        return self.root.get(key, default)

    def keys(self) -> KeysView[str]:
        return self.root.keys()

    def values(self) -> ValuesView[Any]:
        return self.root.values()

    def items(self) -> ItemsView[str, Any]:
        return self.root.items()

    def to_dict(self) -> dict[str, Any]:
        return dict(self.root)


class ExecutionContextMeta(BaseModel):
    """Typed interoperability fields for execution contexts.

    Protocol dataclasses still accept a bare ``metadata`` mapping; use
    :func:`coerce_context_meta` or context ``.context_meta`` accessors when a
    structured view is needed.
    """

    model_config = ConfigDict(extra="ignore")

    engine: str | None = None
    protocol_version: str | None = None
    vocabulary_version: str | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)

    @field_validator("extensions")
    @classmethod
    def _validate_extensions(cls, value: Mapping[str, Any]) -> dict[str, Any]:
        payload = dict(value)
        validate_extension_metadata(payload, path="extensions", strict=True)
        return payload


class CompileArtifactMeta(BaseModel):
    """Typed interoperability fields for compile / artifact metadata."""

    model_config = ConfigDict(extra="ignore")

    engine: str | None = None
    protocol_version: str | None = None
    vocabulary_version: str | None = None
    extensions: dict[str, Any] = Field(default_factory=dict)

    @field_validator("extensions")
    @classmethod
    def _validate_extensions(cls, value: Mapping[str, Any]) -> dict[str, Any]:
        payload = dict(value)
        validate_extension_metadata(payload, path="extensions", strict=True)
        return payload


def _split_structured_meta(
    data: Mapping[str, Any],
) -> dict[str, Any]:
    """Normalize a mapping into structured meta + extension bag."""
    payload = dict(data)
    if "extensions" in payload or any(
        key in payload for key in ("engine", "protocol_version", "vocabulary_version")
    ):
        extensions = dict(payload.get("extensions") or {})
        for key, value in payload.items():
            if key in _KNOWN_META_KEYS:
                continue
            extensions[str(key)] = value
        return {
            "engine": payload.get("engine"),
            "protocol_version": payload.get("protocol_version"),
            "vocabulary_version": payload.get("vocabulary_version"),
            "extensions": extensions,
        }
    return {"extensions": payload}


def coerce_context_meta(
    data: Mapping[str, Any] | ExecutionContextMeta | None,
) -> ExecutionContextMeta:
    """Coerce a mapping or existing model into :class:`ExecutionContextMeta`."""
    if data is None:
        return ExecutionContextMeta()
    if isinstance(data, ExecutionContextMeta):
        return data
    return ExecutionContextMeta.model_validate(_split_structured_meta(data))


def coerce_compile_meta(
    data: Mapping[str, Any] | CompileArtifactMeta | None,
) -> CompileArtifactMeta:
    """Coerce a mapping or existing model into :class:`CompileArtifactMeta`."""
    if data is None:
        return CompileArtifactMeta()
    if isinstance(data, CompileArtifactMeta):
        return data
    return CompileArtifactMeta.model_validate(_split_structured_meta(data))
