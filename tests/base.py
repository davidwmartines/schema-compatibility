from uuid import uuid4

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient


class SchemaTester:

    schema_type: str = None

    @classmethod
    def setup_class(cls):
        cls.client = SchemaRegistryClient({"url": "http://localhost:8081"})

    def is_compatible(self, from_schema: str, to_schema: str) -> bool:
        subject = str(uuid4())
        self.client.register_schema(
            subject, Schema(schema_str=from_schema, schema_type=self.schema_type)
        )
        return self.client.test_compatibility(
            subject, Schema(schema_str=to_schema, schema_type=self.schema_type)
        )

    def not_compatible(self, from_schema: str, to_schema: str) -> bool:
        return not self.is_compatible(from_schema, to_schema)
