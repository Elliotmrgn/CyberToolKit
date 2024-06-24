from scapy.all import *
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import argparse

@dataclass
class WifiNetwork:
    ssid: str  # Network name
    bssid: str  # MAC address of the access point
    channel: int  # Wi-Fi channel
    signal_strength: int  # Signal strength in dBm
    security: List[str] = field(default_factory=list)  # Security protocols (e.g., WEP, WPA, WPA2)

class WifiScan:
    def __init__(self):
        self.interface: str = ""  # Network interface to use for scanning
        self.timeout: int = 60  # Scan duration in seconds
        self.networks: Dict[str, WifiNetwork] = {}  # Dictionary to store discovered networks

    def scan(self) -> None:
        print(f"Scanning for Wi-Fi networks on {self.interface}...")
        # Note: This assumes the interface is already in monitor mode
        # Use scapy's sniff function to capture packets
        sniff(iface=self.interface, prn=self._packet_handler, timeout=self.timeout)
    def _packet_handler(self, pkt: Packet) -> None:
        if pkt.haslayer(Dot11Beacon):
            # Extract basic information
            bssid = pkt[Dot11].addr2
            ssid = pkt[Dot11Elt].info.decode(errors="ignore")
            
            # Extract channel
            try:
                channel = int(ord(pkt[Dot11Elt:3].info))
            except:
                channel = 0
            
            # Extract signal strength
            try:
                signal_strength = -(256-ord(pkt.notdecoded[-4:-3]))
            except:
                signal_strength = -100  # Default value if we can't extract signal strength
            
            # Determine security protocols
            security = []
            cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}")
            if 'privacy' in cap:
                security.append("WEP")
            if pkt.haslayer(Dot11EltRSN):
                security.append("WPA2")
            elif pkt.haslayer(Dot11Elt) and pkt[Dot11Elt].ID == 221 and pkt[Dot11Elt].info.startswith(b'\x00P\xf2\x01\x01\x00'):
                security.append("WPA")
            
            if not security:
                security.append("OPEN")

            # Store or update the network information
            if bssid not in self.networks:
                self.networks[bssid] = WifiNetwork(ssid, bssid, channel, signal_strength, security)
            else:
                # Update signal strength if we've seen this network before
                self.networks[bssid].signal_strength = max(self.networks[bssid].signal_strength, signal_strength)

    def print_results(self) -> None:
        print("\nScanned Wi-Fi Networks:")
        print("SSID".ljust(33) + "BSSID".ljust(19) + "Channel".ljust(9) + "Signal".ljust(8) + "Security")
        print("-" * 80)
        # Sort networks by signal strength and print
        for network in sorted(self.networks.values(), key=lambda x: x.signal_strength, reverse=True):
            print(f"{network.ssid[:30].ljust(33)}{network.bssid.ljust(19)}{str(network.channel).ljust(9)}"
                  f"{str(network.signal_strength).ljust(8)}{', '.join(network.security)}")
            
    def run(self):
        self.interface = input("Enter the name of the network interface to use for scanning: ")
        self.timeout = int(input("Enter the timeout length in seconds (optional): "))
        self.scan()
        self.print_results()
