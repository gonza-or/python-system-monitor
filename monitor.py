#!/usr/bin/env python3
"""Resumen de recursos del equipo local."""

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
        interfaces[name] = [address.address for address in addresses
                            if address.family in (socket.AF_INET, socket.AF_INET6)]
    alerts = []
    for label, value in (("CPU", cpu), ("RAM", memory.percent), ("Disco", disk.percent)):
        if value >= 90:
            alerts.append(f"{label}: uso alto ({value}%)")
    return {
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
        "status": "Atención" if alerts else "Sin umbrales superados",
        "alerts": alerts,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", default=str(Path.home().anchor), help="Ruta del volumen a consultar")
    parser.add_argument("--json", action="store_true", help="Salida JSON")
    args = parser.parse_args()
    try:
        report = collect_report(args.path)
    except (OSError, psutil.Error) as error:
        parser.exit(1, f"No se pudo consultar el sistema: {error}\n")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print(f"Equipo: {report['hostname']}\nSistema: {report['os']}")
    print(f"CPU: {report['cpu_model']} | {report['cpu_logical_count']} lógicos | {report['cpu_percent']}%")
    print(f"RAM: {report['ram_percent']}% de {report['ram_total_gib']} GiB")
    print(f"Disco ({report['disk_path']}): {report['disk_percent']}% de {report['disk_total_gib']} GiB")
    print(f"Encendido: {report['uptime']}\nEstado: {report['status']}")
    for name, addresses in report['interfaces'].items():
        print(f"Red {name}: {', '.join(addresses) or 'Sin IP'}")
    for alert in report['alerts']:
        print(f"Aviso: {alert}")


if __name__ == "__main__":
    main()
