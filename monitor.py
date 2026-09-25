#!/usr/bin/env python3
import argparse
import json
import platform
import socket
import time
from datetime import timedelta
from pathlib import Path

import psutil


def collect_report(path):
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(path)
    interfaces = {}
    for name, addresses in psutil.net_if_addrs().items():
        interfaces[name] = []
        for address in addresses:
            if address.family in (socket.AF_INET, socket.AF_INET6):
                interfaces[name].append(address.address)
    alerts = []
    if cpu >= 90:
        alerts.append("CPU: uso alto ({}%)".format(cpu))
    if memory.percent >= 90:
        alerts.append("RAM: uso alto ({}%)".format(memory.percent))
    if disk.percent >= 90:
        alerts.append("Disco: uso alto ({}%)".format(disk.percent))
    report = {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "cpu_model": platform.processor() or "No informado por el sistema",
        "cpu_logical_count": psutil.cpu_count(),
        "cpu_percent": cpu,
        "ram_total_gib": round(memory.total / 1024**3, 2),
        "ram_percent": memory.percent,
        "disk_path": str(Path(path).resolve()),
        "disk_total_gib": round(disk.total / 1024**3, 2),
        "disk_percent": disk.percent,
        "uptime": str(timedelta(seconds=int(time.time() - psutil.boot_time()))),
        "interfaces": interfaces,
        "status": "Sin umbrales superados",
        "alerts": alerts,
    }
    if alerts:
        report["status"] = "Atención"
    return report


def main():
    parser = argparse.ArgumentParser(description="Muestra información del equipo")
    parser.add_argument("--path", default=str(Path.home().anchor), help="Ruta del volumen a consultar")
    parser.add_argument("--json", action="store_true", help="Muestra JSON")
    args = parser.parse_args()
    try:
        report = collect_report(args.path)
    except (OSError, psutil.Error) as error:
        parser.exit(1, "Error: {}\n".format(error))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("Equipo: {}\nSistema: {}".format(report["hostname"], report["os"]))
    print("CPU: {} | {} lógicos | {}%".format(report["cpu_model"], report["cpu_logical_count"], report["cpu_percent"]))
    print("RAM: {}% de {} GiB".format(report["ram_percent"], report["ram_total_gib"]))
    print("Disco ({}): {}% de {} GiB".format(report["disk_path"], report["disk_percent"], report["disk_total_gib"]))
    print("Encendido: {}\nEstado: {}".format(report["uptime"], report["status"]))
    for name, addresses in report['interfaces'].items():
        if addresses:
            value = ", ".join(addresses)
        else:
            value = "Sin IP"
        print("Red {}: {}".format(name, value))
    for alert in report['alerts']:
        print("Aviso: {}".format(alert))


if __name__ == "__main__":
    main()
