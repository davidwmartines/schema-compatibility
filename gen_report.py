import sys
from typing import Dict, List, NamedTuple

from tests import test_avro
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

    title: str = ""
    schema_type: str = ""

    _allowed_transforms: Dict[str, List] = {}
    _not_allowed_transforms: Dict[str, List] = {}

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
            tester.schema_type = self.schema_type
            tester.client.set_compatibility(level=mode.level)
            for transform in self.get_all_transforms():
                if tester.is_compatible(transform.v1_str, transform.v2_str):
                    self._allowed_transforms[mode.level].append(transform)
                else:
                    self._not_allowed_transforms[mode.level].append(transform)

    def output_lines(self) -> list:
        lines = []

        lines.append(f"# {self.title}")
        lines.append("")

        for mode in self._modes:
            lines.append(f"## {mode.name}")
            lines.append(mode.description)

            for transform in self._allowed_transforms[mode.level]:
                lines.append(f"### {transform.name}")
                lines.append("")
                lines.append("V1")
                lines.extend(transform.v1_lines())
                lines.append("V2")
                lines.extend(transform.v2_lines())

            lines.append("")
            lines.append(f"## Changes that break {(mode.name)}")
            lines.append("")
            lines.append("")
            for transform in self._not_allowed_transforms[mode.level]:
                lines.append(f"### {transform.name} *(not permitted)*")
                lines.append("")
                lines.append("V1")
                lines.extend(transform.v1_lines())
                lines.append("V2")
                lines.extend(transform.v2_lines())
            lines.append("---")

        lines.append("")

        return lines


class AvroReporter(SerializationFormatReporter):

    title = "Avro"
    schema_type = "AVRO"

    def get_all_transforms(self) -> List[Transform]:
        return [
            Transform(
                name="Add optional field",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_add_optional_field,
            ),
            Transform(
                name="Add required field",
                v1_str=test_avro.base_schema,
                v2_str=test_avro.schema_add_required_field,
            ),
            Transform(
                name="Delete optional field",
                v1_str=test_avro.schema_add_optional_field,
                v2_str=test_avro.base_schema,
            ),
            Transform(
                name="Delete required field",
                v1_str=test_avro.schema_add_required_field,
                v2_str=test_avro.base_schema,
            ),
        ]


class JsonReporter(SerializationFormatReporter):
    title = "JSON Schema"
    schema_type = "JSON"

    def get_all_transforms(self) -> List[Transform]:
        return super().get_all_transforms()


class PbufReporter(SerializationFormatReporter):
    title = "Protocol Buffers"
    schema_type = "PROTOBUF"

    def get_all_transforms(self) -> List[Transform]:
        return super().get_all_transforms()


def generate_report():
    with open("./report.md", "w") as f:
        for reporter in [AvroReporter(), PbufReporter(), JsonReporter()]:
            reporter.test_transforms()
            for line in reporter.output_lines():
                f.write(line)
                f.write("\n")


def main(*argv):
    return generate_report()


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
