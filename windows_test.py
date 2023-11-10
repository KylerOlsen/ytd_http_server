# Kyler Olsen Nov 2023
# Example and Test Code

from ytd_http_server import HTTP_Server, HTTP_Request_Handler

class Custom_Request_Handler(HTTP_Request_Handler):

    def DO_GET(self):
        try:
            path = self.path
            if path[-1] == '/': path += 'index.html'
            # This is a very insecure way to do this
            with open(path[1:], 'rb') as file:
                self.set_status(200)
                data = file.read()
                self.set_header("Content-Length", str(len(data)))
                self.send_headers()
                self.send_body(data)
        except OSError:
            self.set_status(404)
            self.send_headers()


def main():
    server = HTTP_Server(Custom_Request_Handler, port=8001)
    # If you want to add ssl, you can add it here to server.sock
    server.serve_forever()

if __name__ == '__main__':
    main()
