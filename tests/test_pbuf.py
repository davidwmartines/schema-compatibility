from .base import SchemaTester

schema_base = """
syntax = "proto3";

message Example {
    optional string f1 = 1;
}
"""

schema_add_field = """
syntax = "proto3";

message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
"""

schema_rename_field = """
syntax = "proto3";

message Example {
    optional string f2 = 1;
}
"""


class TestBackwardsComatibility(SchemaTester):
    """
    Backward compatibility: A new schema is backward compatible if it can be used to
    read the data written in the previous schema.
    """

    schema_type = "PROTOBUF"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="backward")

    ###############
    # allowed
    ###############
    def test_add_field(self):
        assert self.is_compatible(schema_base, schema_add_field)

    def test_delete_field(self):
        assert self.is_compatible(schema_add_field, schema_base)

    def test_rename_field(self):
        assert self.is_compatible(schema_base, schema_rename_field)


class TestForwardsComatibility(SchemaTester):
    """
    Forward compatibility: A new schema is forward compatible if the previous schema can
    read data written in this schema.
    """

    schema_type = "PROTOBUF"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="forward")

    ###############
    # allowed
    ###############
    def test_add_field(self):
        assert self.is_compatible(schema_base, schema_add_field)

    def test_delete_field(self):
        assert self.is_compatible(schema_add_field, schema_base)

    def test_rename_field(self):
        assert self.is_compatible(schema_base, schema_rename_field)


class TestFullCompatibility(SchemaTester):

    schema_type: str = "PROTOBUF"

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.client.set_compatibility(level="full")

    ###############
    # allowed
    ###############
    def test_add_field(self):
        assert self.is_compatible(schema_base, schema_add_field)

    def test_delete_field(self):
        assert self.is_compatible(schema_add_field, schema_base)
    
    def test_rename_field(self):
        assert self.is_compatible(schema_base, schema_rename_field)
