import socket
import fcntl
import struct
import array

from core.utils import log_or_print

def get_interfaces():
    max_possible = 128
    bytes = max_possible * 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B', b'\0' * bytes)
    outbytes = struct.unpack('iL', fcntl.ioctl(
        s.fileno(),
        0x8912,
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
            0x8915,
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
            0x8927,
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
            0x8921,
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
            0x8913,
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

def parse_proc_net(path):
    results = []
    try:
        with open(path, "r") as f:
            next(f)
            for line in f:
                parts = line.strip().split()
                local_address = parts[1]
                state = parts[3]
                if state == "0A":
                    ip_hex, port_hex = local_address.split(":")
                    ip = socket.inet_ntoa(bytes.fromhex(ip_hex)[::-1])
                    port = int(port_hex, 16)
                    results.append(f"{path.split('/')[-1]} LISTEN: {ip}:{port}")
    except Exception:
        pass
    return results

def log_listening_ports():
    log_or_print("\n[Listening Ports]")
    try:
        tcp_ports = parse_proc_net("/proc/net/tcp")
        udp_ports = parse_proc_net("/proc/net/udp")
        for port_info in tcp_ports + udp_ports:
            log_or_print(port_info)
    except Exception as e:
        log_or_print(f"Error retrieving listening ports: {e}")
