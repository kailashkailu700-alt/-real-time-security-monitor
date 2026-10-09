"""
External Device Security Monitoring Agent
"""
import socket
import platform
import time
import psutil
import requests


# ---------- CONFIG ----------
BACKEND_URL = "http://127.0.0.1:8000"
DEVICE_ID = "demo-laptop-001"
INTERVAL = 15
# ----------------------------


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def register_device():
    payload = {
        "device_id": DEVICE_ID,
        "hostname": socket.gethostname(),
        "ip_address": get_local_ip(),
        "operating_system": f"{platform.system()} {platform.release()}",
    }
    try:
        r = requests.post(f"{BACKEND_URL}/api/devices/register", json=payload, timeout=5)
        print(f"[+] Device registered: {r.status_code}")
        return True
    except Exception as e:
        print(f"[!] Registration failed: {e}")
        return False


def get_network_connections():
    try:
        conns = psutil.net_connections(kind="inet")
        return len(conns)
    except Exception:
        return 0


def get_listening_ports():
    try:
        conns = psutil.net_connections(kind="inet")
        ports = [c.laddr.port for c in conns if c.status == "LISTEN"]
        return list(set(ports))
    except Exception:
        return []


def send_event(event_type, severity, description, port=None, source_ip=None):
    payload = {
        "device_id": DEVICE_ID,
        "event_type": event_type,
        "source_ip": source_ip,
        "destination_ip": get_local_ip(),
        "port": port,
        "description": description,
        "severity": severity,
    }
    try:
        r = requests.post(f"{BACKEND_URL}/api/events", json=payload, timeout=5)
        print(f"[->] Event sent: {event_type} ({r.status_code})")
    except Exception as e:
        print(f"[!] Event send failed: {e}")


def heartbeat():
    register_device()


def scan_and_report():
    conns = get_network_connections()
    ports = get_listening_ports()

    print(f"[*] Active connections: {conns} | Listening ports: {ports}")

    if conns > 100:
        send_event("high_traffic", "MEDIUM",
                   f"High number of network connections: {conns}")

    suspicious = [p for p in ports if p in {21, 23, 445, 1433, 3306, 3389, 5900}]
    for p in suspicious:
        send_event("suspicious_port", "HIGH",
                   f"Suspicious listening port detected: {p}", port=p)


def main():
    print("=" * 50)
    print(f"  Security Agent started - Device: {DEVICE_ID}")
    print(f"  Backend: {BACKEND_URL}")
    print("=" * 50)

    register_device()

    counter = 0
    while True:
        try:
            heartbeat()
            counter += 1
            if counter % 4 == 0:
                scan_and_report()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\n[!] Agent stopped.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(INTERVAL)


if __name__ == "__main__":
    main()