from uuid import uuid4

from confluent_kafka.schema_registry import Schema, SchemaRegistryClient


class SchemaTester:
    @classmethod
    def setup_class(cls):
        cls.client = SchemaRegistryClient({"url": "http://localhost:8081"})

    def is_compatible(self, from_schema: Schema, to_schema: Schema) -> bool:
        subject = str(uuid4())
        self.client.register_schema(subject, from_schema)
        return self.client.test_compatibility(subject, to_schema)

    def not_compatible(self, from_schema: Schema, to_schema: Schema) -> bool:
        return not self.is_compatible(from_schema, to_schema)
