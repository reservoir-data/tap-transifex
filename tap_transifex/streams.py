"""Stream type classes for tap-transifex."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_transifex.client import TransifexStream

if t.TYPE_CHECKING:
    from urllib.parse import ParseResult

    from singer_sdk.helpers.types import Context


class Languages(TransifexStream):
    """Languages stream."""

    name = "languages"
    path = "/languages"
    primary_keys = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Language identifier.",
            required=True,
        ),
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property(
                    "code",
                    th.StringType,
                    description="The language code as defined in CLDR.",
                    required=True,
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the Language as defined in CLDR.",
                    required=True,
                ),
                th.Property(
                    "plural_equation",
                    th.StringType,
                    description="The language plural rule equation as defined in CLDR.",
                    required=True,
                ),
                th.Property(
                    "plural_rules",
                    th.ObjectType(
                        additional_properties=th.StringType,
                    ),
                    description=(
                        "Object of plural rules for Language as defined in CLDR."
                    ),
                ),
                th.Property(
                    "rtl",
                    th.BooleanType,
                    description="If the language is rlt.",
                    required=True,
                ),
            ),
            description="Language attributes.",
            required=True,
        ),
        th.Property(
            "links",
            th.ObjectType(th.Property("self", th.StringType, required=True)),
            description="Language links.",
            required=True,
        ),
        th.Property("type", th.StringType),
    ).to_dict()


class Organizations(TransifexStream):
    """Organizations stream."""

    name = "organizations"
    path = "/organizations"
    primary_keys = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property(
                    "logo_url",
                    th.StringType,
                    description="The organization logo url.",
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="The organization name.",
                    required=True,
                ),
                th.Property(
                    "private",
                    th.BooleanType,
                    description=(
                        "Private organization. A private organization is "
                        "visible only by you and your team."
                    ),
                ),
                th.Property(
                    "slug",
                    th.StringType,
                    description="The organization slug.",
                    required=True,
                ),
            ),
            description="Organization attributes.",
            required=True,
        ),
        th.Property(
            "id",
            th.StringType,
            description="Organization identifier.",
            required=True,
        ),
        th.Property(
            "links",
            th.ObjectType(
                th.Property("self", th.StringType, required=True),
            ),
            description="Organization links.",
            required=True,
        ),
        th.Property(
            "relationships",
            th.ObjectType(
                th.Property(
                    "projects",
                    th.ObjectType(
                        th.Property(
                            "links",
                            th.ObjectType(th.Property("related", th.StringType)),
                        )
                    ),
                ),
                th.Property(
                    "teams",
                    th.ObjectType(
                        th.Property(
                            "links",
                            th.ObjectType(th.Property("related", th.StringType)),
                        )
                    ),
                ),
            ),
        ),
        th.Property("type", th.StringType),
    ).to_dict()

    def generate_child_contexts(  # noqa: D102
        self,
        record: dict[str, t.Any],
        context: Context | None,  # noqa: ARG002
    ) -> t.Iterable[dict[str, t.Any] | None]:
        yield {
            "organization_id": record["id"],
        }


class I18nFormats(TransifexStream):
    """I18nFormats stream."""

    name = "i18n_formats"
    path = "/i18n_formats"
    primary_keys = ("id",)
    replication_key = None

    parent_stream_type = Organizations

    schema = th.PropertiesList(
        th.Property(
            "attributes",
            th.ObjectType(
                th.Property(
                    "description",
                    th.StringType,
                    description="The i18n_type description.",
                    required=True,
                ),
                th.Property(
                    "file_extensions",
                    th.ArrayType(th.StringType),  # ty: ignore[invalid-argument-type]
                    description=(
                        "The file name extension association to the media_type."
                    ),
                    required=True,
                ),
                th.Property(
                    "media_type",
                    th.StringType,
                    description=(
                        "A two-part identifier for file formats and format contents "
                        "transmitted."
                    ),
                    required=True,
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="The name of the i18n format.",
                    required=True,
                ),
            ),
            description="I18n format attributes.",
            required=True,
        ),
        th.Property(
            "id",
            th.StringType,
            description="I18n format identifier.",
            required=True,
        ),
        th.Property("type", th.StringType),
        th.Property("organization_id", th.StringType, description="Organization ID."),
    ).to_dict()

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: ParseResult | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        params = super().get_url_params(context, next_page_token)
        params["filter[organization]"] = context["organization_id"] if context else None
        return params
