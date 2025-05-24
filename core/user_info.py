import os
from core.utils import log_or_print

def log_users_and_groups():
    log_or_print("\n[Users - /etc/passwd]")
    try:
        with open("/etc/passwd", "r") as passwd_file:
            for line in passwd_file:
                log_or_print(line.strip())
    except Exception as e:
        log_or_print(f"Could not read /etc/passwd: {e}")

    log_or_print("\n[Groups - /etc/group]")
    try:
        with open("/etc/group", "r") as group_file:
            for line in group_file:
                log_or_print(line.strip())
    except Exception as e:
        log_or_print(f"Could not read /etc/group: {e}")

    log_or_print("\n[Sudoers - /etc/sudoers and /etc/sudoers.d/]")
    try:
        with open("/etc/sudoers", "r") as sudo_file:
            log_or_print("[/etc/sudoers]")
            for line in sudo_file:
                log_or_print(line.strip())
    except PermissionError:
        log_or_print("Could not read /etc/sudoers: Permission denied (requires sudo).")
    except Exception as e:
        log_or_print(f"Could not read /etc/sudoers: {e}")

    try:
        log_or_print("\n[/etc/sudoers.d/ files]")
        files = os.listdir("/etc/sudoers.d/")
        for file in files:
            log_or_print(f"/etc/sudoers.d/{file}")
    except FileNotFoundError:
        log_or_print("Directory /etc/sudoers.d/ not found.")
    except PermissionError:
        log_or_print("Permission denied when listing /etc/sudoers.d/ (requires sudo).")
    except Exception as e:
        log_or_print(f"Could not list /etc/sudoers.d/: {e}")

def log_suid_sgid_files():
    log_or_print("\n[SUID/SGID Files]")
    try:
        suid_sgid_files = []
        for root, dirs, files in os.walk("/"):
            for file in files:
                try:
                    filepath = os.path.join(root, file)
                    st = os.lstat(filepath)
                    if st.st_mode & 0o4000 or st.st_mode & 0o2000:
                        suid_sgid_files.append(f"{filepath} - {oct(st.st_mode)}")
                except Exception:
                    continue
            if len(suid_sgid_files) > 1000:
                break
        if suid_sgid_files:
            for f in suid_sgid_files:
                log_or_print(f)
        else:
            log_or_print("No se encontraron archivos SUID/SGID.")
    except Exception as e:
        log_or_print(f"Error buscando archivos SUID/SGID: {e}")
