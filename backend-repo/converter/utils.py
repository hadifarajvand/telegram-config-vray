from __future__ import annotations

import base64
import re
from typing import Any


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if re.fullmatch(r"[A-Za-z0-9_.:/@%+\-]+", text) and text[0] not in "@-?:,[]{}#&*!|>'\"%`":
        return text
    return "'" + text.replace("'", "''") + "'"


def yaml_lines(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return [f"{prefix}{{}}"]
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, dict):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {{}}")
            elif isinstance(item, list):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(item)}")
        return lines
    if isinstance(value, list):
        if not value:
            return [f"{prefix}[]"]
        lines = []
        for item in value:
            if isinstance(item, dict):
                if item:
                    lines.append(f"{prefix}-")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}- {{}}")
            elif isinstance(item, list):
                if item:
                    lines.append(f"{prefix}-")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}- []")
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
        return lines
    return [f"{prefix}{yaml_scalar(value)}"]


def safe_int(value: Any, default: int | None = None) -> int | None:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def decode_base64_any(text: str) -> str | None:
    normalized = re.sub(r"\s+", "", text)
    for candidate in (normalized, normalized.replace("-", "+").replace("_", "/")):
        for pad in range(4):
            try:
                raw = base64.b64decode(candidate + ("=" * pad), validate=False)
                return raw.decode("utf-8")
            except Exception:
                continue
    return None


def split_lines(content: str) -> list[str]:
    lines: list[str] = []
    for raw in content.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        lines.append(line)
    return lines


def normalize_name(name: str | None, fallback: str) -> str:
    value = (name or "").strip()
    return value or fallback


def dedupe_name(name: str, seen: dict[str, int]) -> str:
    count = seen.get(name, 0)
    seen[name] = count + 1
    if count == 0:
        return name
    return f"{name}-{count + 1}"


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "on"}:
        return True
    if lowered in {"0", "false", "no", "off"}:
        return False
    return None
