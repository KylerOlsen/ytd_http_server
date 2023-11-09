import socket

VERSION = 'uytd/0.0.0a'

def parse_headers(raw_headers):
    headers = raw_headers.split('\r\n')
    method, path, protocol = headers[0].split(' ')
    headers = {header.split(':')[0]: header.split(':')[1].strip() for header in headers[1:]}
    return method, path, protocol, headers

def send_headers(conn, code=200, **kwargs):
    conn.send(f'HTTP/1.0 {code}\r\n')
    conn.send(f'Server: {VERSION}\r\n')
    # conn.send(f'Date: {''}\r\n')
    for key, value in kwargs.items():
        conn.send(f'{key}: {value}')

def http_server(request_class):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print("HTTP listening...")

    while True:
        conn, addr = s.accept()
        print(f'Got a connection from {addr}')
        request = conn.recv(1024)
        raw_headers, body = request.split(b'\r\n\r\n', 1)
        method, path, protocol, headers = parse_headers(raw_headers.decode('utf-8'))
        print(f'HTTP {addr} {method} {path} {protocol} {headers}')
        response = "Hello World".encode()
        conn.send(response)
        conn.close()

def main():
    http_server(None)

if __name__ == "__main__":
    main()
