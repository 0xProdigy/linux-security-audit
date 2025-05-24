import os
import platform
import grp
from core.utils import log_or_print

def check_kernel_version():
    log_or_print("\n[Kernel Version]")
    kernel = platform.uname().release
    log_or_print(f"Kernel: {kernel}")

def check_user_privileges():
    """
    Evalúa si el usuario actual pertenece a grupos privilegiados como sudo, wheel, adm, etc.
    No accede a /etc/sudoers para ser sigiloso.
    """
    log_or_print("\n[Privilege Groups Check]")

    try:
        user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]
        suspicious = {"sudo", "wheel", "adm", "admin"}

        found = suspicious.intersection(user_groups)
        if found:
            log_or_print(f"[!] El usuario pertenece a grupos privilegiados: {', '.join(found)}")
        else:
            log_or_print("✔ El usuario no pertenece a grupos privilegiados conocidos.")
    except Exception as e:
        log_or_print(f"[!] Error al obtener grupos del usuario: {e}")

def check_world_writable_dirs():
    """
    Busca directorios world-writable en rutas comunes como /tmp, /var/tmp, /dev/shm, /home.
    """
    log_or_print("\n[World-Writable Directories]")

    paths = ["/tmp", "/var/tmp", "/dev/shm", "/home"]
    try:
        for path in paths:
            for root, dirs, _ in os.walk(path):
                for d in dirs:
                    full_path = os.path.join(root, d)
                    try:
                        if os.stat(full_path).st_mode & 0o002:
                            log_or_print(f"[!] {full_path} es world-writable")
                    except Exception:
                        continue
    except Exception as e:
        log_or_print(f"Error durante el chequeo de permisos world-writable: {e}")
