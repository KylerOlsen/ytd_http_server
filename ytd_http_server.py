# Kyler Olsen Nov 2023
# Simple HTTP server

# MIT License

# Copyright (c) 2023 Kyler Olsen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

try:
    import usocket as socket
except:
    import socket

VERSION = 'uytd/0.0.0a'


class HTTPERROR(Exception): pass


class HTTP_Request_Handler:

    _conn: socket.socket
    _addr: str

    _status: int | str
    _response_headers: dict[str, str]
    _method: str
    _path: str
    _protocol: str
    _headers: dict[str, str]

    def __init__(self, conn: socket.socket, addr: str):
        self._conn = conn
        self._addr = addr
        self._status = "200 OK"
        self._response_headers = {}
        (
            self._method,
            self._path,
            self._protocol,
            self._headers,
        ) = self._parse_headers()

    @property
    def addr(self) -> str: return self._addr
    @property
    def status(self) -> int | str: return self._status
    @property
    def method(self) -> str: return self._method
    @property
    def path(self) -> str: return self._path
    @property
    def protocol(self) -> str: return self._protocol

    def DO(self):
        if self.method == "HEAD": self.DO_HEAD()
        elif self.method == "GET": self.DO_GET()
        elif self.method == "PUT": self.DO_PUT()
        elif self.method == "POST": self.DO_POST()
        elif self.method == "DELETE": self.DO_DELETE()
        else: self.DO_UNKNOWN()

        if isinstance(self.status, str): status = self.status.split(' ')[0]
        else: status = self.status
        print(f"INFO []: {self.method} {status} {self.addr}")

    def DO_HEAD(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def DO_GET(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def DO_PUT(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def DO_POST(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def DO_DELETE(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def DO_UNKNOWN(self):
        self.set_status("501 Not Implemented")
        self.send_headers()

    def has_header(self, key: str) -> bool:
        return key in self._headers

    def get_header(self, key: str) -> str:
        return self._headers[key]

    def set_status(self, status: int | str):
        self._status = status

    def set_header(self, key: str, value: str):
        if key.lower() in ["server", "date"]:
            raise ValueError(f"Header key '{key}' cannot be changed.")
        self._response_headers[key] = value

    def get_set_header(self, key: str) -> str:
        return self._response_headers[key]

    def send_headers(self):
        self._conn.send(f'HTTP/1.1 {self._status}\r\n'.encode('utf-8'))
        self._conn.send(f'Server: {VERSION}\r\n'.encode('utf-8'))
        # conn.send(f'Date: {''}\r\n')
        for key, value in self._response_headers.items():
            self._conn.send(f'{key}: {value}\r\n'.encode('utf-8'))
        self._conn.send(b'\r\n\r\n')

    def send_body(self, data: bytes):
        self._conn.send(data)

    def _parse_headers(self) -> tuple[str, str, str, dict[str, str]]:
        try:
            raw_headers = self._read_headers()
            headers = raw_headers.split('\r\n')
            method, path, protocol = headers[0].split(' ')
            headers = {
                header.split(':')[0]:
                header.split(':')[1].strip()
                for header in headers[1:-2]
            }
            return method, path, protocol, headers
        except:
            self.set_status("400 Bad Request")
            self.send_headers()
            raise HTTPERROR("Invalid Request Format")

    def _read_headers(self) -> str:
        i = 0
        raw_headers = bytearray()
        while raw_headers[-4:] != b'\r\n\r\n':
            raw_headers += self._conn.recv(1)
            i += 1
            if i > 1024:
                self.set_status("431 Request Header Fields Too Large")
                self.send_headers()
                raise HTTPERROR("Request Header Too Large (> 1024 bytes).")
        return raw_headers.decode('utf-8')

class HTTP_Server:

    _request_handler: type[HTTP_Request_Handler]
    _address: str
    _port: int
    sock: socket.socket

    def __init__(
        self,
        request_handler: type[HTTP_Request_Handler] = HTTP_Request_Handler,
        address: str = '',
        port: int = 80,
    ):
        self._request_handler = request_handler
        self._address = address
        self._port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self._address, self._port))

    def serve_forever(self):
        self.sock.listen(5)
        print("HTTP listening...")

        while True:
            conn, addr = self.sock.accept()
            print(f"Connection from {addr[0]}")
            try: request_handler = self._request_handler(conn, addr[0])
            except HTTPERROR: pass
            except Exception:
                conn.send(b'HTTP/1 500 Internal Server Error\r\n\r\n')
                print(f"Error []: Unknown 500 {addr[0]}")
            else:
                try: request_handler.DO()
                except HTTPERROR: pass
                except Exception:
                    request_handler.set_status("500 Internal Server Error")
                    request_handler.send_headers()
                    print(f"Error []: {request_handler.method} 500 {addr[0]}")
            finally: conn.close()
