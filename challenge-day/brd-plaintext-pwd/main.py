import argparse
import json
import base64
import time
import socket as sk


parser = argparse.ArgumentParser(prog="Client", description="DTLab program")

parser.add_argument("--password", required=True, type=str)
parser.add_argument("-p", "--port", required=True, type=int)
parser.add_argument("--ip", required=True, action="append")

packet = {"protocol": "sus", "encoding": "base64"}


def send_packet(address: str, port: int, password: str) -> None:
    cs = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    cs.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    cs.setsockopt(sk.SOL_SOCKET, sk.SO_BROADCAST, 1)

    packet["secret"] = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    data = json.dumps(packet)
    cs.sendto(data.encode("utf-8"), (address, port))

    cs.close()


def run(ips: list, port: int, password: str) -> None:
    while True:
        for ip in ips:
            print(f"sending packet on {ip}:{port}")
            send_packet(ip, port, password)
        time.sleep(5)


if __name__ == "__main__":
    args = parser.parse_args()
    run(args.ip, args.port, args.password)
