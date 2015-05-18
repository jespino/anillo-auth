import base64

from anillo.http.request import Request
from anillo.http.responses import Response

from anillo_auth.backends.http_auth import HttpBasicAuthBackend


def test_http_auth_parse_with_not_auth_data():
    backend = HttpBasicAuthBackend(lambda x, y: x)
    request = Request()
    assert backend.parse(request) is None


def test_http_auth_parse_with_invalid_auth_header():
    backend = HttpBasicAuthBackend(lambda x, y: x)
    request = Request(headers={"Authorization": "invalid-data"})
    assert backend.parse(request) is None


def test_http_auth_parse_with_invalid_auth_data():
    backend = HttpBasicAuthBackend(lambda x, y: x)
    request = Request(headers={"Authorization": "Basic: invalid-data"})
    assert backend.parse(request) is None


def test_http_auth_parse_with_valid_auth_data():
    backend = HttpBasicAuthBackend(lambda x, y: x)
    request = Request(headers={"Authorization": "Basic: {}".format(base64.b64encode(b"test-user:test-pass").decode())})
    assert backend.parse(request) == {"username": "test-user", "password": "test-pass"}


def test_http_auth_authenticate_with_invalid_user():
    backend = HttpBasicAuthBackend(lambda x, y: None)
    request = Request()
    request = backend.authenticate(request, {"username": "test", "password": "test"})
    assert request.identity is None


def test_http_auth_authenticate_when_handler_returns_a_response():
    backend = HttpBasicAuthBackend(lambda x, y: Response("test"))
    request = Request()
    response = backend.authenticate(request, {"username": "test", "password": "test"})
    assert isinstance(response, Response)
    assert response.body == "test"


def test_http_auth_authenticate_when_handler_returns_data():
    backend = HttpBasicAuthBackend(lambda x, y: {"user_id": 1})
    request = Request()
    request = backend.authenticate(request, {"username": "test", "password": "test"})
    assert request.identity == {"user_id": 1}
