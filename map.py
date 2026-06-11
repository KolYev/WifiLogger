import folium
import http.server
import socketserver
import webbrowser
import os
from wifi_scanning import *


coordinate_lat, coordinate_lon = get_ip_location()
location = [coordinate_lat, coordinate_lon]

world_map = folium.Map(location=[coordinate_lat, coordinate_lon], zoom_start=12)
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
    httpd.serve_forever()
