# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: esw_server.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x65sw_server.proto\"\x87\x01\n\x07Request\x12%\n\x08getCount\x18\x01 \x01(\x0b\x32\x11.Request.GetCountH\x00\x12\'\n\tpostWords\x18\x02 \x01(\x0b\x32\x12.Request.PostWordsH\x00\x1a\n\n\x08GetCount\x1a\x19\n\tPostWords\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x42\x05\n\x03msg\"j\n\x08Response\x12 \n\x06status\x18\x01 \x01(\x0e\x32\x10.Response.Status\x12\x0f\n\x07\x63ounter\x18\x02 \x01(\x05\x12\x0e\n\x06\x65rrMsg\x18\x03 \x01(\t\"\x1b\n\x06Status\x12\x06\n\x02OK\x10\x00\x12\t\n\x05\x45RROR\x10\x01\x42 \n\x1c\x63z.cvut.fel.esw.server.protoP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'esw_server_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034cz.cvut.fel.esw.server.protoP\001'
  _REQUEST._serialized_start=21
  _REQUEST._serialized_end=156
  _REQUEST_GETCOUNT._serialized_start=112
  _REQUEST_GETCOUNT._serialized_end=122
  _REQUEST_POSTWORDS._serialized_start=124
  _REQUEST_POSTWORDS._serialized_end=149
  _RESPONSE._serialized_start=158
  _RESPONSE._serialized_end=264
  _RESPONSE_STATUS._serialized_start=237
  _RESPONSE_STATUS._serialized_end=264
# @@protoc_insertion_point(module_scope)
