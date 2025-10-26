#!/usr/bin/env python3
import cgi
import os
import time

UPLOAD_DIR = "../ShareMiiShot_Received"  # relativo al cgi-bin

print("Content-Type: text/html\n")

form = cgi.FieldStorage()
fileitem = form['file'] if 'file' in form else None

if fileitem and fileitem.filename:
    filename = os.path.basename(fileitem.filename)
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(fileitem.file.read())
    print(f"<h2>IMMAGINE RICEVUTA: {filename}</h2>")
    print(f"<p>Salvata in: {filepath}</p>")
else:
    print("<h2>Nessun file ricevuto o file vuoto!</h2>")

print('<p><a href="../index.html">Torna al form</a></p>')
