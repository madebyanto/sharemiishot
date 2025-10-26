#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShareMiiShot Wi-Fi Receiver (Python)
Riceve immagini dal Wii U sulla rete locale.
Il server si chiude automaticamente dopo 5 minuti per sicurezza.
"""

import http.server
import socketserver
import threading
import os
import sys
from urllib.parse import parse_qs
from io import BytesIO
import time

PORT = 8080
TIMEOUT = 5 * 60  # 5 minuti
received_images = []

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            content_type = self.headers.get('Content-Type', '')

            if 'multipart/form-data' not in content_type:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Errore: richiesta non multipart/form-data')
                return

            boundary = content_type.split('boundary=')[-1].encode()
            body = self.rfile.read(content_length)

            # cerca il file nel body
            parts = body.split(b'--' + boundary)
            for part in parts:
                if b'Content-Disposition' in part and b'name="file"' in part:
                    # estrai il filename
                    headers, file_data = part.split(b'\r\n\r\n', 1)
                    file_data = file_data.rstrip(b'\r\n--')
                    # estrai il nome file
                    disposition = [line for line in headers.split(b'\r\n') if b'Content-Disposition' in line][0]
                    filename = disposition.split(b'filename="')[-1].split(b'"')[0].decode('utf-8', 'ignore')
                    received_images.append((filename, file_data))
                    print(f"\nIMMAGINE RICEVUTA: {filename}")
                    answer = input("Vuoi scaricarla? Sì/No [Y/N]: ").strip().lower()
                    if answer in ('y', 's', 'yes', 'si'):
                        with open(filename, 'wb') as f:
                            f.write(file_data)
                        print(f"Immagine salvata come {filename}")
                    else:
                        print("Immagine scartata")
                    break

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Errore interno: ' + str(e).encode())

    def log_message(self, format, *args):
        return  # disabilita log standard

def run_server():
    with socketserver.TCPServer(("", PORT), UploadHandler) as httpd:
        httpd.timeout = 1
        print(f"Server pronto a ricevere immagini sulla rete locale all'indirizzo: http://{get_local_ip()}:{PORT}")
        start_time = time.time()
        try:
            while True:
                httpd.handle_request()
                if time.time() - start_time > TIMEOUT:
                    print("\nTempo massimo trascorso, server chiuso per sicurezza.")
                    break
        except KeyboardInterrupt:
            print("\nServer interrotto manualmente.")

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connessione fittizia per determinare IP locale
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    start = input("Vuoi aprire un server per ricevere immagini dal Wii U? Sì/No [Y/N]: ").strip().lower()
    if start in ('y', 's', 'yes', 'si'):
        run_server()
    else:
        print("Server non avviato.")
