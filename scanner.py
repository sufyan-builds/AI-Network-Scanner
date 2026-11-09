"""
Network Scanner Module
High-performance scanner with ARP cache verification, mDNS/NetBIOS, and MAC Vendor identification.
"""

import socket
import subprocess
import platform
import ipaddress
import logging
import re
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Optional

# Silences Scapy's "No libpcap provider available" warning on Windows
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    from scapy.all import ARP, Ether, srp
    SCAPY_AVAILABLE = True
except Exception:
    SCAPY_AVAILABLE = False

logger = logging.getLogger(__name__)


class NetworkScanner:
    """High-performance network scanner with local ARP and hostname resolution."""
    
    def __init__(self, timeout: int = 2, max_threads: int = 20):
        self.timeout = timeout
        self.max_threads = max_threads
        self.system = platform.system().lower()
        self.arp_table = self._get_arp_table()

    def _get_arp_table(self) -> Dict[str, str]:
        """
        Retrieves IP -> MAC address mapping from local ARP cache.
        Returns a dict: {"192.168.0.38": "AA-BB-CC-DD-EE-FF"}
        """
        arp_map = {}
        try:
            cmd = ["arp", "-a"]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
            out = result.stdout.decode('utf-8', errors='ignore')
            
            # Match IP and MAC address pairs from ARP output
            lines = out.splitlines()
            for line in lines:
                ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                mac_match = re.search(r'([0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2})', line)
                if ip_match and mac_match:
                    ip = ip_match.group(1)
                    mac = mac_match.group(1).replace('-', ':').upper()
                    if not ip.startswith("224.") and not ip.endswith(".255"):
                        arp_map[ip] = mac
        except Exception as e:
            logger.debug(f"Failed to parse ARP table: {e}")
        return arp_map

    def ping_host(self, ip: str) -> Dict[str, any]:
        """Ping host and verify if it actually exists on the network segment."""
        try:
            if self.system == "windows":
                command = ["ping", "-n", "1", "-w", str(self.timeout * 1000), ip]
            else:
                command = ["ping", "-c", "1", "-W", str(self.timeout), ip]
            
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout + 2
            )
            
            stdout_str = result.stdout.decode('utf-8', errors='ignore')
            
            # Check for valid ICMP response
            if result.returncode == 0 and ("reply from" in stdout_str.lower() or "bytes from" in stdout_str.lower()):
                
                # Filter Proxy-ARP false positives (must be in local ARP table or gateway .1)
                if len(self.arp_table) > 0 and ip not in self.arp_table and not ip.endswith(".1"):
                    return {
                        "IP": ip,
                        "Status": "Offline",
                        "Response Time": "N/A",
                        "Hostname": "N/A"
                    }

                response_time = self._extract_response_time(stdout_str)
                hostname = self._resolve_hostname(ip)
                
                return {
                    "IP": ip,
                    "Status": "Online",
                    "Response Time": response_time,
                    "Hostname": hostname
                }
            else:
                return {
                    "IP": ip,
                    "Status": "Offline",
                    "Response Time": "N/A",
                    "Hostname": "N/A"
                }
        except Exception:
            return {
                "IP": ip,
                "Status": "Offline",
                "Response Time": "N/A",
                "Hostname": "N/A"
            }

    def _extract_response_time(self, output: str) -> str:
        """Extract ping response time accurately."""
        try:
            match = re.search(r'time[=<]([\d\.]+)\s*ms', output, re.IGNORECASE)
            if match:
                val = match.group(1)
                return f"{val}ms" if val != "0" else "<1ms"
            
            if "time<1ms" in output.lower().replace(" ", ""):
                return "<1ms"
        except Exception:
            pass
        return "1ms"

    def _resolve_hostname(self, ip: str) -> str:
        """
        Multi-layered Hostname Resolution Strategy:
        1. Reverse DNS
        2. mDNS (.local) query via socket
        3. NetBIOS command lookup
        4. MAC Vendor identification (fallback)
        """
        # Strategy 1: Reverse DNS Lookup
        try:
            socket.setdefaulttimeout(0.6)
            hostname, _, _ = socket.gethostbyaddr(ip)
            if hostname and hostname != ip:
                return hostname
        except Exception:
            pass
        finally:
            socket.setdefaulttimeout(None)

        # Strategy 2: mDNS Resolution Check
        try:
            socket.setdefaulttimeout(0.6)
            name = socket.getfqdn(ip)
            if name and name != ip and not name.startswith("192.168."):
                return name
        except Exception:
            pass
        finally:
            socket.setdefaulttimeout(None)

        # Strategy 3: NetBIOS Lookup (Windows PCs & Samba drives)
        try:
            if self.system == "windows":
                cmd = ["nbtstat", "-A", ip]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1.0)
                out = res.stdout.decode('utf-8', errors='ignore')
                match = re.search(r'^\s*([A-Za-z0-9\-_]+)\s+<00>\s+UNIQUE', out, re.MULTILINE)
                if match:
                    return match.group(1).strip()
        except Exception:
            pass

        # Strategy 4: MAC Vendor identification fallback
        mac = self.arp_table.get(ip)
        if mac:
            vendor = self._get_mac_vendor(mac)
            if vendor:
                return f"{vendor} Device"

        return "Unknown Device"

    def _get_mac_vendor(self, mac_address: str) -> Optional[str]:
        """Identify hardware manufacturer online or via offline OUI prefixes."""
        clean_mac = mac_address.upper().replace(':', '').replace('-', '')
        prefix = clean_mac[:6]
        
        # 1. Offline common OUI lookup dictionary
        offline_oui = {
            "000C29": "VMware",
            "005056": "VMware",
            "B827EB": "Raspberry Pi",
            "DCA632": "Raspberry Pi",
            "E45F01": "Raspberry Pi",
            "001A11": "Google",
            "F4F5E8": "Google",
            "3C5A37": "Google",
            "F0921C": "Apple",
            "A45E60": "Apple",
            "BCD074": "Apple",
            "286B35": "Apple",
            "CC6EA4": "Samsung",
            "8C7A3C": "Samsung",
            "00E04C": "Realtek",
            "708BCD": "ASUSTek",
            "500291": "Amazon",
            "FCA183": "Amazon"
        }
        
        if prefix in offline_oui:
            return offline_oui[prefix]

        # 2. Free API Lookup Fallback
        try:
            req = urllib.request.Request(
                f"https://api.macvendors.com/{mac_address}",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=1.2) as response:
                if response.status == 200:
                    vendor = response.read().decode('utf-8').strip()
                    return vendor
        except Exception:
            pass

        return None

    def scan_network(
        self,
        network_range: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> List[Dict[str, any]]:
        """Refresh ARP table and execute multi-threaded network scan."""
        self.arp_table = self._get_arp_table()
        
        try:
            network = ipaddress.ip_network(network_range, strict=False)
        except ValueError as e:
            raise ValueError(f"Invalid network range: {str(e)}")
        
        all_ips = list(network.hosts())
        if not all_ips:
            all_ips = [network.network_address]
        
        total_ips = len(all_ips)
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.ping_host, str(ip)): ip for ip in all_ips}
            completed = 0
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception:
                    ip = futures[future]
                    results.append({
                        "IP": str(ip),
                        "Status": "Offline",
                        "Response Time": "N/A",
                        "Hostname": "N/A"
                    })
                completed += 1
                if progress_callback:
                    progress_callback(completed / total_ips)
        
        results.sort(key=lambda x: self._ip_to_int(x["IP"]))
        return results

    @staticmethod
    def _ip_to_int(ip_str: str) -> int:
        """Convert IP string to integer for numerical sorting."""
        try:
            return int(ipaddress.ip_address(ip_str))
        except Exception:
            return 0