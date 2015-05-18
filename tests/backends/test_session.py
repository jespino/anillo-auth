from anillo.http.request import Request

from anillo_auth.backends.session import SessionBackend


def test_session_parse_with_not_valid_session():
    backend = SessionBackend()
    request = Request()
    assert backend.parse(request) is None


def test_session_parse_with_session_without_identity():
    backend = SessionBackend()
    request = Request()
    request.session = {}
    assert backend.parse(request) is None


def test_session_parse_with_session_with_identity():
    backend = SessionBackend()
    request = Request()
    request.session = {"identity": "test"}
    assert backend.parse(request) == "test"


def test_session_authenticate():
    backend = SessionBackend()
    request = Request()
    request = backend.authenticate(request, "test-data")
    assert request.identity == "test-data"
