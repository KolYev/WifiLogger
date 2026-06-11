import folium
import http.server
import socketserver
import webbrowser
import os
from wifi_scanning import *

# проверка на локальный IP
def is_local_ip(ip):
    if not ip:
        return True
    
    return (ip.startswith("192.168.") or 
            ip.startswith("10.") or 
            ip.startswith("172.16.") or
            ip.startswith("127.") or 
            ip.startswith("169.254.") or
            ip.startswith("224.") or
            ip == "0.0.0.0")

location_data = get_ip_location()

if location_data:
    coordinate_lat, coordinate_lon = location_data
    print("Ваши координаты успешно определены.")
else:
    print("Предупреждение: Не удалось получить ваши координаты. Используются дефолтные.")
    coordinate_lat, coordinate_lon = 55.7558, 37.6173 

location = [coordinate_lat, coordinate_lon]
world_map = folium.Map(location=location, zoom_start=12)

folium.Marker(
    location = location,
    popup = "You",
).add_to(world_map)

# for i in range(0, len(packet_data)):
#     location = get_ip_location
#     folium.Marker(
#         location=
#     )

world_map.save("world_map.html")

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath('world_map.html')))

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}/world_map.html')
    print(f'http://localhost:{PORT}/world_map.html')
    httpd.serve_forever()
