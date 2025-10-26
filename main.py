import http.server
import socketserver
import socket
import threading
import time
import os
import cgi

PORT = 8080
RECEIVE_TIMEOUT = 300  # 5 minuti
RECEIVED_DIR = "ShareMiiShot Received"
received_files = []

# crea cartella received se non esiste
if not os.path.exists(RECEIVED_DIR):
    os.makedirs(RECEIVED_DIR)

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
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],}
            )
            file_item = form['file']  # 'file' deve corrispondere al nome dell'input file in HTML
            if file_item.filename:
                filename = os.path.basename(file_item.filename)
            else:
                filename = f"image_{int(time.time())}.jpg"

            filepath = os.path.join(RECEIVED_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(file_item.file.read())

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
        return  # disabilita log HTTP standard

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
