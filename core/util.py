import socket
import requests


def get_numeric_ip(ip):
    if ip not in ["localhost", "127.0.0.1"]:
        return ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip


def get_normal_addr(master_url):
    if "localhost" in master_url:
        url = f'{master_url}/cluster/status'
        r = requests.get(url)
        master_url = f"http://{r.json()['Leader']}/"
    return master_url
