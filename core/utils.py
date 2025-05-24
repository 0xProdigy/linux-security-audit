import time
import threading

SAVE_LOG = False
LOG_FILE = "/dev/shm/audit-log.txt"
spinner_running = False

def spinner():
    global spinner_running
    spinner_running = True
    while spinner_running:
        for cursor in '|/-\\':
            print(f'\r{cursor} Recolectando información...', end='', flush=True)
            time.sleep(0.1)
    print('\r', end='', flush=True)

def start_spinner():
    t = threading.Thread(target=spinner)
    t.start()
    return t

def stop_spinner(t):
    global spinner_running
    spinner_running = False
    t.join()

def log_or_print(text):
    from core.system_info import SAVE_LOG, LOG_FILE
    if SAVE_LOG:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)

def print_help():
    help_text = """
Audit Tool - Linux Basic Post-Exploitation Info Collector

Uso:
  python3 audit.py -save    Guardar log en disco (en /dev/shm/). ⚠ Deja artefactos.
  python3 audit.py -nosave  Solo salida por consola, no deja artefactos.

Ejemplo:
  python3 audit.py -save

Sin parámetros esta ayuda será mostrada.

La herramienta recolecta info sobre CPU, memoria, disco, red, servicios,
usuarios, sudoers y archivos SUID/SGID con un enfoque sigiloso.
"""
    print(help_text)
