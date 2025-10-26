import http.server
import socketserver
import socket
import threading
import time
import os

PORT = 8080
RECEIVE_TIMEOUT = 300  # 5 minuti

received_files = []

# funzione per ottenere IP locale della Wi-Fi
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

# handler HTTP per ricevere POST con immagine
class ImageHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers['Content-Length'])
            filename = self.headers.get('X-Filename', 'unnamed.jpg')
            data = self.rfile.read(length)
            with open(filename, 'wb') as f:
                f.write(data)
            received_files.append(filename)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK: file ricevuto')
            print(f"IMMAGINE RICEVUTA: {filename}")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Errore durante ricezione')
            print("Errore ricezione:", e)

    def log_message(self, format, *args):
        return  # disabilita log HTTP standard

# thread per chiudere server dopo timeout
def timeout_thread(httpd, timeout):
    time.sleep(timeout)
    print(f"\nTimeout di {timeout} secondi raggiunto. Chiusura server.")
    httpd.shutdown()

def main():
    local_ip = get_local_ip()
    handler = ImageHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(f"Server pronto! Invia le immagini a: http://{local_ip}:{PORT}\n")
    
    # avvia timeout
    threading.Thread(target=timeout_thread, args=(httpd, RECEIVE_TIMEOUT), daemon=True).start()

    # serve fino a shutdown
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nChiusura manuale server.")
    finally:
        httpd.server_close()

    # gestione download immagini ricevute
    for f in received_files:
        choice = input(f"Vuoi scaricare {f}? [Y/N]: ").strip().upper()
        if choice == 'Y':
            print(f"Immagine salvata: {os.path.abspath(f)}")
        else:
            print(f"Immagine ignorata: {f}")

if __name__ == "__main__":
    main()
