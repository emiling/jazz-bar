# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chord.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chord.proto',
  package='chord',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0b\x63hord.proto\x12\x05\x63hord\"\x1b\n\x0bHealthCheck\x12\x0c\n\x04ping\x18\x01 \x01(\r\"\x1b\n\x0bHealthReply\x12\x0c\n\x04pong\x18\x01 \x01(\r\"1\n\nNodeDetail\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x12\n\nwhich_node\x18\x02 \x01(\r\"@\n\x07NodeVal\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x11\n\tnode_host\x18\x02 \x01(\t\x12\x11\n\tnode_port\x18\x03 \x01(\t\"U\n\x08NodeType\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x11\n\tnode_host\x18\x02 \x01(\t\x12\x11\n\tnode_port\x18\x03 \x01(\t\x12\x12\n\nwhich_node\x18\x04 \x01(\r\"V\n\x07Message\x12\x0f\n\x07node_id\x18\x01 \x01(\t\x12\x11\n\tnode_host\x18\x02 \x01(\t\x12\x11\n\tnode_port\x18\x03 \x01(\t\x12\x14\n\x0cmessage_type\x18\x04 \x01(\r2B\n\rHealthChecker\x12\x31\n\x05\x43heck\x12\x12.chord.HealthCheck\x1a\x12.chord.HealthReply\"\x00\x32\x41\n\x0cGetNodeValue\x12\x31\n\nGetNodeVal\x12\x11.chord.NodeDetail\x1a\x0e.chord.NodeVal\"\x00\x32H\n\nNotifyNode\x12:\n\x11NotifyNodeChanged\x12\x0f.chord.NodeType\x1a\x12.chord.HealthReply\"\x00\x32\x39\n\x0bTossMessage\x12*\n\x02TM\x12\x0e.chord.Message\x1a\x12.chord.HealthReply\"\x00\x62\x06proto3'
)




_HEALTHCHECK = _descriptor.Descriptor(
  name='HealthCheck',
  full_name='chord.HealthCheck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ping', full_name='chord.HealthCheck.ping', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=22,
  serialized_end=49,
)


_HEALTHREPLY = _descriptor.Descriptor(
  name='HealthReply',
  full_name='chord.HealthReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pong', full_name='chord.HealthReply.pong', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=51,
  serialized_end=78,
)


_NODEDETAIL = _descriptor.Descriptor(
  name='NodeDetail',
  full_name='chord.NodeDetail',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='chord.NodeDetail.node_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='which_node', full_name='chord.NodeDetail.which_node', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=80,
  serialized_end=129,
)


_NODEVAL = _descriptor.Descriptor(
  name='NodeVal',
  full_name='chord.NodeVal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='chord.NodeVal.node_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_host', full_name='chord.NodeVal.node_host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_port', full_name='chord.NodeVal.node_port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=131,
  serialized_end=195,
)


_NODETYPE = _descriptor.Descriptor(
  name='NodeType',
  full_name='chord.NodeType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='chord.NodeType.node_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_host', full_name='chord.NodeType.node_host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_port', full_name='chord.NodeType.node_port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='which_node', full_name='chord.NodeType.which_node', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=197,
  serialized_end=282,
)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='chord.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='chord.Message.node_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_host', full_name='chord.Message.node_host', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_port', full_name='chord.Message.node_port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_type', full_name='chord.Message.message_type', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=284,
  serialized_end=370,
)

DESCRIPTOR.message_types_by_name['HealthCheck'] = _HEALTHCHECK
DESCRIPTOR.message_types_by_name['HealthReply'] = _HEALTHREPLY
DESCRIPTOR.message_types_by_name['NodeDetail'] = _NODEDETAIL
DESCRIPTOR.message_types_by_name['NodeVal'] = _NODEVAL
DESCRIPTOR.message_types_by_name['NodeType'] = _NODETYPE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HealthCheck = _reflection.GeneratedProtocolMessageType('HealthCheck', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHCHECK,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.HealthCheck)
  })
_sym_db.RegisterMessage(HealthCheck)

HealthReply = _reflection.GeneratedProtocolMessageType('HealthReply', (_message.Message,), {
  'DESCRIPTOR' : _HEALTHREPLY,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.HealthReply)
  })
_sym_db.RegisterMessage(HealthReply)

NodeDetail = _reflection.GeneratedProtocolMessageType('NodeDetail', (_message.Message,), {
  'DESCRIPTOR' : _NODEDETAIL,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.NodeDetail)
  })
_sym_db.RegisterMessage(NodeDetail)

NodeVal = _reflection.GeneratedProtocolMessageType('NodeVal', (_message.Message,), {
  'DESCRIPTOR' : _NODEVAL,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.NodeVal)
  })
_sym_db.RegisterMessage(NodeVal)

NodeType = _reflection.GeneratedProtocolMessageType('NodeType', (_message.Message,), {
  'DESCRIPTOR' : _NODETYPE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.NodeType)
  })
_sym_db.RegisterMessage(NodeType)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:chord.Message)
  })
_sym_db.RegisterMessage(Message)



_HEALTHCHECKER = _descriptor.ServiceDescriptor(
  name='HealthChecker',
  full_name='chord.HealthChecker',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=372,
  serialized_end=438,
  methods=[
  _descriptor.MethodDescriptor(
    name='Check',
    full_name='chord.HealthChecker.Check',
    index=0,
    containing_service=None,
    input_type=_HEALTHCHECK,
    output_type=_HEALTHREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_HEALTHCHECKER)

DESCRIPTOR.services_by_name['HealthChecker'] = _HEALTHCHECKER


_GETNODEVALUE = _descriptor.ServiceDescriptor(
  name='GetNodeValue',
  full_name='chord.GetNodeValue',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=440,
  serialized_end=505,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetNodeVal',
    full_name='chord.GetNodeValue.GetNodeVal',
    index=0,
    containing_service=None,
    input_type=_NODEDETAIL,
    output_type=_NODEVAL,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GETNODEVALUE)

DESCRIPTOR.services_by_name['GetNodeValue'] = _GETNODEVALUE


_NOTIFYNODE = _descriptor.ServiceDescriptor(
  name='NotifyNode',
  full_name='chord.NotifyNode',
  file=DESCRIPTOR,
  index=2,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=507,
  serialized_end=579,
  methods=[
  _descriptor.MethodDescriptor(
    name='NotifyNodeChanged',
    full_name='chord.NotifyNode.NotifyNodeChanged',
    index=0,
    containing_service=None,
    input_type=_NODETYPE,
    output_type=_HEALTHREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_NOTIFYNODE)

DESCRIPTOR.services_by_name['NotifyNode'] = _NOTIFYNODE


_TOSSMESSAGE = _descriptor.ServiceDescriptor(
  name='TossMessage',
  full_name='chord.TossMessage',
  file=DESCRIPTOR,
  index=3,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=581,
  serialized_end=638,
  methods=[
  _descriptor.MethodDescriptor(
    name='TM',
    full_name='chord.TossMessage.TM',
    index=0,
    containing_service=None,
    input_type=_MESSAGE,
    output_type=_HEALTHREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_TOSSMESSAGE)

DESCRIPTOR.services_by_name['TossMessage'] = _TOSSMESSAGE

# @@protoc_insertion_point(module_scope)