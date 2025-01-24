import paramiko
import socket
from ipaddress import ip_network

# Variables
NETWORK_RANGE = "192.168.1.0/24"
TIMEOUT = 1


def SCAN_IP_RANGE(NETWORK_RANGE, TIMEOUT=1):
    ssh_hosts = []
    print(f"Scanning network range: {NETWORK_RANGE} for open port 22...\n")
    for ip in ip_network(NETWORK_RANGE).hosts():
        ip = str(ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        try:
            sock.connect((ip, 22))
            print(f"[+] Port 22 open on {ip}")
            ssh_hosts.append(ip)

            # Optional: Attempt SSH connection
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, port=22, username='test', password='test', timeout=TIMEOUT)
                print(f"[+] SSH connection successful on {ip} (test credentials)")
                ssh.close()
            except paramiko.AuthenticationException:
                print(f"[!] SSH authentication failed on {ip}")
            except paramiko.SSHException as e:
                print(f"[!] SSH error on {ip}: {e}")

        except (socket.timeout, ConnectionRefusedError):
            print(f"[-] Port 22 closed on {ip}")
        finally:
            sock.close()

    print("\nScan complete.")
    print("Open SSH hosts:", ssh_hosts)
    return ssh_hosts

if __name__ == "__main__":
    SCAN_IP_RANGE(NETWORK_RANGE, TIMEOUT)
