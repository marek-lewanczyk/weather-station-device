# device_web_config.py

import network
import socket
import ujson
import machine
from config import config

def load_html():
    try:
        with open("config_ui.html", "r") as f:
            html = f.read()

        html = html.replace("{{ssid}}", config.get("WIFI_SSID", ""))
        html = html.replace("{{password}}", config.get("WIFI_PASSWORD", ""))

        return html
    except:
        return "<h1>UI load error</h1>"

def save_config(data):
    try:
        with open("config.json", "w") as f:
            ujson.dump(data, f)
        return True
    except:
        return False

def start_config_server():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="WeatherStation-Setup")

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Setup portal running at http://192.168.4.1")

    while True:
        cl, addr = s.accept()
        request = cl.recv(1024).decode()

        if "POST /save" in request:
            post_data = request.split("\r\n\r\n")[1]
            fields = {kv.split("=")[0]: kv.split("=")[1] for kv in post_data.split("&")}
            ssid = fields.get("ssid", "").replace("+", " ").strip()
            password = fields.get("password", "").replace("+", " ").strip()

            config_data = {
                "WIFI_SSID": ssid,
                "WIFI_PASSWORD": password
            }

            if save_config(config_data):
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
                response += "<h3>Config saved. Rebooting...</h3>"
                cl.send(response)
                cl.close()
                machine.reset()
            else:
                cl.send("HTTP/1.1 500 Internal Server Error\r\n\r\nFailed to save config.")
        else:
            html = load_html()
            cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            cl.send(html)
            cl.close()