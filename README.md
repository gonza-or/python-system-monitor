# Python System Monitor

Resumen del equipo local para una primera revisión de recursos. Usa Python 3.10+ y `psutil` en Linux y Windows.

## Instalación

Desde esta carpeta, crear y activar un entorno virtual e instalar la dependencia:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows usar `py -m venv .venv` y `.venv\Scripts\Activate.ps1`.

## Uso y ejemplos

```bash
python monitor.py
python monitor.py --path . --json
python monitor.py --help
```

Muestra hostname, sistema operativo, identificación de CPU si está disponible, núcleos lógicos, uso de CPU/RAM, capacidad y ocupación del volumen seleccionado, uptime e IP por interfaz. La muestra de CPU dura medio segundo. `--path` consulta el volumen que contiene esa ruta; no suma todos los discos.

Marca «Atención» cuando CPU, RAM o disco alcanzan el 90%. Es un umbral orientativo: una muestra aislada no diagnostica una falla ni garantiza la salud del hardware. La ruta inexistente produce un mensaje y salida 1; la consulta exitosa devuelve 0, incluso si hay alertas.

## Qué demuestra

Consulta de métricas del sistema, unidades GiB, interfaces IPv4/IPv6, argumentos de consola, manejo de errores y salida estructurada JSON. El código separa la recolección de la presentación para poder probar ambas partes.
