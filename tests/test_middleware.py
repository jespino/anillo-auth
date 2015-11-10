from anillo.http.responses import Response
from anillo.http.request import Request

from anillo_auth.auth import wrap_auth
from unittest import mock


def test_wrap_auth_with_invalid_parsed_data():
    func = mock.MagicMock()
    backend = mock.MagicMock()
    backend.parse = mock.MagicMock(return_value=None)
    backend.authenticate = mock.MagicMock()

    wrap_auth(backend=lambda: backend)(func)("test-request")
    assert backend.parse.called
    assert backend.parse.call_count == 1
    assert backend.parse.call_args == (("test-request",),)
    assert not backend.authenticate.called
    assert func.called
    assert func.call_count == 1


def test_wrap_auth_with_response_on_parse():
    func = mock.MagicMock()
    backend = mock.MagicMock()
    backend.parse = mock.MagicMock(return_value=Response("response-from-parse"))
    backend.authenticate = mock.MagicMock()

    response = wrap_auth(backend=lambda: backend)(func)("test-request")
    assert isinstance(response, Response)
    assert response.body == "response-from-parse"
    assert backend.parse.called
    assert backend.parse.call_count == 1
    assert backend.parse.call_args == (("test-request",),)
    assert not backend.authenticate.called
    assert not func.called


def test_wrap_auth_with_data_on_parse():
    func = mock.MagicMock()
    backend = mock.MagicMock()
    backend.parse = mock.MagicMock(return_value="test-data")
    backend.authenticate = mock.MagicMock(return_value="test-data")

    request = Request()
    wrap_auth(backend=lambda: backend)(func)(request)
    assert backend.parse.called
    assert backend.parse.call_count == 1
    assert backend.parse.call_args == ((request,),)
    assert backend.authenticate.called
    assert backend.authenticate.call_count == 1
    assert backend.authenticate.call_args == ((request, "test-data"),)
    assert func.called
    assert func.call_count == 1
    assert func.call_count == 1


def test_wrap_auth_with_data_on_parse_and_with_authenticate_return_response():
    func = mock.MagicMock()
    backend = mock.MagicMock()
    backend.parse = mock.MagicMock(return_value="test-data")
    backend.authenticate = mock.MagicMock(return_value=Response("test"))

    response = wrap_auth(backend=lambda: backend)(func)("test-request")
    assert isinstance(response, Response)
    assert response.body == "test"
    assert backend.parse.called
    assert backend.parse.call_count == 1
    assert backend.parse.call_args == (("test-request",),)
    assert backend.authenticate.called
    assert backend.authenticate.call_count == 1
    assert backend.authenticate.call_args == (("test-request", "test-data"),)
    assert not func.called
