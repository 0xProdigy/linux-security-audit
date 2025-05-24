import os
import subprocess
from core.utils import log_or_print

def log_environment_variables():
    """Logea todas las variables de entorno actuales."""
    log_or_print("\n[Environment Variables]")
    for key, value in os.environ.items():
        log_or_print(f"{key}={value}")

def log_shell_aliases():
    """
    Logea los alias configurados en el shell del usuario.
    Asume que el shell es bash o zsh.
    """
    log_or_print("\n[Shell Aliases]")

    shell = os.environ.get("SHELL", "")
    try:
        if "bash" in shell or "zsh" in shell:
            # Ejecuta 'alias' en el shell para capturar alias
            result = subprocess.run(
                [shell, "-ic", "alias"], capture_output=True, text=True, timeout=3
            )
            output = result.stdout.strip()
            if output:
                log_or_print(output)
            else:
                log_or_print("No se encontraron alias.")
        else:
            log_or_print(f"Shell {shell} no soportado para búsqueda de alias.")
    except Exception as e:
        log_or_print(f"Error obteniendo alias: {e}")

def log_user_shells():
    """
    Lista todos los shells disponibles en /etc/shells
    """
    log_or_print("\n[Available Shells (/etc/shells)]")
    try:
        with open("/etc/shells", "r") as f:
            shells = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        for sh in shells:
            log_or_print(sh)
    except Exception as e:
        log_or_print(f"Error leyendo /etc/shells: {e}")
