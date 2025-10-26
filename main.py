#!/usr/bin/env python3
import http.server
import socketserver
import threading
import time
import socket
import os

PORT = 8080
RECEIVE_TIMEOUT = 300  # 5 minuti
SAVE_DIR = "ShareMiiShot Received"
os.makedirs(SAVE_DIR, exist_ok=True)

received_files = []

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
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Nessun dato ricevuto")
                return

            # usa X-Filename o nome automatico
            filename = self.headers.get("X-Filename", f"image_{int(time.time())}.jpg")
            filename = os.path.basename(filename)
            filepath = os.path.join(SAVE_DIR, filename)

            with open(filepath, 'wb') as f:
                f.write(self.rfile.read(length))

            received_files.append(filepath)
            print(f"IMMAGINE RICEVUTA: {filepath}")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK: file ricevuto")

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Errore ricezione")
            print("Errore ricezione:", e)

    def log_message(self, format, *args):
        return

def timeout_thread(httpd, timeout):
    time.sleep(timeout)
    print(f"\nTimeout di {timeout} secondi raggiunto. Chiusura server.")
    httpd.shutdown()

def main():
    local_ip = get_local_ip()
    handler = ImageHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"Server pronto! Invia le immagini a: http://{local_ip}:{PORT}\n")

    threading.Thread(target=timeout_thread, args=(httpd, RECEIVE_TIMEOUT), daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nChiusura manuale server.")
    finally:
        httpd.server_close()

    print("Files ricevuti correttamente:")
    for f in received_files:
        print(f" - {f}")

if __name__ == "__main__":
    main()
