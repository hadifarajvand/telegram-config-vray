from __future__ import annotations

from pathlib import Path

from mihomo_converter import (  # compatibility shim for the old root module
    ConvertOptions,
    ConvertResult,
    V2RayToMihomoConverter,
    convertV2RaySubscriptionToMihomoConfig,
    main,
)

__all__ = [
    "ConvertOptions",
    "ConvertResult",
    "V2RayToMihomoConverter",
    "convert_v2ray_subscription_to_mihomo_config",
]


def convert_v2ray_subscription_to_mihomo_config(
    input_text: str, options: ConvertOptions | None = None
) -> ConvertResult:
    return convertV2RaySubscriptionToMihomoConfig(input_text, options)


def cli(argv: list[str] | None = None) -> int:
    return main(argv)

