import pytest
from uuid import uuid4
from confluent_kafka.schema_registry import SchemaRegistryClient, Schema

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


class TestBackwardsComatibility:
    """
    Backward compatibility: A new schema is backward compatible if it can be used to
    read the data written in the previous schema.
    """

    @classmethod
    def setup_class(cls):
        cls.client = SchemaRegistryClient({"url": "http://localhost:8081"})
        cls.client.set_compatibility(level="backward")

    @pytest.fixture
    def subject(self):
        return str(uuid4())

    def _is_compatible(self, subject, new_schema):
        return self.client.test_compatibility(subject, new_schema)

    def _not_compatible(self, subject, new_schema):
        return not self.client.test_compatibility(subject, new_schema)

    def test_add_field_with_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self._is_compatible(subject, schema_add_field_with_default)

    def test_add_field_without_default(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self._not_compatible(subject, schema_add_field_without_default)

    def test_rename_field_with_alias(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self._is_compatible(subject, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self, subject):
        self.client.register_schema(subject, base_schema)
        assert self._is_compatible(subject, schema_field_evolved_to_union)

    def test_remove_type_from_union(self, subject):
        self.client.register_schema(subject, schema_field_add_type_to_union)
        assert self._not_compatible(subject, schema_field_evolved_to_union)

    def test_add_type_to_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self._is_compatible(subject, schema_field_add_type_to_union)

    def test_field_evolved_from_union(self, subject):
        self.client.register_schema(subject, schema_field_evolved_to_union)
        assert self._not_compatible(subject, base_schema)
