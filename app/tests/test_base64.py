from app.models.base64 import Base64Type


def test_base64_encode():
    base64_obj = Base64Type(b"MSArIDE=")
    assert base64_obj.encode_str() == "TVNBcklERT0="
    assert base64_obj.encode() == b"TVNBcklERT0="
    assert base64_obj.decode_str() == "1 + 1"
    assert base64_obj.decode() == b"1 + 1"
