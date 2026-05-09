from __future__ import annotations

from dataclasses import dataclass, field

from converter.policy import (
    DEFAULT_APP_RULES,
    DEFAULT_AUTO_INTERVAL,
    DEFAULT_AUTO_TOLERANCE,
    DEFAULT_LOAD_BALANCE_INTERVAL,
    DEFAULT_LOAD_BALANCE_STRATEGY,
    DEFAULT_TEST_URL,
)


@dataclass
class ConvertOptions:
    prepend_app_rules: bool = False
    test_url: str = DEFAULT_TEST_URL
    auto_interval: int = DEFAULT_AUTO_INTERVAL
    load_balance_interval: int = DEFAULT_LOAD_BALANCE_INTERVAL
    load_balance_strategy: str = DEFAULT_LOAD_BALANCE_STRATEGY
    auto_tolerance: int = DEFAULT_AUTO_TOLERANCE
    app_rules: list[str] = field(
        default_factory=lambda: list(DEFAULT_APP_RULES)
    )


@dataclass
class ConvertResult:
    yaml: str
    proxies: list[dict[str, object]]
    warnings: list[str]
    errors: list[str]
