import sys
from datetime import datetime
from typing import Dict, List, NamedTuple

from tests import test_avro, test_json, test_pbuf
from tests.base import SchemaTester

SchemaTester.setup_class()


class CompatMode(NamedTuple):
    level: str
    name: str
    description: str


class Transform(NamedTuple):
    name: str = ""
    v1_str: str = ""
    v2_str: str = ""
    schema_lang: str = "json"

    def _code_snippet(self, multi_line_str: str) -> list:
        snip = [f"```{self.schema_lang}"]
        for line in multi_line_str.split("\n"):
            snip.append(line)
        snip.append("```")
        return [line for line in snip if len(line)]

    def v1_lines(self) -> list:
        return self._code_snippet(self.v1_str)

    def v2_lines(self) -> list:
        return self._code_snippet(self.v2_str)


class SerializationFormatReporter:
    def __init__(self, title: str, schema_type: str) -> None:
        self._title = title
        self._schema_type = schema_type
        self._allowed_transforms: Dict[str, List] = {}
        self._not_allowed_transforms: Dict[str, List] = {}

    _modes: list = [
        CompatMode(
            level="backward",
            name="Backwards Compatibility",
            description="A new schema is backward compatible if it can be used to read the data written in the previous schema.",
        ),
        CompatMode(
            level="forward",
            name="Forwards Compatibility",
            description="A new schema is forward compatible if the previous schema can read data written in this schema.",
        ),
        CompatMode(
            level="full",
            name="Full Compatibility",
            description="A new schema is fully compatible if it's both backward and forward compatible.",
        ),
    ]

    def get_all_transforms(self) -> List[Transform]:
        return []

    def test_transforms(self) -> None:
        for mode in self._modes:
            self._allowed_transforms[mode.level] = []
            self._not_allowed_transforms[mode.level] = []
            tester = SchemaTester()
            tester.schema_type = self._schema_type
            tester.client.set_compatibility(level=mode.level)
            for transform in self.get_all_transforms():
                if tester.is_compatible(transform.v1_str, transform.v2_str):
                    self._allowed_transforms[mode.level].append(transform)
                else:
                    self._not_allowed_transforms[mode.level].append(transform)

    def summary(self) -> List[str]:
        lines = []
        lines.append(f'### [{self._title}](#{self._title.replace(" ", "_")})')
        lines.append("")
        for mode in self._modes:
            lines.append(
                f'[{mode.name}](#{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")})'
            )
            lines.append(f" - Allowed transformations")
            lines.append("")
            for transform in self._allowed_transforms[mode.level]:
                lines.append(
                    f'   - [{transform.name}](#{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")}_{transform.name.replace(" ", "_")})'
                )
                lines.append("")
            lines.append(f" - Non-allowed transformations")
            lines.append("")
            for transform in self._not_allowed_transforms[mode.level]:
                lines.append(
                    f'   - [{transform.name}](#{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")}_{transform.name.replace(" ", "_")})'
                )
                lines.append("")

        return lines

    def details(self) -> List[str]:
        lines = []

        lines.append(f'# <a id="{self._title.replace(" ", "_")}"></a>{self._title}')
        lines.append("")

        for mode in self._modes:
            lines.append(
                f'## <a id="{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")}"></a>{mode.name}'
            )
            lines.append(mode.description)

            for transform in self._allowed_transforms[mode.level]:
                lines.append(
                    f'### <a id="{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")}_{transform.name.replace(" ", "_")}"></a>{transform.name}'
                )
                lines.append("")
                lines.append("V1")
                lines.extend(transform.v1_lines())
                lines.append("V2")
                lines.extend(transform.v2_lines())

            lines.append("")
            lines.append(f"## Changes that break {(mode.name)}")
            lines.append("")
            if len(self._not_allowed_transforms[mode.level]):
                lines.append("")
                for transform in self._not_allowed_transforms[mode.level]:
                    lines.append(
                        f'### <a id="{self._title.replace(" ", "_")}_{mode.level.replace(" ", "_")}_{transform.name.replace(" ", "_")}"></a>{transform.name} *(not permitted)*'
                    )
                    lines.append("")
                    lines.append("V1")
                    lines.extend(transform.v1_lines())
                    lines.append("V2")
                    lines.extend(transform.v2_lines())
            else:
                lines.append("*(none)*")
            lines.append("---")

        lines.append("")

        return lines


