from .base import SchemaTester

base_schema = """
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
"""

schema_add_field_with_default = """
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
"""


schema_add_field_without_default = """
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
"""


schema_rename_field_with_alias = """
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
"""


schema_field_evolved_to_union = """
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
"""

schema_field_add_type_to_union = """
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
"""


class TestBackwardsComatibility(SchemaTester):
    """
    Backward compatibility: A new schema is backward compatible if it can be used to
    read the data written in the previous schema.
    """

    schema_type = "AVRO"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="backward")

    def test_add_field_with_default(self):
        assert self.is_compatible(base_schema, schema_add_field_with_default)

    def test_add_field_without_default(self):
        assert self.not_compatible(base_schema, schema_add_field_without_default)

    def test_delete_field_with_default(self):
        assert self.is_compatible(schema_add_field_with_default, base_schema)

    def test_delete_field_without_default(self):
        assert self.is_compatible(schema_add_field_without_default, base_schema)

    def test_rename_field_with_alias(self):
        assert self.is_compatible(base_schema, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self):
        assert self.is_compatible(base_schema, schema_field_evolved_to_union)

    def test_remove_type_from_union(self):
        assert self.not_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )

    def test_add_type_to_union(self):
        assert self.is_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )

    def test_field_evolved_from_union(self):
        assert self.not_compatible(schema_field_evolved_to_union, base_schema)


class TestForwardsCompatibility(SchemaTester):
    """
    Forward compatibility: A new schema is forward compatible if the previous schema can
    read data written in this schema.
    """

    schema_type = "AVRO"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    def test_add_field_with_default(self):
        assert self.is_compatible(base_schema, schema_add_field_with_default)

    def test_add_field_without_default(self):
        assert self.is_compatible(base_schema, schema_add_field_without_default)

    def test_delete_field_with_default(self):
        assert self.is_compatible(schema_add_field_with_default, base_schema)

    def test_delete_field_without_default(self):
        assert self.not_compatible(schema_add_field_without_default, base_schema)

    def test_rename_field_with_alias(self):
        assert self.not_compatible(base_schema, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self):
        assert self.not_compatible(base_schema, schema_field_evolved_to_union)

    def test_remove_type_from_union(self):
        assert self.is_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )

    def test_add_type_to_union(self):
        assert self.not_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )

    def test_field_evolved_from_union(self):
        assert self.is_compatible(schema_field_evolved_to_union, base_schema)


class TestFullCompatibility(SchemaTester):

    schema_type: str = "AVRO"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="full")

    def test_add_field_with_default(self):
        assert self.is_compatible(base_schema, schema_add_field_with_default)

    def test_add_field_without_default(self):
        assert self.not_compatible(base_schema, schema_add_field_without_default)

    def test_delete_field_with_default(self):
        assert self.is_compatible(schema_add_field_with_default, base_schema)

    def test_delete_field_without_default(self):
        assert self.not_compatible(schema_add_field_without_default, base_schema)

    def test_rename_field_with_alias(self):
        assert self.not_compatible(base_schema, schema_rename_field_with_alias)

    def test_field_evolved_to_union(self):
        assert self.not_compatible(base_schema, schema_field_evolved_to_union)

    def test_remove_type_from_union(self):
        assert self.not_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )

    def test_add_type_to_union(self):
        assert self.not_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )

    def test_field_evolved_from_union(self):
        assert self.not_compatible(schema_field_evolved_to_union, base_schema)
