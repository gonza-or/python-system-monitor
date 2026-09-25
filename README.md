# Python System Monitor

Script de Python para consultar el estado básico del equipo.

Muestra hostname, sistema operativo, CPU, RAM, disco, tiempo encendido e interfaces de red. Con `--json` devuelve la misma información en JSON.

## Requisitos

- Python 3.10 o superior
- `psutil`

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Uso

```bash
python monitor.py
python monitor.py --path .
python monitor.py --path . --json
```

`--path` se usa para consultar el disco que contiene esa ruta. CPU, RAM y disco generan un aviso cuando llegan al 90%. Es una lectura puntual, no un diagnóstico de hardware.
