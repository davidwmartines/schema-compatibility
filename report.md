# Schema Evolution Compatibility
Generated on 2022-11-16T17:09:46.487607
## Summary
### [Avro](#Avro)

[Backwards Compatibility](#Avro_backward)
 - Allowed transformations

   - [Add optional field](#Avro_backward_Add_optional_field)

   - [Delete optional field](#Avro_backward_Delete_optional_field)

   - [Delete required field](#Avro_backward_Delete_required_field)

   - [Make required field optional](#Avro_backward_Make_required_field_optional)

   - [Make optional field required](#Avro_backward_Make_optional_field_required)

   - [Rename field with alias](#Avro_backward_Rename_field_with_alias)

   - [Make non-nullable field nullable](#Avro_backward_Make_non-nullable_field_nullable)

   - [Add type to union](#Avro_backward_Add_type_to_union)

 - Non-allowed transformations

   - [Add required field](#Avro_backward_Add_required_field)

   - [Make nullable field non-nullable](#Avro_backward_Make_nullable_field_non-nullable)

   - [Remove type from union](#Avro_backward_Remove_type_from_union)

[Forwards Compatibility](#Avro_forward)
 - Allowed transformations

   - [Add optional field](#Avro_forward_Add_optional_field)

   - [Delete optional field](#Avro_forward_Delete_optional_field)

   - [Add required field](#Avro_forward_Add_required_field)

   - [Make required field optional](#Avro_forward_Make_required_field_optional)

   - [Make optional field required](#Avro_forward_Make_optional_field_required)

   - [Make nullable field non-nullable](#Avro_forward_Make_nullable_field_non-nullable)

   - [Remove type from union](#Avro_forward_Remove_type_from_union)

 - Non-allowed transformations

   - [Delete required field](#Avro_forward_Delete_required_field)

   - [Rename field with alias](#Avro_forward_Rename_field_with_alias)

   - [Make non-nullable field nullable](#Avro_forward_Make_non-nullable_field_nullable)

   - [Add type to union](#Avro_forward_Add_type_to_union)

[Full Compatibility](#Avro_full)
 - Allowed transformations

   - [Add optional field](#Avro_full_Add_optional_field)

   - [Delete optional field](#Avro_full_Delete_optional_field)

   - [Make required field optional](#Avro_full_Make_required_field_optional)

   - [Make optional field required](#Avro_full_Make_optional_field_required)

 - Non-allowed transformations

   - [Add required field](#Avro_full_Add_required_field)

   - [Delete required field](#Avro_full_Delete_required_field)

   - [Rename field with alias](#Avro_full_Rename_field_with_alias)

   - [Make non-nullable field nullable](#Avro_full_Make_non-nullable_field_nullable)

   - [Make nullable field non-nullable](#Avro_full_Make_nullable_field_non-nullable)

   - [Add type to union](#Avro_full_Add_type_to_union)

   - [Remove type from union](#Avro_full_Remove_type_from_union)

### [Protocol Buffers](#Protocol_Buffers)

[Backwards Compatibility](#Protocol_Buffers_backward)
 - Allowed transformations

   - [Add Field](#Protocol_Buffers_backward_Add_Field)

   - [Delete Field](#Protocol_Buffers_backward_Delete_Field)

   - [Rename Field Number](#Protocol_Buffers_backward_Rename_Field_Number)

 - Non-allowed transformations

[Forwards Compatibility](#Protocol_Buffers_forward)
 - Allowed transformations

   - [Add Field](#Protocol_Buffers_forward_Add_Field)

   - [Delete Field](#Protocol_Buffers_forward_Delete_Field)

   - [Rename Field Number](#Protocol_Buffers_forward_Rename_Field_Number)

 - Non-allowed transformations

[Full Compatibility](#Protocol_Buffers_full)
 - Allowed transformations

   - [Add Field](#Protocol_Buffers_full_Add_Field)

   - [Delete Field](#Protocol_Buffers_full_Delete_Field)

   - [Rename Field Number](#Protocol_Buffers_full_Rename_Field_Number)

 - Non-allowed transformations

### [JSON Schema](#JSON_Schema)

[Backwards Compatibility](#JSON_Schema_backward)
 - Allowed transformations

 - Non-allowed transformations

[Forwards Compatibility](#JSON_Schema_forward)
 - Allowed transformations

 - Non-allowed transformations

[Full Compatibility](#JSON_Schema_full)
 - Allowed transformations

 - Non-allowed transformations

## Details
# <a id="Avro"></a>Avro

## <a id="Avro_backward"></a>Backwards Compatibility
A new schema is backward compatible if it can be used to read the data written in the previous schema.
### <a id="Avro_backward_Add_optional_field"></a>Add optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Delete_optional_field"></a>Delete optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Delete_required_field"></a>Delete required field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Make_required_field_optional"></a>Make required field optional

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Make_optional_field_required"></a>Make optional field required

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Rename_field_with_alias"></a>Rename field with alias

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Make_non-nullable_field_nullable"></a>Make non-nullable field nullable

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Add_type_to_union"></a>Add type to union

V1
```json
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
```
V2
```json
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
```

## Changes that break Backwards Compatibility


### <a id="Avro_backward_Add_required_field"></a>Add required field *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Make_nullable_field_non-nullable"></a>Make nullable field non-nullable *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_backward_Remove_type_from_union"></a>Remove type from union *(not permitted)*

V1
```json
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
```
V2
```json
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
```
---
## <a id="Avro_forward"></a>Forwards Compatibility
A new schema is forward compatible if the previous schema can read data written in this schema.
### <a id="Avro_forward_Add_optional_field"></a>Add optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Delete_optional_field"></a>Delete optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Add_required_field"></a>Add required field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Make_required_field_optional"></a>Make required field optional

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Make_optional_field_required"></a>Make optional field required

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Make_nullable_field_non-nullable"></a>Make nullable field non-nullable

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Remove_type_from_union"></a>Remove type from union

V1
```json
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
```
V2
```json
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
```

## Changes that break Forwards Compatibility


### <a id="Avro_forward_Delete_required_field"></a>Delete required field *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Rename_field_with_alias"></a>Rename field with alias *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Make_non-nullable_field_nullable"></a>Make non-nullable field nullable *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_forward_Add_type_to_union"></a>Add type to union *(not permitted)*

V1
```json
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
```
V2
```json
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
```
---
## <a id="Avro_full"></a>Full Compatibility
A new schema is fully compatible if it's both backward and forward compatible.
### <a id="Avro_full_Add_optional_field"></a>Add optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Delete_optional_field"></a>Delete optional field

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Make_required_field_optional"></a>Make required field optional

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Make_optional_field_required"></a>Make optional field required

V1
```json
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
```
V2
```json
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
```

## Changes that break Full Compatibility


### <a id="Avro_full_Add_required_field"></a>Add required field *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Delete_required_field"></a>Delete required field *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Rename_field_with_alias"></a>Rename field with alias *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Make_non-nullable_field_nullable"></a>Make non-nullable field nullable *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Make_nullable_field_non-nullable"></a>Make nullable field non-nullable *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Add_type_to_union"></a>Add type to union *(not permitted)*

V1
```json
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
```
V2
```json
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
```
### <a id="Avro_full_Remove_type_from_union"></a>Remove type from union *(not permitted)*

V1
```json
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
```
V2
```json
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
```
---

# <a id="Protocol_Buffers"></a>Protocol Buffers

## <a id="Protocol_Buffers_backward"></a>Backwards Compatibility
A new schema is backward compatible if it can be used to read the data written in the previous schema.
### <a id="Protocol_Buffers_backward_Add_Field"></a>Add Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
### <a id="Protocol_Buffers_backward_Delete_Field"></a>Delete Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
### <a id="Protocol_Buffers_backward_Rename_Field_Number"></a>Rename Field Number

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f2 = 1;
}
```

## Changes that break Backwards Compatibility

*(none)*
---
## <a id="Protocol_Buffers_forward"></a>Forwards Compatibility
A new schema is forward compatible if the previous schema can read data written in this schema.
### <a id="Protocol_Buffers_forward_Add_Field"></a>Add Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
### <a id="Protocol_Buffers_forward_Delete_Field"></a>Delete Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
### <a id="Protocol_Buffers_forward_Rename_Field_Number"></a>Rename Field Number

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f2 = 1;
}
```

## Changes that break Forwards Compatibility

*(none)*
---
## <a id="Protocol_Buffers_full"></a>Full Compatibility
A new schema is fully compatible if it's both backward and forward compatible.
### <a id="Protocol_Buffers_full_Add_Field"></a>Add Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
### <a id="Protocol_Buffers_full_Delete_Field"></a>Delete Field

V1
```Protocol Buffer
syntax = "proto3";
message Example {
  optional string f1 = 1;
  optional string f2 = 2;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
### <a id="Protocol_Buffers_full_Rename_Field_Number"></a>Rename Field Number

V1
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f1 = 1;
}
```
V2
```Protocol Buffer
syntax = "proto3";
message Example {
    optional string f2 = 1;
}
```

## Changes that break Full Compatibility

*(none)*
---

# <a id="JSON_Schema"></a>JSON Schema

## <a id="JSON_Schema_backward"></a>Backwards Compatibility
A new schema is backward compatible if it can be used to read the data written in the previous schema.

## Changes that break Backwards Compatibility

*(none)*
---
## <a id="JSON_Schema_forward"></a>Forwards Compatibility
A new schema is forward compatible if the previous schema can read data written in this schema.

## Changes that break Forwards Compatibility

*(none)*
---
## <a id="JSON_Schema_full"></a>Full Compatibility
A new schema is fully compatible if it's both backward and forward compatible.

## Changes that break Full Compatibility

*(none)*
---

