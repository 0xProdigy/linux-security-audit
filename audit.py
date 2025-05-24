import platform
from datetime import datetime
import os
import subprocess
import socket
import fcntl
import struct
import array
import sys
import time

# Variables globales
SAVE_LOG = False
LOG_FILE = "/dev/shm/audit-log.txt"

# Spinner para procesos lentos
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
    import threading
    t = threading.Thread(target=spinner)
    t.start()
    return t

def stop_spinner(t):
    global spinner_running
    spinner_running = False
    t.join()

def log_or_print(text):
    if SAVE_LOG:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)

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

# ----------------------------------------------
# Funciones para interfaces de red (estilo ifconfig)
# ----------------------------------------------

def get_interfaces():
    max_possible = 128
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        struct.pack('iL', bytes, names.buffer_info()[0])
    ))[0]
    namestr = names.tobytes()
    interfaces = []
    for i in range(0, outbytes, 40):
        name = namestr[i:i+16].split(b'\0', 1)[0]
        interfaces.append(name.decode('utf-8'))
    return interfaces

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip = fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[20:24]
        return socket.inet_ntoa(ip)
    except OSError:
        return "No IP"

def get_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        info = fcntl.ioctl(
            s.fileno(),
            0x8927,  # SIOCGIFHWADDR
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )
        return ':'.join('%02x' % b for b in info[18:24])
    except OSError:
        return "No MAC"

def get_mtu(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        mtu = struct.unpack('H', fcntl.ioctl(
            s.fileno(),
            0x8921,  # SIOCGIFMTU
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[16:18])[0]
        return mtu
    except OSError:
        return "No MTU"

def get_flags(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        flags = struct.unpack('H', fcntl.ioctl(
            s.fileno(),
            0x8913,  # SIOCGIFFLAGS
            struct.pack('256s', ifname[:15].encode('utf-8'))
        )[16:18])[0]
        return flags
    except OSError:
        return 0

def if_flags_to_str(flags):
    flags_str = []
    if flags & 0x1:
        flags_str.append("UP")
    if flags & 0x2:
        flags_str.append("BROADCAST")
    if flags & 0x8:
        flags_str.append("LOOPBACK")
    if flags & 0x10:
        flags_str.append("POINTOPOINT")
    if flags & 0x1000:
        flags_str.append("MULTICAST")
    return " ".join(flags_str)

def get_network_info():
    interfaces = get_interfaces()
    output = []
    for ifname in interfaces:
        ip = get_ip_address(ifname)
        mac = get_mac_address(ifname)
        mtu = get_mtu(ifname)
        flags = get_flags(ifname)
        flags_str = if_flags_to_str(flags)
        output.append(f"{ifname}: flags={flags_str}  mtu {mtu}")
        output.append(f"    inet {ip}")
        output.append(f"    ether {mac}\n")
    return "\n".join(output).strip()

# ----------------------------------------------
# Otras funciones de recolección
# ----------------------------------------------

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

    # Servicios activos con systemctl
    log_or_print("\n[Services - systemctl list-units]")
    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--no-pager"],
            capture_output=True, text=True, timeout=5
        )
        log_or_print(result.stdout.strip())
    except Exception as e:
        log_or_print(f"Could not retrieve systemctl services: {e}")

    # Scripts en /etc/init.d
    log_or_print("\n[Services - /etc/init.d/]")
    try:
        scripts = os.listdir("/etc/init.d/")
        for script in scripts:
            log_or_print(f"/etc/init.d/{script}")
    except Exception as e:
        log_or_print(f"Could not list /etc/init.d/: {e}")

    # Crontab del sistema
    log_or_print("\n[Crontabs]")
    try:
        with open("/etc/crontab", "r") as crontab:
            log_or_print(crontab.read().strip())
    except Exception as e:
        log_or_print(f"Could not read /etc/crontab: {e}")

    log_or_print("=" * 95)

def log_listening_ports():
    log_or_print("\n[Listening Ports]")
    try:
        # En lugar de 'ss' o 'netstat', leemos /proc/net/tcp y /proc/net/udp
        tcp_ports = parse_proc_net("/proc/net/tcp")
        udp_ports = parse_proc_net("/proc/net/udp")
        for port_info in tcp_ports + udp_ports:
            log_or_print(port_info)
    except Exception as e:
        log_or_print(f"Error retrieving listening ports: {e}")

def parse_proc_net(path):
    # Lectura simple de puertos listening desde /proc/net/tcp o udp
    results = []
    try:
        with open(path, "r") as f:
            next(f)  # saltar encabezado
            for line in f:
                parts = line.strip().split()
                local_address = parts[1]
                state = parts[3]
                # state 0A = LISTEN en tcp
                if state == "0A":
                    ip_hex, port_hex = local_address.split(":")
                    ip = socket.inet_ntoa(bytes.fromhex(ip_hex)[::-1])
                    port = int(port_hex, 16)
                    results.append(f"{path.split('/')[-1]} LISTEN: {ip}:{port}")
    except Exception:
        pass
    return results

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
    # Usamos lectura de /proc para no usar find
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
            # Para no tardar mucho, limitar el recorrido
            if len(suid_sgid_files) > 1000:
                break
        if suid_sgid_files:
            for f in suid_sgid_files:
                log_or_print(f)
        else:
            log_or_print("No se encontraron archivos SUID/SGID.")
    except Exception as e:
        log_or_print(f"Error buscando archivos SUID/SGID: {e}")

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
usuarios, sudoers y archivos SUID/SGID con un enfoque minimalista y sigiloso.
"""
    print(help_text)

def main():
    global SAVE_LOG

    if len(sys.argv) != 2:
        print_help()
        return

    arg = sys.argv[1].lower()

    if arg == "-save":
        SAVE_LOG = True
        print(f"⚠ Modo guardado habilitado. Se creará un archivo de log en {LOG_FILE}")
        print("⚠ Esto deja artefactos que pueden ser detectados en análisis post-mortem.\n")
    elif arg == "-nosave":
        SAVE_LOG = False
    else:
        print_help()
        return

    if SAVE_LOG:
        # Crear o limpiar archivo log
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(f"Audit Log iniciado {datetime.now()}\n\n")
        except Exception as e:
            print(f"No se pudo crear el archivo log: {e}")
            return

    spinner_thread = start_spinner()

    try:
        log_system_info()
        log_listening_ports()
        log_users_and_groups()
        log_suid_sgid_files()
    finally:
        stop_spinner(spinner_thread)

    log_or_print("\n✅ Recolección completada.")

    if SAVE_LOG:
        print(f"\n✅ Log de auditoría guardado en: {LOG_FILE}")
    else:
        print("\n✅ Recolección finalizada. Sin archivos guardados.")

if __name__ == "__main__":
    main()
