from __future__ import annotations

from pathlib import Path

from converter.mihomo import ConvertOptions, convert_v2ray_subscription_to_mihomo_config


def _should_skip_line(line: str) -> bool:
    lowered = line.lower()
    if any(token in lowered for token in ("latest-update", "telegram-channel", "developed-by", "donating")):
        return True
    if "://127.0.0.1:" in lowered or "://localhost:" in lowered or "://[::1]:" in lowered:
        return True
    return False


def build_clash_verge_feed(path: str | Path, configs: list[str], options: ConvertOptions | None = None) -> str:
    filtered = [line for line in configs if not _should_skip_line(line)]
    text = "\n".join(filtered)
    result = convert_v2ray_subscription_to_mihomo_config(text, options or ConvertOptions())
    Path(path).write_text(result.yaml, encoding="utf-8")
    return result.yaml
