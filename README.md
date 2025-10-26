<img src="sharemiishot.png" alt="ShareMiiShot Logo">

# ShareMiiShot

**ShareMiiShot** is a web service for **Wii U** and **3DS** that allows you to share images between consoles and other devices like phones or PCs.

---

# How It Works

It’s super simple!  

1. Download the project zip, extract it, and run the Python code (`server.py`) using an IDE (e.g., **VSCode**) or directly from the Linux terminal.  
2. Agree to start the local server on port `8080`. For security reasons, the server will automatically shut down after 5 minutes.  
3. On your **Wii U** or **3DS**, open the [ShareMiiShot website](http://sharemiishot.aurastudioitalia.it) and select the image you want to send.  
4. Click **"Send to Wi-Fi Server"** and wait a few seconds.  
5. The image will be transferred and appear in the Python code, where you can download it.  
6. Done! Your image has been successfully transferred.

---

# Notes

- Transfer speed depends on your connection, but the service works well even on slower connections (1 Mbps is enough).  
- The **Wii U/3DS browser** is a bit outdated, so minor issues may occur after web app updates.  
- If the file is received successfully but the browser shows **"Network error"**, you can safely ignore it: the file is still intact.

---

# Credits

ShareMiiShot is a web app developed solely by me (Anto) in HTML/CSS (for the web interface), Python (for FTP), and JavaScript (for the flow and logic). Creating this web app was incredibly complicated as I had to use "ancient" JS logic, so you should know that I put a lot of effort and care into it. If you'd like to donate to support my work, here's the Ko-Fi: https://ko-fi.com/madebyanto
