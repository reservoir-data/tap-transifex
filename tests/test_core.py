"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_transifex.tap import TapTransifex

SAMPLE_CONFIG: dict[str, Any] = {}

TestTapTransifex = get_tap_test_class(
    TapTransifex,
    config=SAMPLE_CONFIG,
    suite_config=SuiteConfig(
        # max_records_limit=10,  # noqa: ERA001
    ),
)
