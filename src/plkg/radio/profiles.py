from __future__ import annotations

import tomllib
from dataclasses import dataclass, fields
from functools import cache, lru_cache
from importlib.resources import files
from typing import Any, Literal, cast

PROFILE_PACKAGE = "plkg.radio.profile_data"
REQUIRED_FIELDS = {
    "name",
    "measurement",
    "carrier_frequency_hz",
    "speed_kmh",
    "sample_interval_s",
    "alice_bob_correlation",
}


@dataclass(frozen=True)
class RadioProfile:
    name: str
    measurement: Literal["csi", "rssi"]
    carrier_frequency_hz: float
    speed_kmh: float
    sample_interval_s: float
    alice_bob_correlation: float
    alice_eve_correlation: float = 0.0
    estimation_error: float = 0.0
    rssi_reference_power_dbm: float = -60.0
    rssi_noise_std_db: float = 1.0
    rssi_resolution_db: float = 1.0

    def __post_init__(self) -> None:
        if self.measurement not in {"csi", "rssi"}:
            raise ValueError("measurement must be 'csi' or 'rssi'")
        if self.carrier_frequency_hz <= 0:
            raise ValueError("carrier_frequency_hz must be positive")
        if self.speed_kmh < 0:
            raise ValueError("speed_kmh cannot be negative")
        if self.sample_interval_s <= 0:
            raise ValueError("sample_interval_s must be positive")
        if not -1 <= self.alice_bob_correlation <= 1:
            raise ValueError("alice_bob_correlation must be in [-1, 1]")
        if not -1 <= self.alice_eve_correlation <= 1:
            raise ValueError("alice_eve_correlation must be in [-1, 1]")
        if self.estimation_error < 0:
            raise ValueError("estimation_error cannot be negative")
        if self.rssi_noise_std_db < 0:
            raise ValueError("rssi_noise_std_db cannot be negative")
        if self.rssi_resolution_db <= 0:
            raise ValueError("rssi_resolution_db must be positive")


@lru_cache(maxsize=1)
def _profile_names() -> tuple[str, ...]:
    resources = files(PROFILE_PACKAGE)
    return tuple(
        sorted(
            resource.name.removesuffix(".toml")
            for resource in resources.iterdir()
            if resource.name.endswith(".toml")
        )
    )


def list_profiles() -> tuple[str, ...]:
    return _profile_names()


@cache
def get_profile(name: str) -> RadioProfile:
    if name not in _profile_names():
        available = ", ".join(_profile_names())
        raise ValueError(f"unknown profile {name!r}; available: {available}")

    resource = files(PROFILE_PACKAGE).joinpath(f"{name}.toml")
    raw = tomllib.loads(resource.read_text(encoding="utf-8"))
    profile = _parse_profile(raw, source=resource.name)
    if profile.name != name:
        raise ValueError(
            f"{resource.name}: profile name {profile.name!r} must match filename"
        )
    return profile


def _parse_profile(raw: dict[str, Any], *, source: str) -> RadioProfile:
    missing = REQUIRED_FIELDS - raw.keys()
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"{source}: missing required fields: {names}")

    allowed = {item.name for item in fields(RadioProfile)}
    unknown = raw.keys() - allowed
    if unknown:
        names = ", ".join(sorted(unknown))
        raise ValueError(f"{source}: unknown fields: {names}")

    values = dict(raw)
    values["measurement"] = cast(Literal["csi", "rssi"], values["measurement"])
    try:
        return RadioProfile(**values)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{source}: invalid radio profile: {error}") from error
