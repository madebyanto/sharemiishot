import http.server
import socketserver
import socket
import os
import time
from urllib.parse import parse_qs

PORT = 8080
RECEIVE_DIR = "ShareMiiShot_Received"
os.makedirs(RECEIVE_DIR, exist_ok=True)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length)
        filename = f"image_{int(time.time())}.jpg"
        filepath = os.path.join(RECEIVE_DIR, filename)
        try:
            with open(filepath, 'wb') as f:
                f.write(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK: file ricevuta')
            print(f"IMAGE RECEIVED: {filename}")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Error during reception')
            print("Receiving Error:", e)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ShareMiiShot server ready to receive images via POST.")

    def log_message(self, format, *args):
        return  # disabilita log HTTP standard

if __name__ == "__main__":
    ip = get_local_ip()
    with socketserver.TCPServer(("", PORT), ImageHandler) as httpd:
        print(f"Server ready! Send images to http://{ip}:{PORT}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutdown.")
