from app.models.base64 import Base64Type


def test_base64_encode():
    base64_obj = Base64Type(b"Hello World")
    assert base64_obj.encode_str() == "SGVsbG8gV29ybGQ="
    assert base64_obj.encode() == b"SGVsbG8gV29ybGQ="
    assert base64_obj.decode_str() == "Hello World"
    assert base64_obj.decode() == b"Hello World"
