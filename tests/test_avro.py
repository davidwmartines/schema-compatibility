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

schema_add_optional_field = """
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

schema_add_required_field = """
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

    ###############
    # allowed
    ###############
    def test_add_optional_field(self):
        assert self.is_compatible(base_schema, schema_add_optional_field)

    def test_delete_optional_field(self):
        assert self.is_compatible(schema_add_optional_field, base_schema)

    def test_delete_required_field(self):
        assert self.is_compatible(schema_add_required_field, base_schema)

    def test_make_required_field_optional(self):
        assert self.is_compatible(schema_add_required_field, schema_add_optional_field)

    def test_make_optional_field_required(self):
        assert self.is_compatible(schema_add_optional_field, schema_add_required_field)

    def test_rename_field_with_alias(self):
        assert self.is_compatible(base_schema, schema_rename_field_with_alias)

    def test_make_non_nullable_field_nullable(self):
        assert self.is_compatible(base_schema, schema_field_evolved_to_union)

    def test_add_type_to_union(self):
        assert self.is_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )

    # ###############
    # not allowed
    # ###############
    def test_add_required_field(self):
        assert self.not_compatible(base_schema, schema_add_required_field)

    def test_remove_type_from_union(self):
        assert self.not_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )

    def test_make_nullable_field_non_nullable(self):
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

    ###############
    # allowed
    ###############
    def test_add_optional_field(self):
        assert self.is_compatible(base_schema, schema_add_optional_field)

    def test_add_required_field(self):
        assert self.is_compatible(base_schema, schema_add_required_field)

    def test_delete_optional_field(self):
        assert self.is_compatible(schema_add_optional_field, base_schema)

    def test_make_required_field_optional(self):
        assert self.is_compatible(schema_add_required_field, schema_add_optional_field)

    def test_make_optional_field_required(self):
        assert self.is_compatible(schema_add_optional_field, schema_add_required_field)

    def test_remove_type_from_union(self):
        assert self.is_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )

    def test_make_nullable_field_non_nullable(self):
        assert self.is_compatible(schema_field_evolved_to_union, base_schema)

    # ###############
    # not allowed
    # ###############
    def test_delete_required_field(self):
        assert self.not_compatible(schema_add_required_field, base_schema)

    def test_rename_field_with_alias(self):
        assert self.not_compatible(base_schema, schema_rename_field_with_alias)

    def test_make_non_nullable_field_nullable(self):
        assert self.not_compatible(base_schema, schema_field_evolved_to_union)

    def test_add_type_to_union(self):
        assert self.not_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )


class TestFullCompatibility(SchemaTester):

    schema_type: str = "AVRO"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="full")

    ###############
    # allowed
    ###############
    def test_add_optional_field(self):
        assert self.is_compatible(base_schema, schema_add_optional_field)

    def test_delete_optional_field(self):
        assert self.is_compatible(schema_add_optional_field, base_schema)

    def test_make_required_field_optional(self):
        assert self.is_compatible(schema_add_required_field, schema_add_optional_field)

    def test_make_optional_field_required(self):
        assert self.is_compatible(schema_add_optional_field, schema_add_required_field)

    # ###############
    # not allowed
    # ###############
    def test_delete_required_field(self):
        assert self.not_compatible(schema_add_required_field, base_schema)

    def test_add_required_field(self):
        assert self.not_compatible(base_schema, schema_add_required_field)

    def test_rename_field_with_alias(self):
        assert self.not_compatible(base_schema, schema_rename_field_with_alias)

    def test_make_nullable_field_non_nullable(self):
        assert self.not_compatible(schema_field_evolved_to_union, base_schema)

    def test_make_non_nullable_field_nullable(self):
        assert self.not_compatible(base_schema, schema_field_evolved_to_union)

    def test_add_type_to_union(self):
        assert self.not_compatible(
            schema_field_evolved_to_union, schema_field_add_type_to_union
        )

    def test_remove_type_from_union(self):
        assert self.not_compatible(
            schema_field_add_type_to_union, schema_field_evolved_to_union
        )
