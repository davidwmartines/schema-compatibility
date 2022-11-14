import pytest
from confluent_kafka.schema_registry import SchemaRegistryClient
from uuid import uuid4


class SchemaTester:
    @classmethod
    def setup_class(cls):
        cls.client = SchemaRegistryClient({"url": "http://localhost:8081"})

    @pytest.fixture
    def subject(self):
        return str(uuid4())

    def is_compatible(self, subject, new_schema):
        return self.client.test_compatibility(subject, new_schema)

    def not_compatible(self, subject, new_schema):
        return not self.client.test_compatibility(subject, new_schema)
