from itsdangerous import JSONWebSignatureSerializer

from anillo.http.request import Request

from anillo_auth.backends.token import JWSBackend

serializer = JSONWebSignatureSerializer("secret")


def test_session_parse_without_token():
    backend = JWSBackend("secret")
    request = Request()
    assert backend.parse(request) is None


def test_session_parse_with_invalid_token_name():
    backend = JWSBackend("secret", "Test-Token")
    request = Request(headers={"Authorization": "Invalid: {}".format(serializer.dumps({"test": "test"}))})
    assert backend.parse(request) is None


def test_session_parse_with_invalid_token():
    backend = JWSBackend("secret", "Test-Token")
    request = Request(headers={"Authorization": "Test-Token: invalid-data"})
    assert backend.parse(request) is None


def test_session_parse_with_valid_token():
    backend = JWSBackend("secret", "Test-Token")
    request = Request(headers={"Authorization": "Test-Token: {}".format(serializer.dumps({"test": "test"}).decode())})
    assert backend.parse(request) == {"test": "test"}


def test_session_authenticate():
    backend = JWSBackend("secret")
    request = Request()
    request = backend.authenticate(request, "test-data")
    assert request.identity == "test-data"
