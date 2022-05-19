import base64
import binascii
from typing import Any

from pydantic import BaseModel, PydanticTypeError, ValidationError
from pydantic.errors import DictError


# Create Base64Error class
class Base64Error(PydanticTypeError):
    msg_template = "value is not valid base64"


class Base64Type:
    def __init__(self, decoded_bytes: bytes):
        self._decoded_bytes: bytes = decoded_bytes

    def data(self) -> str:
        return self._decoded_bytes

    def encode(self) -> bytes:
        return base64.b64encode(self._decoded_bytes)

    def encode_str(self) -> str:
        return self.encode().decode()

    def decode(self) -> bytes:
        return base64.b64decode(self._decoded_bytes)

    def decode_str(self) -> str:
        return base64.b64decode(self._decoded_bytes).decode()

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

    @classmethod
    def validate(cls, value) -> "Base64Type":
        if isinstance(value, Base64Type):
            return value
        if isinstance(value, str):
            value = value.encode()
        elif isinstance(value, int):
            raise Base64Error
        elif not isinstance(value, (bytes, bytearray, memoryview)):
            value = bytes(value)

        return cls(value)
