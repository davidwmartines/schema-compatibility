# Schema Compatibility Tests

Demonstrates various schema compatibility rules evaluated by the Confluent Schema Registry.

Backwards, Forwards, and Full compatibility is tested using **Avro**, **JSON Schema**, and **Protocol Buffers** schemas.

The compatibility types and their rules for schema changes are based on: https://docs.confluent.io/platform/current/schema-registry/avro.html#compatibility-types.

A test suite written in Python using `pytest` assertions is run, inspired by the [Confluent Avro Compatibility Test Suite](https://github.com/confluentinc/schema-registry/blob/master/core/src/test/java/io/confluent/kafka/schemaregistry/avro/AvroCompatibilityTest.java).

## Purpose
Provide information to help in choosing an appropriate serialization format for use in schema (contract) based systems where producers and consumers need to change independently.

## Schema Evolution

Schemas are evolved from one version to the next by making one or more of the following types of changes:

- Add an optional field
- Add a required field
- Delete a required field
- Delete an optional field
- Make a required field optional
- Make an optional field required
- Add a default value to a field
- Remove a default value from a field

(Re-naming a field would be considered a combination of removing and adding.)

> Note that the possible changes are limited to the serialization format. For example the `proto3` syntax does not include the ability to specify the `required` field rule or to include default field values (as in the `proto2` syntax).

> For JSON Schema, certain transitions are limited by the content models (open vs. closed) of the schemas.

## Tests

For each serialization format, for each compatibility mode, the preceding list of changes to a schema are tested for their expected compliance with the compatibility mode's rules.

## Report

To summarize the findings, a markdown document showing an example of each type of schema change (in each serialization format) with an indication of the change's compliance with each compatibility mode's rules will be generated.
