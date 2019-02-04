# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocol.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protocol.proto',
  package='proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0eprotocol.proto\x12\x05proto\")\n\x06Vector\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"D\n\nConnection\x12\x14\n\x0c\x63onnected_to\x18\x01 \x01(\x04\x12 \n\tdirection\x18\x02 \x01(\x0b\x32\r.proto.Vector\"\x7f\n\x04\x43\x65ll\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x1a\n\x03pos\x18\x02 \x01(\x0b\x32\r.proto.Vector\x12\x1a\n\x03vel\x18\x03 \x01(\x0b\x32\r.proto.Vector\x12\x0b\n\x03\x64na\x18\x04 \x01(\x0c\x12&\n\x0b\x63onnections\x18\x05 \x03(\x0b\x32\x11.proto.Connection\"u\n\x10\x43\x65llComputeBatch\x12\x11\n\ttime_step\x18\x01 \x01(\x04\x12%\n\x10\x63\x65lls_to_compute\x18\x02 \x03(\x0b\x32\x0b.proto.Cell\x12\'\n\x12\x63\x65lls_in_proximity\x18\x03 \x03(\x0b\x32\x0b.proto.Cell2e\n\x16\x43\x65llInteractionService\x12K\n\x17\x43omputeCellInteractions\x12\x17.proto.CellComputeBatch\x1a\x17.proto.CellComputeBatchb\x06proto3')
)




_VECTOR = _descriptor.Descriptor(
  name='Vector',
  full_name='proto.Vector',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='proto.Vector.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='proto.Vector.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='z', full_name='proto.Vector.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=66,
)


_CONNECTION = _descriptor.Descriptor(
  name='Connection',
  full_name='proto.Connection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connected_to', full_name='proto.Connection.connected_to', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='proto.Connection.direction', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=136,
)


_CELL = _descriptor.Descriptor(
  name='Cell',
  full_name='proto.Cell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='proto.Cell.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='proto.Cell.pos', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vel', full_name='proto.Cell.vel', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dna', full_name='proto.Cell.dna', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='connections', full_name='proto.Cell.connections', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=138,
  serialized_end=265,
)


_CELLCOMPUTEBATCH = _descriptor.Descriptor(
  name='CellComputeBatch',
  full_name='proto.CellComputeBatch',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_step', full_name='proto.CellComputeBatch.time_step', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cells_to_compute', full_name='proto.CellComputeBatch.cells_to_compute', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cells_in_proximity', full_name='proto.CellComputeBatch.cells_in_proximity', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=267,
  serialized_end=384,
)

_CONNECTION.fields_by_name['direction'].message_type = _VECTOR
_CELL.fields_by_name['pos'].message_type = _VECTOR
_CELL.fields_by_name['vel'].message_type = _VECTOR
_CELL.fields_by_name['connections'].message_type = _CONNECTION
_CELLCOMPUTEBATCH.fields_by_name['cells_to_compute'].message_type = _CELL
_CELLCOMPUTEBATCH.fields_by_name['cells_in_proximity'].message_type = _CELL
DESCRIPTOR.message_types_by_name['Vector'] = _VECTOR
DESCRIPTOR.message_types_by_name['Connection'] = _CONNECTION
DESCRIPTOR.message_types_by_name['Cell'] = _CELL
DESCRIPTOR.message_types_by_name['CellComputeBatch'] = _CELLCOMPUTEBATCH
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Vector = _reflection.GeneratedProtocolMessageType('Vector', (_message.Message,), dict(
  DESCRIPTOR = _VECTOR,
  __module__ = 'protocol_pb2'
  # @@protoc_insertion_point(class_scope:proto.Vector)
  ))
_sym_db.RegisterMessage(Vector)

Connection = _reflection.GeneratedProtocolMessageType('Connection', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTION,
  __module__ = 'protocol_pb2'
  # @@protoc_insertion_point(class_scope:proto.Connection)
  ))
_sym_db.RegisterMessage(Connection)

Cell = _reflection.GeneratedProtocolMessageType('Cell', (_message.Message,), dict(
  DESCRIPTOR = _CELL,
  __module__ = 'protocol_pb2'
  # @@protoc_insertion_point(class_scope:proto.Cell)
  ))
_sym_db.RegisterMessage(Cell)

CellComputeBatch = _reflection.GeneratedProtocolMessageType('CellComputeBatch', (_message.Message,), dict(
  DESCRIPTOR = _CELLCOMPUTEBATCH,
  __module__ = 'protocol_pb2'
  # @@protoc_insertion_point(class_scope:proto.CellComputeBatch)
  ))
_sym_db.RegisterMessage(CellComputeBatch)



_CELLINTERACTIONSERVICE = _descriptor.ServiceDescriptor(
  name='CellInteractionService',
  full_name='proto.CellInteractionService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=386,
  serialized_end=487,
  methods=[
  _descriptor.MethodDescriptor(
    name='ComputeCellInteractions',
    full_name='proto.CellInteractionService.ComputeCellInteractions',
    index=0,
    containing_service=None,
    input_type=_CELLCOMPUTEBATCH,
    output_type=_CELLCOMPUTEBATCH,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CELLINTERACTIONSERVICE)

DESCRIPTOR.services_by_name['CellInteractionService'] = _CELLINTERACTIONSERVICE

# @@protoc_insertion_point(module_scope)
