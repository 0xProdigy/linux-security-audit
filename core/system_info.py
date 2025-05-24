import platform
from datetime import datetime
import subprocess
import sys

from core.utils import (
    log_or_print,
    start_spinner,
    stop_spinner,
    print_help,
    SAVE_LOG,
    LOG_FILE,
)

from core.network_info import get_network_info, log_listening_ports
from core.user_info import log_users_and_groups, log_suid_sgid_files
from core.services_info import log_services

from core.environment_info import (
    log_environment_variables,
    log_shell_aliases,
    log_user_shells,
)

from core.vuln_checks import (
    check_kernel_version,
    check_user_privileges,
    check_world_writable_dirs,
)


def get_cpu_usage():
    try:
        result = subprocess.run(["top", "-bn1"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Cpu(s):" in line:
                return line.strip()
        return "No se pudo obtener uso de CPU"
    except Exception as e:
        return f"Error al obtener uso de CPU: {e}"


def get_memory_info():
    try:
        result = subprocess.run(["free", "-h"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error al obtener información de memoria: {e}"


def get_disk_info():
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error al obtener uso de disco: {e}"


def log_system_info():
    log_or_print("\n" + "=" * 40 + " AUDIT REPORT " + "=" * 40)
    log_or_print(f"Date and Time: {datetime.now()}")
    log_or_print(f"System: {platform.system()} {platform.release()}")
    log_or_print(f"Processor: {platform.processor()}")

    log_or_print("\n[CPU]")
    log_or_print(get_cpu_usage())

    log_or_print("\n[Memory]")
    log_or_print(get_memory_info())

    log_or_print("\n[Disk]")
    log_or_print(get_disk_info())

    log_or_print("\n[Network Interfaces]")
    log_or_print(get_network_info())


def main():
    if len(sys.argv) != 2:
        print_help()
        return

    arg = sys.argv[1].lower()

    from core import utils

    if arg == "-save":
        utils.SAVE_LOG = True
        utils.LOG_FILE = "/dev/shm/audit-log.txt"
        print(f"⚠ Modo guardado habilitado. Se creará un archivo de log en {LOG_FILE}")
        print("⚠ Esto deja artefactos que pueden ser detectados en análisis post-mortem.\n")
    elif arg == "-nosave":
        utils.SAVE_LOG = False
    else:
        print_help()
        return

    if utils.SAVE_LOG:
        try:
            with open(utils.LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"Audit Log iniciado {datetime.now()}\n\n")
        except Exception as e:
            print(f"No se pudo crear el archivo log: {e}")
            return

    spinner_thread = start_spinner()

    try:
        log_system_info()
        log_listening_ports()
        log_users_and_groups()
        # log_suid_sgid_files()  # Si necesitas incluirlo, descomenta

        log_services()

        log_environment_variables()
        log_shell_aliases()
        log_user_shells()

        check_kernel_version()
        check_user_privileges()
        check_world_writable_dirs()

    finally:
        stop_spinner(spinner_thread)

    log_or_print("\n✅ Recolección completada.")

    if utils.SAVE_LOG:
        print(f"\n✅ Log de auditoría guardado en: {utils.LOG_FILE}")
    else:
        print("\n✅ Recolección finalizada. Sin archivos guardados.")
