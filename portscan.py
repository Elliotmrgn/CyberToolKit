# todo: add input validation
# todo: add default option for top 100 ports
import socket
from typing import Set, Optional
from dataclasses import dataclass

@dataclass
class ScanResult:
    port: int
    is_open: bool

class PortScan:
    def __init__(self):
        self.target_ip: Optional[str] = None
        self.target_ports: Set[int] = set()

    def get_target_ip(self) -> bool:
        # Gets IP to scan
        target = input("Enter target IP or domain name to scan: ")
        try:
            self.target_ip = socket.gethostbyname(target)
            return True
        except socket.gaierror as e:
            print(f"Error resolving hostname '{target}': {e}")
            return False

    def get_target_ports(self) -> None:
        # Gets range of ports to scan
        user_defined_ports = input(
            "Enter target ports to scan (separate numbers and ranges by comma): "
        ).split(",")
        for port in user_defined_ports:
            port = port.strip()
            if "-" in port:
                start, end = map(int, port.split("-"))
                self.target_ports.update(range(start, end + 1))
            else:
                self.target_ports.add(int(port))

        # Attempts to connect to each targeted port on target IP, outputs result
    def scan_port(self, port: int) -> ScanResult:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.1)  # Set timeout for socket connection
            result = sock.connect_ex((self.target_ip, port))# 0 = no error connecting (port is open)
            return ScanResult(port=port, is_open=(result == 0))

    def scan(self) -> None:
        if not self.target_ip:
            print("No target IP set. Please run get_target_ip() first.")
            return

        results = [self.scan_port(port) for port in self.target_ports]
        self.print_results(results)

    @staticmethod
    def print_results(results: list[ScanResult]) -> None:
        for result in results:
            status = "open" if result.is_open else "closed"
            print(f"Port {result.port} is {status}")

    def run(self) -> None:
        if self.get_target_ip():
            self.get_target_ports()
            self.scan()
