# Anillo-Auth middleware

[![Build Status](http://img.shields.io/travis/jespino/anillo-auth.svg?branch=master)](https://travis-ci.org/jespino/anillo-auth)
[![Coveralls Status](http://img.shields.io/coveralls/jespino/anillo-auth/master.svg)](https://coveralls.io/r/jespino/anillo-auth)
[![Development Status](https://pypip.in/status/anillo-auth/badge.svg)](https://pypi.python.org/pypi/anillo-auth/)
[![Latest Version](https://pypip.in/version/anillo-auth/badge.svg)](https://pypi.python.org/pypi/anillo-auth/)
[![Supported Python versions](https://pypip.in/py_versions/anillo-auth/badge.svg)](https://pypi.python.org/pypi/anillo-auth/)
[![License](https://pypip.in/license/anillo-auth/badge.svg)](https://pypi.python.org/pypi/anillo-auth/)
[![Downloads](https://pypip.in/download/anillo-auth/badge.svg)](https://pypi.python.org/pypi/anillo-auth/)

Anillo auth is a middleware for authentication for the anillo nanoframework.

## Backends

Anillo auth comes with some backends for different types of authentication,
thats allow you to define your own authentication backend, or reuse one of the
anillo-auth shipped backends.

The currently working backends are:

  * HttpBasicAuthBackend: Based on the http basic auth headers.
  * SessionBackend: Based on the session identity key.
  * JWSBackend: Based on the Authentication header and using the Json Web Signature format.

## Usage

### Basic example

```python
from anillo.app import application
from anillo.handlers.routing import router, url
from anillo.middlewares.cookies import cookies_middleware
from anillo.middlewares.session import session_middleware, MemoryStorage
from anillo.http import Ok
from anillo.utils import chain

from anillo_auth.auth import auth_middleware
from anillo_auth.backends.session import SessionBackend

import json


def index(request):
    return Ok(json.dumps(request.get('session', {}).get('identity')))


def login(request):
    request.session['identity'] = {"user_id": 1}
    return Ok("logged-in")


urls = [
    url("/", index),
    url("/login", login),
]

app = application(chain(
    cookies_middleware,
    session_middleware(MemoryStorage()),
    auth_middleware(SessionBackend()),
    router(urls)
))

if __name__ == '__main__':
    from anillo import serving
    serving.run_simple(app, port=5000)
```