class AvroReporter(SerializationFormatReporter):
    def __init__(self) -> None:
        super().__init__("Avro", "AVRO")

    def get_all_transforms(self) -> List[Transform]:
        return [
            Transform(
                name="Add optional field",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_add_optional_field,
            ),
            Transform(
                name="Delete optional field",
                v1_str=test_avro.schema_add_optional_field,
                v2_str=test_avro.base_schema,
            ),
            Transform(
                name="Add required field",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_add_required_field,
            ),
            Transform(
                name="Delete required field",
                v1_str=test_avro.schema_add_required_field,
                v2_str=test_avro.base_schema,
            ),
            Transform(
                name="Make required field optional",
                v1_str=test_avro.schema_add_required_field,
                v2_str=test_avro.schema_add_optional_field,
            ),
            Transform(
                name="Make optional field required",
                v1_str=test_avro.schema_add_optional_field,
                v2_str=test_avro.schema_add_required_field,
            ),
            Transform(
                name="Rename field with alias",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_rename_field_with_alias,
            ),
            Transform(
                name="Make non-nullable field nullable",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_field_evolved_to_union,
            ),
            Transform(
                name="Make nullable field non-nullable",
                v1_str=test_avro.schema_field_evolved_to_union,
                v2_str=test_avro.base_schema,
            ),
            Transform(
                name="Add type to union",
                v1_str=test_avro.schema_field_evolved_to_union,
                v2_str=test_avro.schema_field_add_type_to_union,
            ),
            Transform(
                name="Remove type from union",
                v1_str=test_avro.schema_field_add_type_to_union,
                v2_str=test_avro.schema_field_evolved_to_union,
            ),
        ]


class JsonReporter(SerializationFormatReporter):
    def __init__(self) -> None:
        super().__init__("JSON Schema", "JSON")

    def get_all_transforms(self) -> List[Transform]:
        return [
            Transform(
                "Delete optional field (open content model)",
                v1_str=test_json.schema_add_optional_field,
                v2_str=test_json.schema_base,
            ),
            Transform(
                "Delete required field (open content model)",
                v1_str=test_json.schema_add_required_field,
                v2_str=test_json.schema_base,
            ),
            Transform(
                "Add optional field (open content model)",
                v1_str=test_json.schema_base,
                v2_str=test_json.schema_add_optional_field,
            ),
            Transform(
                "Add required field (open content model)",
                v1_str=test_json.schema_base,
                v2_str=test_json.schema_add_required_field,
            ),
            Transform(
                "Add optional field (open to closed content model)",
                v1_str=test_json.schema_base,
                v2_str=test_json.schema_closed_add_optional_field,
            ),
            Transform(
                "Add required field (open to closed content model)",
                v1_str=test_json.schema_base,
                v2_str=test_json.schema_closed_add_required_field,
            ),
            Transform(
                "Add optional field (closed content model)",
                v1_str=test_json.schema_closed_base,
                v2_str=test_json.schema_closed_add_optional_field,
            ),
            Transform(
                "Add optional field (closed to open content model)",
                v1_str=test_json.schema_closed_base,
                v2_str=test_json.schema_add_optional_field,
            ),
            Transform(
                "Make required field optional (closed content model) ",
                v1_str=test_json.schema_closed_base,
                v2_str=test_json.schema_closed_make_field_optional,
            ),
            Transform(
                "Delete optional field (closed to open content model)",
                v1_str=test_json.schema_closed_add_optional_field,
                v2_str=test_json.schema_base,
            ),
            Transform(
                "Delete required field (closed to open content model)",
                v1_str=test_json.schema_closed_add_required_field,
                v2_str=test_json.schema_base,
            ),
            Transform(
                "Delete optional field (closed content model)",
                v1_str=test_json.schema_closed_add_optional_field,
                v2_str=test_json.schema_closed_base,
            ),
            Transform(
                "Delete required field (closed content model)",
                v1_str=test_json.schema_closed_add_required_field,
                v2_str=test_json.schema_closed_base,
            ),
            Transform(
                "Add required field (closed content model)",
                v1_str=test_json.schema_closed_base,
                v2_str=test_json.schema_closed_add_required_field,
            ),
            Transform(
                "Make optional field required (closed content model)",
                v1_str=test_json.schema_closed_make_field_optional,
                v2_str=test_json.schema_closed_base,
            ),
        ]


class PbufReporter(SerializationFormatReporter):
    def __init__(self) -> None:
        super().__init__("Protocol Buffers", "PROTOBUF")

    def get_all_transforms(self) -> List[Transform]:
        return [
            Transform(
                "Add Field",
                v1_str=test_pbuf.schema_base,
                v2_str=test_pbuf.schema_add_field,
                schema_lang="Protocol Buffer",
            ),
            Transform(
                "Delete Field",
                v1_str=test_pbuf.schema_add_field,
                v2_str=test_pbuf.schema_base,
                schema_lang="Protocol Buffer",
            ),
            Transform(
                "Rename Field Number",
                v1_str=test_pbuf.schema_base,
                v2_str=test_pbuf.schema_rename_field,
                schema_lang="Protocol Buffer",
            ),
        ]


def generate_report():

    reporters = [AvroReporter(), PbufReporter(), JsonReporter()]
    for reporter in reporters:
        reporter.test_transforms()

    with open("./report.md", "w") as f:
        f.write("# Schema Evolution Compatibility\n")
        f.write(f"Generated on {datetime.utcnow().isoformat()}\n")

        f.write("## Summary\n")
        for reporter in reporters:
            for line in reporter.summary():
                f.write(line)
                f.write("\n")

        f.write("## Details\n")
        for reporter in reporters:
            for line in reporter.details():
                f.write(line)
                f.write("\n")


def main(*argv):
    return generate_report()


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
