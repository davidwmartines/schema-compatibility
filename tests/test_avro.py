from .base import SchemaTester
from uuid import uuid4
from confluent_kafka.schema_registry import Schema

SCHEMA_TYPE = "AVRO"

base_schema = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1",
      "type": "string"
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)

schema_add_field_with_default = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1",
      "type": "string"
    },
    {
      "name": "f2",
      "type": "string",
      "default": "foo"
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)


schema_add_field_without_default = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1",
      "type": "string"
    },
    {
      "name": "f2",
      "type": "string"
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)


schema_rename_field_with_alias = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1_new",
      "type": "string",
      "aliases": ["f1"]
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)


schema_field_evolved_to_union = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1",
      "type": ["null", "string"]
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)

schema_field_add_type_to_union = Schema(
    schema_str="""
{
  "namespace": "test",
  "name": "myrecord",
  "type": "record",
  "fields": [
    {
      "name": "f1",
      "type": ["null", "string", "int"]
    }
  ]
}
""",
    schema_type=SCHEMA_TYPE,
)


class TestBackwardsComatibility(SchemaTester):
    """
    Backward compatibility: A new schema is backward compatible if it can be used to
    read the data written in the previous schema.
    """

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="backward")

    def test_add_field_with_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.is_compatible(subject, schema_add_field_with_default)

    def test_add_field_without_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.not_compatible(subject, schema_add_field_without_default)

    def test_rename_field_with_alias(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.is_compatible(subject, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.is_compatible(subject, schema_field_evolved_to_union)

    def test_remove_type_from_union(self, subject):
        self.client.register_schema(subject, schema_field_add_type_to_union)
        assert self.not_compatible(subject, schema_field_evolved_to_union)

    def test_add_type_to_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self.is_compatible(subject, schema_field_add_type_to_union)

    def test_field_evolved_from_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self.not_compatible(subject, base_schema)


class TestForwardsCompatibility(SchemaTester):
    """
    Forward compatibility: A new schema is forward compatible if the previous schema can
    read data written in this schema.
    """

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    def test_add_field_with_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.is_compatible(subject, schema_add_field_with_default)

    def test_add_field_without_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.is_compatible(subject, schema_add_field_without_default)

    def test_rename_field_with_alias(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.not_compatible(subject, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self.not_compatible(subject, schema_field_evolved_to_union)

    def test_remove_type_from_union(self, subject):
        self.client.register_schema(subject, schema_field_add_type_to_union)
        assert self.is_compatible(subject, schema_field_evolved_to_union)

    def test_add_type_to_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self.not_compatible(subject, schema_field_add_type_to_union)

    def test_field_evolved_from_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self.is_compatible(subject, base_schema)
