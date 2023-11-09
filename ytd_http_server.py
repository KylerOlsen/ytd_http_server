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

import socket

VERSION = 'uytd/0.0.0a'


class HTTP_Request_Handler:

    _conn: socket.socket
    _addr: str

    _status: int
    _response_headers: dict[str, str]
    _method: str
    _path: str
    _protocol: str
    _headers: dict[str, str]

    def __init__(self, conn: socket.socket, addr: str):
        self._conn = conn
        self._addr = addr

        self._status = 200
        self._response_headers = {}
        (
            self._method,
            self._path,
            self._protocol,
            self._headers,
        ) = self._parse_headers()

    def DO(self):
        pass

    def DO_GET(self):
        pass

    def DO_PUT(self):
        pass

    def DO_POST(self):
        pass

    def DO_DELETE(self):
        pass

    def set_header(self, key: str, value: str):
        if key.lower() in ["server", "date"]:
            raise ValueError(f"Header Key cannot be '{key}'")
        self._response_headers[key] = value

    def send_headers(self):
        self._conn.send(f'HTTP/1.0 {self._status}\r\n'.encode('utf-8'))
        self._conn.send(f'Server: {VERSION}\r\n'.encode('utf-8'))
        # conn.send(f'Date: {''}\r\n')
        for key, value in self._response_headers.items():
            self._conn.send(f'{key}: {value}'.encode('utf-8'))

    def _parse_headers(self) -> tuple[str, str, str, dict[str, str]]:
        raw_headers = self._read_headers()
        headers = raw_headers.split('\r\n')
        method, path, protocol = headers[0].split(' ')
        headers = {
            header.split(':')[0]:
            header.split(':')[1].strip()
            for header in headers[1:]
        }
        return method, path, protocol, headers

    def _read_headers(self) -> str:
        i = 0
        raw_headers = bytearray()
        while raw_headers[-4:] != b'\r\n\r\n':
            raw_headers += self._conn.recv(1)
            i += 1
            if i > 1024:
                raise BufferError("Request Header Too Large (> 1024 bytes)")
        return raw_headers.decode('utf-8')

class HTTP_Server:

    _request_handler: type[HTTP_Request_Handler]
    _address: str
    _port: int

    def __init__(
        self,
        request_handler: type[HTTP_Request_Handler] = HTTP_Request_Handler,
        address: str = '',
        port: int = 80,
    ):
        self._request_handler = request_handler
        self._address = address
        self._port = port

    def serve_forever(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        print("HTTP listening...")

        while True:
            conn, addr = s.accept()
            try:
                request_handler = self._request_handler(conn, addr)
                request_handler.DO()
            except:
                pass
            conn.close()
