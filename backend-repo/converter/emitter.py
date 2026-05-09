from __future__ import annotations

from typing import Any

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None

from .utils import yaml_lines


def dump_yaml(document: dict[str, Any]) -> str:
    if yaml is not None:
        return yaml.safe_dump(document, sort_keys=False, allow_unicode=True)
    return "\n".join(yaml_lines(document)) + "\n"
