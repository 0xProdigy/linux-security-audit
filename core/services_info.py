import os
from core.utils import log_or_print
import subprocess

def log_services():
    log_or_print("\n[Services - systemctl list-units]")
    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--no-pager"],
            capture_output=True, text=True, timeout=5
        )
        log_or_print(result.stdout.strip())
    except Exception as e:
        log_or_print(f"Could not retrieve systemctl services: {e}")

    log_or_print("\n[Services - /etc/init.d/]")
    try:
        scripts = os.listdir("/etc/init.d/")
        for script in scripts:
            log_or_print(f"/etc/init.d/{script}")
    except Exception as e:
        log_or_print(f"Could not list /etc/init.d/: {e}")

    log_or_print("\n[Crontabs]")
    try:
        with open("/etc/crontab", "r") as crontab:
            log_or_print(crontab.read().strip())
    except Exception as e:
        log_or_print(f"Could not read /etc/crontab: {e}")
