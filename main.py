import http.server
import socketserver
import socket
import threading
import time
import os
import signal
import sys

PORT = 8080
RECEIVE_TIMEOUT = 300  # 5 minuti
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
            content_type = self.headers.get('Content-Type', '')
            boundary = content_type.split('boundary=')[-1].encode()
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)

            parts = data.split(b'--' + boundary)
            for part in parts:
                if b'Content-Disposition' in part and b'filename=' in part:
                    header, file_data = part.split(b'\r\n\r\n', 1)
                    file_data = file_data.rstrip(b'\r\n--')
                    
                    fname_line = [l for l in header.split(b'\r\n') if b'filename=' in l][0]
                    filename = fname_line.split(b'filename=')[-1].strip(b'" ')
                    filename = filename.decode(errors='ignore')
                    
                    if not filename:
                        filename = f"image_{int(time.time())}.jpg"

                    os.makedirs("received", exist_ok=True)
                    filepath = os.path.join("received", filename)

                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    
                    received_files.append(filepath)
                    print(f"IMMAGINE RICEVUTA: {filepath}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK: file ricevuto')

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Errore durante ricezione')
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

    # chiusura server al segnale di terminazione
    def signal_handler(sig, frame):
        print("\nTerminale chiuso o interrotto. Chiusura server.")
        httpd.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    threading.Thread(target=timeout_thread, args=(httpd, RECEIVE_TIMEOUT), daemon=True).start()

    try:
        httpd.serve_forever()
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
