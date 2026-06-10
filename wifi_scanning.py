from scapy.all import *
import requests

INTERFACE = "wlo1"

# локальный IP адрес
router_ip = conf.route.route("0.0.0.0")[2]
print(f"IP-адрес роутера: {router_ip}")

# внешний IP адрес
def get_ip_location():
    try:
        url = "http://ip-api.com/json/"
        response = requests.get(url)
        data = response.json()

        if data.get('status') == 'success':
            ip = data.get('query')
            country = data.get('country')
            region = data.get('regionName')
            city = data.get('city')
            coordinate_lat = data.get('lat')
            coordinate_lon = data.get('lon')
            
            print(f"Внешний IP: {ip}")
            print(f"Страна: {country}")
            print(f"Регион: {region}")
            print(f"Город: {city}")
            print(f"Координаты: {coordinate_lat}, {coordinate_lon}")
            return coordinate_lat, coordinate_lon
        else:
            print(f"Ошибка сервиса: {data.get('message', 'Неизвестный сбой')}")
        
    except Exception as e:
        print(f"Ошибка подключения: {e}")

def packet_callback(packet):
    print(f"Пакет получен: {packet.summary()}")

sniff(iface=INTERFACE, prn=packet_callback, store=0)