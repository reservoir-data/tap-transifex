"""REST client handling, including TransifexStream base class."""

from __future__ import annotations

import typing as t
from urllib.parse import parse_qs

from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk.pagination import BaseHATEOASPaginator

if t.TYPE_CHECKING:
    from urllib.parse import ParseResult

    from requests import Response
    from singer_sdk.helpers.types import Context


class TransifexPaginator(BaseHATEOASPaginator):
    """Transifex paginator.

    https://developers.transifex.com/reference/api-pagination
    """

    def get_next_url(self, response: Response) -> str | None:
        """Get the next URL from the response."""
        data = response.json()
        return data.get("links", {}).get("next")  # type: ignore[no-any-return]


class TransifexStream(RESTStream[t.Any]):
    """Transifex stream class."""

    url_base = "https://rest.api.transifex.com"
    records_jsonpath = "$.data[*]"
    next_page_token_jsonpath = "$.links.next"  # noqa: S105

    @property
    def authenticator(self) -> BearerTokenAuthenticator:
        """Get an authenticator object.

        Returns:
            The authenticator instance for this REST stream.
        """
        return BearerTokenAuthenticator(token=self.config["token"])

    @property
    def http_headers(self) -> dict[str, str]:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"User-Agent": f"{self.tap_name}/{self._tap.plugin_version}"}

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: ParseResult | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.

        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            Mapping of URL query parameters.
        """
        params: dict[str, t.Any] = {}

        if next_page_token:
            params |= parse_qs(next_page_token.query)

        return params
