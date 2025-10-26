import http.server
import socketserver
import socket
import threading
import os

PORT = 8080
RECEIVE_TIMEOUT = 300  # 5 minuti
UPLOAD_DIR = "ShareMiiShot_Received"

# crea cartella upload se non esiste
os.makedirs(UPLOAD_DIR, exist_ok=True)

# trova IP locale
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

# abilita CGI
Handler = http.server.CGIHTTPRequestHandler
Handler.cgi_directories = ["/cgi-bin"]

httpd = socketserver.TCPServer(("", PORT), Handler)
local_ip = get_local_ip()
print(f"Server pronto! Apri nel browser Wii U: http://{local_ip}:{PORT}/index.html")

# thread per timeout
def stop_server():
    threading.Timer(RECEIVE_TIMEOUT, lambda: httpd.shutdown()).start()

stop_server()

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer chiuso manualmente.")
finally:
    httpd.server_close()
