import http.server
import socketserver
import socket
import threading
import time
import os

PORT = 8081
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
            # trova boundary multipart
            content_type = self.headers.get('Content-Type', '')
            boundary = content_type.split('boundary=')[-1].encode()
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)

            # estrai il file dal multipart manualmente
            parts = data.split(b'--' + boundary)
            for part in parts:
                if b'Content-Disposition' in part and b'filename=' in part:
                    # estrai filename
                    header, file_data = part.split(b'\r\n\r\n', 1)
                    file_data = file_data.rstrip(b'\r\n--')
                    fname_line = [l for l in header.split(b'\r\n') if b'filename=' in l][0]
                  filename = fname_line.split(b'filename=')[-1].strip(b'" ')
filename = filename.decode(errors='ignore')
if not filename:  # se vuoto
    filename = f"image_{int(time.time())}.jpg"  # nome automatico unico
                    with open(filename, 'wb') as f:
                        f.write(file_data)
                    received_files.append(filename)
                    print(f"IMMAGINE RICEVUTA: {filename}")

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
