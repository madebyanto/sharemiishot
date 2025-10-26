#!/usr/bin/env python3
import http.server
import socketserver
import cgi
import os
import threading
import time
import socket

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

class ImageHandler(http.server.CGIHTTPRequestHandler):
    def do_POST(self):
        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],}
            )
            if "file" in form:
                fileitem = form["file"]
                filename = fileitem.filename or f"image_{int(time.time())}.jpg"
                filename = os.path.basename(filename)
                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(fileitem.file.read())
                received_files.append(filepath)
                print(f"IMMAGINE RICEVUTA: {filepath}")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK: file ricevuto')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Errore: nessun file ricevuto')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Errore durante ricezione')
            print("Errore ricezione:", e)

    def log_message(self, format, *args):
        return  # disabilita log standard

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

    for f in received_files:
        choice = input(f"Vuoi scaricare {f}? [Y/N]: ").strip().upper()
        if choice == 'Y':
            print(f"Immagine salvata: {os.path.abspath(f)}")
        else:
            print(f"Immagine ignorata: {f}")

if __name__ == "__main__":
    main()
