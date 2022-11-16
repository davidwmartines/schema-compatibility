from .base import SchemaTester

schema_base = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"}
  },
"required": ["f1"]
}
"""

schema_add_optional_field = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"},
    "f2": {"type": "string"}
  },
  "required": ["f1"]
}
"""

schema_add_required_field = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"},
    "f2": {"type": "string"}
  },
  "required": ["f1", "f2"]
}
"""

schema_closed_base = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"}
  },
  "additionalProperties": false,
  "required": ["f1"]
}
"""

schema_closed_make_field_optional = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"}
  },
  "additionalProperties": false,
  "required": []
}
"""

schema_closed_add_optional_field = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"},
    "f2": {"type": "string"}
  },
  "additionalProperties": false,
  "required": ["f1"]
}
"""

schema_closed_add_required_field = """
{
  "type": "object",
  "properties": {
    "f1": {"type": "string"},
    "f2": {"type": "string"}
  },
  "additionalProperties": false,
  "required": ["f1", "f2"]
}
"""


class TestBackwardsComatibility_Open(SchemaTester):
    """
    Tests for backwards compatibility with open content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="backward")

    ###############
    # allowed
    ###############
    def test_open_delete_optional_field(self):
        assert self.is_compatible(schema_add_optional_field, schema_base)

    def test_open_delete_required_field(self):
        assert self.is_compatible(schema_add_required_field, schema_base)

    ###############
    # not allowed
    ###############
    def test_open_add_optional_field(self):
        assert self.not_compatible(schema_base, schema_add_optional_field)

    def test_open_add_required_field(self):
        assert self.not_compatible(schema_base, schema_add_required_field)

    def test_open_add_optional_field_closed(self):
        assert self.not_compatible(schema_base, schema_closed_add_optional_field)

    def test_open_add_required_field_closed(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)


class TestBackwardsComatibility_Closed(SchemaTester):
    """
    Tests for backwards compatibility with closed content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="backward")

    ###############
    # allowed
    ###############
    def test_closed_add_optional_field(self):
        assert self.is_compatible(schema_closed_base, schema_closed_add_optional_field)

    def test_closed_add_optional_field_open(self):
        assert self.is_compatible(schema_closed_base, schema_add_optional_field)

    def test_closed_make_field_optional(self):
        assert self.is_compatible(schema_closed_base, schema_closed_make_field_optional)

    def test_closed_delete_optional_field_open(self):
        assert self.is_compatible(schema_closed_add_optional_field, schema_base)

    def test_closed_delete_required_field_open(self):
        assert self.is_compatible(schema_closed_add_required_field, schema_base)

    ###############
    # not allowed
    ###############
    def test_closed_delete_optional_field(self):
        assert self.not_compatible(schema_closed_add_optional_field, schema_closed_base)

    def test_closed_delete_required_field(self):
        assert self.not_compatible(schema_closed_add_required_field, schema_closed_base)

    def test_closed_add_required_field(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)

    def test_closed_make_field_required(self):
        assert self.not_compatible(
            schema_closed_make_field_optional, schema_closed_base
        )


class TestForwardsCompatibility_Open(SchemaTester):
    """
    Tests for forwards compatibility with open content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    ###############
    # allowed
    ###############
    def test_open_add_optional_field(self):
        assert self.is_compatible(schema_base, schema_add_optional_field)

    def test_open_add_required_field(self):
        assert self.is_compatible(schema_base, schema_add_required_field)

    def test_open_add_optional_field_closed(self):
        assert self.is_compatible(schema_base, schema_closed_add_optional_field)

    ###############
    # not allowed
    ###############
    def test_open_delete_optional_field(self):
        assert self.not_compatible(schema_add_optional_field, schema_base)

    def test_open_delete_required_field(self):
        assert self.not_compatible(schema_add_required_field, schema_base)

    def test_open_add_required_field_closed(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)


class TestForwardsCompatibility_Closed(SchemaTester):
    """
    Tests for forwards compatibility with closed content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    ###############
    # allowed
    ###############
    def test_closed_delete_optional_field(self):
        assert self.is_compatible(schema_closed_add_optional_field, schema_closed_base)

    def test_closed_make_field_required(self):
        assert self.is_compatible(schema_closed_make_field_optional, schema_closed_base)

    ###############
    # not allowed
    ###############
    def test_closed_add_required_field(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)

    def test_closed_add_optional_field(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_optional_field)

    def test_closed_add_optional_field_open(self):
        assert self.not_compatible(schema_closed_base, schema_add_optional_field)

    def test_closed_delete_required_field(self):
        assert self.not_compatible(schema_closed_add_required_field, schema_closed_base)

    def test_closed_make_field_optional(self):
        assert self.not_compatible(
            schema_closed_base, schema_closed_make_field_optional
        )

    def test_closed_delete_optional_field_open(self):
        assert self.not_compatible(schema_closed_add_optional_field, schema_base)

    def test_closed_delete_required_field_open(self):
        assert self.not_compatible(schema_closed_add_required_field, schema_base)


class TestFullCompatibility_Open(SchemaTester):
    """
    Tests for full compatibility with open content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    ###############
    # allowed
    ###############
    def test_open_add_optional_field(self):
        assert self.is_compatible(schema_base, schema_add_optional_field)

    def test_open_add_required_field(self):
        assert self.is_compatible(schema_base, schema_add_required_field)

    def test_open_add_optional_field_closed(self):
        assert self.is_compatible(schema_base, schema_closed_add_optional_field)

    ###############
    # not allowed
    ###############
    def test_open_add_required_field_closed(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)

    def test_open_delete_optional_field(self):
        assert self.not_compatible(schema_add_optional_field, schema_base)

    def test_open_delete_required_field(self):
        assert self.not_compatible(schema_add_required_field, schema_base)


class TestFullCompatibility_Closed(SchemaTester):
    """
    Tests for Full compatibility with closed content model schemas.
    """

    schema_type = "JSON"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    ###############
    # allowed
    ###############
    def test_closed_make_field_required(self):
        assert self.is_compatible(schema_closed_make_field_optional, schema_closed_base)

    def test_closed_delete_optional_field(self):
        assert self.is_compatible(schema_closed_add_optional_field, schema_closed_base)

    ###############
    # not allowed
    ###############
    def test_closed_add_required_field(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_required_field)

    def test_closed_delete_required_field(self):
        assert self.not_compatible(schema_closed_add_required_field, schema_closed_base)

    def test_closed_add_optional_field(self):
        assert self.not_compatible(schema_closed_base, schema_closed_add_optional_field)

    def test_closed_add_optional_field_open(self):
        assert self.not_compatible(schema_closed_base, schema_add_optional_field)

    def test_closed_make_field_optional(self):
        assert self.not_compatible(
            schema_closed_base, schema_closed_make_field_optional
        )

    def test_closed_delete_optional_field_open(self):
        assert self.not_compatible(schema_closed_add_optional_field, schema_base)

    def test_closed_delete_required_field_open(self):
        assert self.not_compatible(schema_closed_add_required_field, schema_base)
