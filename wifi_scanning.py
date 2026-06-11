from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
import requests

INTERFACE = "wlo1"

# локальный IP адрес
router_ip = conf.route.route("0.0.0.0")[2]
print(f"IP-адрес роутера: {router_ip}")

# внешний IP адрес
def get_ip_location(ip_address=None):
    try:
        url = "http://ip-api.com/json" 
        if ip_address:
            url += ip_address
        
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
            return None

    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

packet_data = []

def packet_callback(packet):
    packet_info = {}

    if IP in packet and Ether in packet:
        packet_info = {
            "type": "IP",
            "sender_ip": packet[IP].src, # ip отправителя
            "sender_mac": packet[Ether].src, # MAC-адрес отправителя
            "recipient_ip" :  packet[IP].dst, # ip получателя
            "recipient_mac" : packet[Ether].dst # MAC-адрес получателя
        }
        
        print(f"{packet_info['sender_ip']} -> {packet_info['recipient_ip']} | {packet_info['sender_mac']} -> {packet_info['recipient_mac']}")
    
    elif Ether in packet:
        packet_info = {
            "type": "Ethernet",
            "sender_mac" : packet[Ether].src,
            "recipient_mac" : packet[Ether].dst
        }
        
        print(f"{packet_info['sender_mac']} -> {packet_info['recipient_mac']}")
    else:
        packet_info = {
            "type": "Other",
            "summary": packet.summary()
        }
        print(f"Другое: {packet_info['summary']}")

    packet_data.append(packet_info)


sniff(iface=INTERFACE, prn=packet_callback, store=0, count=100)

print(f"Сохранено пакетов: {len(packet_data)}")