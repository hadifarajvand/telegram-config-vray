from .options import ConvertOptions, ConvertResult

__all__ = [
    "ConvertOptions",
    "ConvertResult",
    "V2RayToMihomoConverter",
    "convert_v2ray_subscription_to_mihomo_config",
]


def convert_v2ray_subscription_to_mihomo_config(input_text, options=None):
    from .mihomo import convert_v2ray_subscription_to_mihomo_config as _convert

    return _convert(input_text, options)


def V2RayToMihomoConverter(*args, **kwargs):
    from .mihomo import V2RayToMihomoConverter as _Converter

    return _Converter(*args, **kwargs)
