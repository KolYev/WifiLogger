from scapy.all import *

router_ip = conf.route.route("0.0.0.0")[2]
print(f"IP-адрес роутера: {router_ip}")