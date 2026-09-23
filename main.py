import network
import socket
import time
import json
# =========================================================
# ESP32 Access Point Settings
# =========================================================
AP_SSID = "ESP32_Health"
AP_PASSWORD = "12345678"
# =========================================================
# Start ESP32 as Wi-Fi Access Point
# =========================================================
def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(
        essid=AP_SSID,
        password=AP_PASSWORD
    )
    while not ap.active():
        pass
    print("ESP32 Access Point Started")
    print("SSID:", AP_SSID)
    print("Password:", AP_PASSWORD)
    print("IP Address:", ap.ifconfig()[0])
    return ap
# =========================================================
# Heart Rate and SpO2 Reading
# =========================================================
# Replace these values with your actual MAX30102 readings.
# This section is simulated for now.
def read_sensor():
    heart_rate = 78
    spo2 = 97
    return heart_rate, spo2
# =========================================================
# Web Page
# =========================================================
html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32 Health Monitor</title>
<style>
body {
    font-family: Arial;
    text-align: center;
    background-color: #f2f2f2;
    margin-top: 40px;
}
.container {
    width: 320px;
    margin: auto;
    background: white;
    padding: 25px;
    border-radius: 15px;
}
h2 {
    margin-bottom: 30px;
}
.label {
    font-size: 20px;
}
.value {
    font-size: 45px;
    font-weight: bold;
}
</style>
</head>
<body>
<div class="container">
<h2>ESP32 Health Monitor</h2>
<p class="label">Heart Rate</p>
<p class="value">
<span id="heart">--</span> BPM
</p>
<p class="label">Blood Oxygen</p>
<p class="value">
<span id="spo2">--</span> %
</p>
</div>
<script>
function updateValues() {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        document.getElementById("heart").innerHTML =
        data.heart_rate;
        document.getElementById("spo2").innerHTML =
        data.spo2;
    })
    .catch(error => {
        console.log(error);
    });
}
setInterval(updateValues, 1000);
updateValues();
</script>
</body>
</html>
"""
# =========================================================
# Web Server
# =========================================================
def start_web_server():
    address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    server = socket.socket()
    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    server.bind(address)
    server.listen(5)
    print("Web server started")
    print("Open http://192.168.4.1")
    while True:
        client, addr = server.accept()
        request = client.recv(1024)
        request = request.decode()
        # ---------------------------------------------
        # Sensor data request
        # ---------------------------------------------
        if "GET /data " in request:
            heart_rate, spo2 = read_sensor()
            data = {
                "heart_rate": heart_rate,
                "spo2": spo2
            }
            response = json.dumps(data)
            client.send(
                "HTTP/1.1 200 OK\r\n"
            )
            client.send(
                "Content-Type: application/json\r\n"
            )
            client.send(
                "Connection: close\r\n\r\n"
            )
            client.send(response)
        # ---------------------------------------------
        # Main web page
        # ---------------------------------------------
        else:
            client.send(
                "HTTP/1.1 200 OK\r\n"
            )
            client.send(
                "Content-Type: text/html\r\n"
            )
            client.send(
                "Connection: close\r\n\r\n"
            )
            client.send(html)
        client.close()
# =========================================================
# Main Program
# =========================================================
start_access_point()
start_web_server()
