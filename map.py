import folium
import http.server
import socketserver
import webbrowser
import os
from wifi_scanning import get_ip_location


coordinate_lat, coordinate_lon = get_ip_location()
location = [coordinate_lat, coordinate_lon]

world_map = folium.Map(location=[coordinate_lat, coordinate_lon], zoom_start=12)
folium.Marker(
    location = location,
    popup = "Location",
).add_to(world_map)
world_map.save("world_map.html")

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath('world_map.html')))

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}/world_map.html')
    httpd.serve_forever()
