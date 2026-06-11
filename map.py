import folium
import http.server
import socketserver
import webbrowser
import os
import time
from wifi_scanning import *

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
    my_lat, my_lon = location_data
else:
    my_lat, my_lon = 55.7558, 37.6173 

my_location = [my_lat, my_lon]
world_map = folium.Map(location=my_location, zoom_start=4)

folium.Marker(
    location=my_location,
    popup="Вы",
    icon=folium.Icon(color="blue", icon="home")
).add_to(world_map)

coord_cache = {}

def get_cached_location(ip):
    if is_local_ip(ip):
        return [my_lat, my_lon]
        
    if ip in coord_cache:
        return coord_cache[ip]
    
    result = get_ip_location(ip)
    time.sleep(1.4) 
    coord_cache[ip] = result
    return result

placed_markers = set()

for packet in packet_data:
    if packet.get("type") != "IP":
        continue

    sender_ip = packet.get("sender_ip")
    recipient_ip = packet.get("recipient_ip")

    sender_coords = get_cached_location(sender_ip)
    recipient_coords = get_cached_location(recipient_ip)

    if sender_coords and recipient_coords:
        if sender_coords == recipient_coords:
            continue

        if sender_ip not in placed_markers and not is_local_ip(sender_ip):
            folium.Marker(
                location=sender_coords,
                popup=f"Отправитель: {sender_ip}",
                icon=folium.Icon(color="red", icon="cloud")
            ).add_to(world_map)
            placed_markers.add(sender_ip)

        if recipient_ip not in placed_markers and not is_local_ip(recipient_ip):
            folium.Marker(
                location=recipient_coords,
                popup=f"Получатель: {recipient_ip}",
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(world_map)
            placed_markers.add(recipient_ip)

        folium.PolyLine(
            locations=[sender_coords, recipient_coords],
            color="orange",
            weight=2,
            opacity=0.6,
            tooltip=f"{sender_ip} → {recipient_ip}"
        ).add_to(world_map)

world_map.save("world_map.html")

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath('world_map.html')))

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}/world_map.html')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")