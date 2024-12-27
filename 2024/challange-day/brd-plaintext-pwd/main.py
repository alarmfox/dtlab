import argparse
import json
import base64

from socket import *
from netifaces import interfaces, ifaddresses, AF_INET

parser = argparse.ArgumentParser(
    prog='Client',
    description='DTLab program')

parser.add_argument("-p", "--password", required=True, type=str)

packet = {
    "protocol": "sus",
    "encoding": "base64"
}

def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        try:
            for link in ifaddresses(interface)[AF_INET]:
                ip_list.append(link['broadcast'])
        except KeyError:
            print("skipping", interface)
    return ip_list

def broadcast(address: str, password: str) -> None:
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
   
    packet["secret"] = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    data = json.dumps(packet) 
    cs.sendto(data.encode("utf-8"), (address, 54545))

    cs.close()

def run(password: str) -> None:
    ips = ip4_addresses()

    for ip in ips:
        print("broadcasting on", ip)
        broadcast(ip, password)


if __name__ == "__main__":
    args = parser.parse_args()
    run(args.password)
