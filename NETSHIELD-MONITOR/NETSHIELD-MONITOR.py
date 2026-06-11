import subprocess
import time
import logging
import os
import re
from datetime import datetime
from statistics import mean
from twilio.rest import Client
import ipaddress

# =========================
# CONFIGURACION
# =========================

TARGETS = [
    "192.0.2.123",
    "google.com",
    "cloudflare.com"
]

CHECK_INTERVAL = 300  # 5 min

from config import *

client = Client(TWILIO_SID, TWILIO_AUTH)

# =========================
# ESTADO GLOBAL
# =========================

HOST_STATS = {
    host: {
        "ok": 0,
        "fail": 0,
        "latencies": []
    } for host in TARGETS
}

# =========================
# INICIO
# =========================

logging.basicConfig(
    filename="monitor_logs.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# FUNCIONES
# =========================

def send_whatsapp(message: str):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_FROM,
            to=TWILIO_WHATSAPP_TO
        )
        logging.info(f"WhatsApp enviado: {message[:80]}")
    except Exception as e:
        logging.error(f"Fallo envío WhatsApp: {e}")


def ping_host(host: str):
    try:
        param = "-n" if os.name == "nt" else "-c"

        result = subprocess.run(
            ["ping", param, "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout

        if result.returncode == 0:
            match = re.search(r"time[=<]([\d\.]+)", output)
            latency = float(match.group(1)) if match else 0
            return True, latency

        return False, None

    except Exception as e:
        logging.error(f"Ping error {host}: {e}")
        return False, None


def nslookup_host(host: str) -> str:
    try:
        result = subprocess.run(
            ["nslookup", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        return (result.stdout + result.stderr).strip()

    except subprocess.TimeoutExpired:
        return "nslookup timeout (DNS lento o caído)"
    except Exception as e:
        return f"Error nslookup: {e}"


def analyze_failure(ns_result: str) -> str:
    try:
        text = ns_result.lower()

        if "can't find" in text or "non-existent" in text:
            return "FALLO DNS"
        elif "timeout" in text:
            return "POSIBLE DNS O RED"
        else:
            return "SERVIDOR NO RESPONDE"

    except:
        return "ERROR ANALISIS"


def write_log(host: str, status: str, ns_result: str):
    try:
        logging.error(f"""
HOST: {host}
STATUS: {status}
TIME: {datetime.now()}
DETAIL:
{ns_result}
--------------------
""")
    except Exception as e:
        logging.error(f"Error log: {e}")


def alert(host: str, reason: str, ns_result: str):
    try:
        message = f"""
🚨 ALERTA DE RED 🚨

Host: {host}
Problema: {reason}

Diagnóstico:
{ns_result[:800]}
"""
        send_whatsapp(message)
    except Exception as e:
        logging.error(f"Error alert: {e}")


def check_host(host: str):
    try:
        ok, latency = ping_host(host)

        # Detectar si es IP
        is_ip = False
        try:
            ipaddress.ip_address(host)
            is_ip = True
        except:
            is_ip = False

        if ok:
            HOST_STATS[host]["ok"] += 1
            HOST_STATS[host]["latencies"].append(latency or 0)

            logging.info(f"OK: {host} | {latency}ms")
            print(f"[OK] {host} - {latency}ms")
            return

        # FALLA
        HOST_STATS[host]["fail"] += 1

        # 🔥 LÓGICA CORRECTA
        if is_ip:
            reason = "SERVIDOR O RED NO RESPONDE"
            ns_result = "No aplica nslookup (es IP)"
        else:
            ns_result = nslookup_host(host)
            reason = analyze_failure(ns_result)

        write_log(host, reason, ns_result)
        alert(host, reason, ns_result)

        print(f"[FAIL] {host} -> {reason}")

    except Exception as e:
        logging.error(f"check_host error {host}: {e}")


def print_dashboard():
    os.system("cls" if os.name == "nt" else "clear")

    print("🔥 NETSHIELD MONITOR - DASHBOARD PRO 🔥")
    print("=" * 60)

    for host, data in HOST_STATS.items():

        total = data["ok"] + data["fail"]
        uptime = (data["ok"] / total * 100) if total > 0 else 100

        avg_latency = mean(data["latencies"]) if data["latencies"] else 0

        if uptime > 95:
            status = "🟢 OK"
        elif uptime > 80:
            status = "🟡 WARNING"
        else:
            status = "🔴 CRITICAL"

        print(f"{status} {host}")
        print(f"   Uptime: {uptime:.2f}%")
        print(f"   Latencia: {avg_latency:.2f} ms")
        print("-" * 60)


def monitor():
    logging.info("=== INICIO MONITOREO PRO ===")

    while True:
        try:
            for host in TARGETS:
                check_host(host)

            print_dashboard()
            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            logging.info("Monitoreo detenido")
            break

        except Exception as e:
            logging.error(f"Loop error: {e}")
            time.sleep(5)


if __name__ == "__main__":
    print("Iniciando sistema de monitoreo...")
    monitor()