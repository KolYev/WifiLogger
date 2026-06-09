import folium
import http.server
import socketserver
import webbrowser
import os

world_map = folium.Map()
world_map.save("world_map.html")

PORT = 8000
os.chdir(os.path.dirname(os.path.abspath('world_map.html')))

with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    webbrowser.open(f'http://localhost:{PORT}/world_map.html')
    httpd.serve_forever()
    