# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hfc/protos/common/ledger.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='hfc/protos/common/ledger.proto',
  package='common',
  syntax='proto3',
  serialized_options=_b('\n$org.hyperledger.fabric.protos.commonZ+github.com/hyperledger/fabric/protos/common'),
  serialized_pb=_b('\n\x1ehfc/protos/common/ledger.proto\x12\x06\x63ommon\"U\n\x0e\x42lockchainInfo\x12\x0e\n\x06height\x18\x01 \x01(\x04\x12\x18\n\x10\x63urrentBlockHash\x18\x02 \x01(\x0c\x12\x19\n\x11previousBlockHash\x18\x03 \x01(\x0c\x42S\n$org.hyperledger.fabric.protos.commonZ+github.com/hyperledger/fabric/protos/commonb\x06proto3')
)




_BLOCKCHAININFO = _descriptor.Descriptor(
  name='BlockchainInfo',
  full_name='common.BlockchainInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='height', full_name='common.BlockchainInfo.height', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currentBlockHash', full_name='common.BlockchainInfo.currentBlockHash', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='previousBlockHash', full_name='common.BlockchainInfo.previousBlockHash', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=42,
  serialized_end=127,
)

DESCRIPTOR.message_types_by_name['BlockchainInfo'] = _BLOCKCHAININFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BlockchainInfo = _reflection.GeneratedProtocolMessageType('BlockchainInfo', (_message.Message,), dict(
  DESCRIPTOR = _BLOCKCHAININFO,
  __module__ = 'hfc.protos.common.ledger_pb2'
  # @@protoc_insertion_point(class_scope:common.BlockchainInfo)
  ))
_sym_db.RegisterMessage(BlockchainInfo)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
