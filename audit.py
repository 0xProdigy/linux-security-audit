import platform
from datetime import datetime
import os
import subprocess

# Crear carpeta de logs si no existe
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "audit-log.txt")

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
        return result.stdout
    except Exception as e:
        return f"Error al obtener información de memoria: {e}"


def get_disk_info():
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error al obtener uso de disco: {e}"


def get_network_info():
    try:
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error al obtener interfaces de red: {e}"


def log_system_info():
    with open(log_file, "a") as f:
        f.write("\n" + "=" * 40 + " AUDIT REPORT " + "=" * 40 + "\n")
        f.write(f"Date and Time: {datetime.now()}\n")
        f.write(f"System: {platform.system()} {platform.release()}\n")
        f.write(f"Processor: {platform.processor()}\n")

        f.write("\n[CPU]\n")
        f.write(get_cpu_usage() + "\n")

        f.write("\n[Memory]\n")
        f.write(get_memory_info() + "\n")

        f.write("\n[Disk]\n")
        f.write(get_disk_info() + "\n")

        f.write("\n[Network Interfaces]\n")
        f.write(get_network_info() + "\n")

        # Servicios activos con systemctl
        f.write("\n[Services - systemctl list-units]\n")
        try:
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--no-pager"],
                capture_output=True, text=True
            )
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Could not retrieve systemctl services: {e}\n")

        # Scripts en /etc/init.d
        f.write("\n[Services - /etc/init.d/]\n")
        try:
            scripts = os.listdir("/etc/init.d/")
            for script in scripts:
                f.write(f"/etc/init.d/{script}\n")
        except Exception as e:
            f.write(f"Could not list /etc/init.d/: {e}\n")

        # Crontab del sistema
        f.write("\n[Crontabs]\n")
        try:
            result = subprocess.run(["cat", "/etc/crontab"], capture_output=True, text=True)
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Could not read /etc/crontab: {e}\n")

        f.write("=" * 95 + "\n")


def log_listening_ports():
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n[Listening Ports]\n")
        try:
            result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, check=True)
            f.write(result.stdout)
        except subprocess.CalledProcessError as e:
            f.write(f"Error retrieving listening ports: {e}\n")

def log_users_and_groups():
    with open(log_file, "a") as f:
        f.write("\n[Users - /etc/passwd]\n")
        try:
            with open("/etc/passwd", "r") as passwd_file:
                for line in passwd_file:
                    f.write(line)
        except Exception as e:
            f.write(f"Could not read /etc/passwd: {e}\n")

        f.write("\n[Groups - /etc/group]\n")
        try:
            with open("/etc/group", "r") as group_file:
                for line in group_file:
                    f.write(line)
        except Exception as e:
            f.write(f"Could not read /etc/group: {e}\n")

        f.write("\n[Sudoers - /etc/sudoers and /etc/sudoers.d/]\n")

        # Intentar leer /etc/sudoers (puede fallar sin permisos)
        try:
            with open("/etc/sudoers", "r") as sudo_file:
                f.write("[/etc/sudoers]\n")
                for line in sudo_file:
                    f.write(line)
        except PermissionError:
            f.write("Could not read /etc/sudoers: Permission denied (requires sudo).\n")
        except Exception as e:
            f.write(f"Could not read /etc/sudoers: {e}\n")

        # Intentar listar archivos en /etc/sudoers.d/
        try:
            f.write("\n[/etc/sudoers.d/ files]\n")
            files = os.listdir("/etc/sudoers.d/")
            for file in files:
                f.write(f"/etc/sudoers.d/{file}\n")
        except FileNotFoundError:
            f.write("Directory /etc/sudoers.d/ not found.\n")
        except PermissionError:
            f.write("Permission denied when listing /etc/sudoers.d/ (requires sudo).\n")
        except Exception as e:
            f.write(f"Could not list /etc/sudoers.d/: {e}\n")

def log_suid_sgid_files():
    with open(log_file, "a") as f:
        f.write("\n[SUID/SGID Files]\n")
        try:
            result = subprocess.run(
                ["find", "/", "-type", "f", "(", "-perm", "-4000", "-o", "-perm", "-2000", ")", "-exec", "ls", "-l", "{}", ";"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            f.write(result.stdout)
        except Exception as e:
            f.write(f"Could not search for SUID/SGID files: {e}\n")


if __name__ == "__main__":
    log_system_info()
    log_listening_ports()
    log_users_and_groups()
    log_suid_sgid_files()
    print(f"Audit complete. Results saved to {log_file}")

