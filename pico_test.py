# Kyler Olsen Nov 2023
# Example and Test Code

from ytd_http_server import HTTP_Server, HTTP_Request_Handler
import network
import time
import my_secrets

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


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(my_secrets.ssid, my_secrets.password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print(wlan.ifconfig())
    return wlan

def access_point():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=my_secrets.ap_ssid, password=my_secrets.ap_password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    host_ip = ap.ifconfig()[0]
    print(f'IP Address To Connect to: {host_ip}')
    return ap

def main():
    # ap = access_point()
    wlan = connect()
    server = HTTP_Server(Custom_Request_Handler)
    server.serve_forever()

if __name__ == '__main__':
    main()

