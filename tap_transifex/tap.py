"""Transifex tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_transifex import streams


class TapTransifex(Tap):
    """Singer tap for Transifex."""

    name = "tap-transifex"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            required=True,
            description="API Token for Transifex",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest datetime to get data from",
        ),
    ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of Transifex streams.
        """
        return [
            streams.Languages(tap=self),
            streams.Organizations(tap=self),
            streams.I18nFormats(tap=self),
        ]
