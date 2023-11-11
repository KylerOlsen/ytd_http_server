# YTD HTTP Server
*Kyler Olsen*

A simple HTTP server intended to work in micropython on a Raspberry Pi Pico W.
Loosely inspired by `http.server` from the Python standard library.

## Documentation

*Also see `windows_test.py` and `pico_test.py`*

First Import the `HTTP_Server` and `HTTP_Request_Handler` classes.

```python
from ytd_http_server import HTTP_Server, HTTP_Request_Handler
```

The `HTTP_Server` class listens for requests and instantiates a Request Handler
class to handle the request.

The `HTTP_Request_Handler` class reads and parses the request, and calls a
member function to handle the request.

The member function called is determined by the http request method.

| Method | Member Function | Short Method Description |
| --- | --- | --- |
| `HEAD` | `DO_HEAD` | Same as `GET` but without response body |
| `GET` | `DO_GET` | Retrieve the resource at the given URI |
| `PUT` | `DO_PUT` | Put data at the given URI |
| `POST` | `DO_POST` | Put data at the given URI |
| `DELETE` | `DO_DELETE` | Delete the resource at the given URI |

Any other method will result in `DO_UNKNOWN` being called.
All of the functions just take the `self` parameter.

The difference between `PUT` and `POST` is that multiple identical `PUT`
requests will have no affect following the first request, where as multiple
identical `POST` requests will change something on the server with
every request.

By default in the `HTTP_Request_Handler` class, each of these methods will
return a `501 Not Implemented` error. If we want to handle one of these
methods, we need to overwrite the associated function by subclassing
`HTTP_Request_Handler`.

Here is an example `HTTP_Request_Handler` subclass that serves **all** files on
the filesystem. *__WARNING:__ Be careful doing it this way as it exposes all
files on the filesystem to anyone with access to the http server.*

```python
class Custom_Request_Handler(HTTP_Request_Handler):

    def DO_GET(self):
        try:
            path = self.path
            if path[-1] == '/': path += 'index.html'
            with open(path[1:], 'rb') as file:
                self.set_status(200)
                data = file.read()
                self.set_header("Content-Length", str(len(data)))
                self.send_headers()
                self.send_body(data)
        except OSError:
            self.set_status(404)
            self.send_headers()
```

`HTTP_Request_Handler.set_status` sets the status code for the response.
Examples: `self.set_status(200)`, `self.set_status('404 Not Found')`

`HTTP_Request_Handler.set_header` sets a header in the response.
Examples: `self.set_header("Content-Length", str(len(data)))`,
`self.set_header("Content-Type", "text/html")`

`HTTP_Request_Handler.send_headers` sends the response headers to the client.
This includes the response code and all given headers.
Example: `self.send_headers()`

`HTTP_Request_Handler.send_body` sends the body of the response. Not all
responses need a body. The object given must be of type `bytes` (Other types
may work but are not guaranteed).
Examples: `self.send_body(data)`,
`self.send_body("Hello World".encode('utf-8'))`

Finally create an `HTTP_Server` object, passing in your Response Handler class.
Then calling `HTTP_Server.serve_forever` will start the server, it will begin
accepting requests, blocking code execution.

```python
def main():
    server = HTTP_Server(Custom_Request_Handler)
    server.serve_forever()
```
