"""
Utility Functions Module

Helper functions for validation, formatting, and data processing.
Includes network validation, input sanitization, and export functionality.
"""

import ipaddress
import logging
from typing import Optional, Dict, List
import pandas as pd

logger = logging.getLogger(__name__)


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_network_range(network_range: str) -> bool:
    """
    Validate network range in CIDR notation.
    
    Args:
        network_range: Network range string (e.g., 192.168.1.0/24)
        
    Returns:
        True if valid, False otherwise
    """
    if not network_range or "/" not in network_range:
        return False
    
    try:
        ipaddress.ip_network(network_range, strict=False)
        return True
    except (ValueError, TypeError):
        return False


def validate_ip_address(ip_string: str) -> bool:
    """
    Validate single IP address.
    
    Args:
        ip_string: IP address to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except (ValueError, TypeError):
        return False


def validate_api_key(api_key: str, min_length: int = 10) -> bool:
    """
    Basic API key validation.
    
    Args:
        api_key: API key to validate
        min_length: Minimum length required
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    api_key = api_key.strip()
    return len(api_key) >= min_length


# ============================================================================
# FORMATTING FUNCTIONS
# ============================================================================

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1m 30s" or "45s")
    """
    if seconds < 0:
        return "0s"
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    
    if minutes > 0:
        return f"{minutes}m {secs}s"
    return f"{secs}s"


def format_bytes(bytes_count: int) -> str:
    """
    Format byte count to readable string.
    
    Args:
        bytes_count: Number of bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    
    return f"{bytes_count:.2f} TB"


def format_percentage(value: float, total: float) -> str:
    """
    Calculate and format percentage.
    
    Args:
        value: Numerator
        total: Denominator
        
    Returns:
        Formatted percentage (e.g., "45.5%")
    """
    if total == 0:
        return "0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def export_to_csv(dataframe: pd.DataFrame) -> str:
    """
    Export DataFrame to CSV string.
    
    Args:
        dataframe: DataFrame to export
        
    Returns:
        CSV string
    """
    try:
        return dataframe.to_csv(index=False)
    except Exception as e:
        logger.error(f"CSV export failed: {e}")
        return ""


def export_to_json(dataframe: pd.DataFrame) -> str:
    """
    Export DataFrame to JSON string.
    
    Args:
        dataframe: DataFrame to export
        
    Returns:
        JSON string
    """
    try:
        return dataframe.to_json(orient="records", indent=2)
    except Exception as e:
        logger.error(f"JSON export failed: {e}")
        return ""


# ============================================================================
# STATISTICS FUNCTIONS
# ============================================================================

def calculate_statistics(scan_results: List[Dict]) -> Dict:
    """
    Calculate statistics from scan results.
    
    Args:
        scan_results: List of scan result dictionaries
        
    Returns:
        Dictionary with calculated statistics
    """
    if not scan_results:
        return {
            "total_scanned": 0,
            "online_count": 0,
            "offline_count": 0,
            "online_percentage": 0.0,
            "offline_percentage": 0.0,
            "avg_response_time": "N/A"
        }
    
    # Count devices
    online = [r for r in scan_results if r.get("Status") == "Online"]
    offline = [r for r in scan_results if r.get("Status") == "Offline"]
    total = len(scan_results)
    
    # Calculate percentages
    online_pct = (len(online) / total * 100) if total > 0 else 0
    offline_pct = (len(offline) / total * 100) if total > 0 else 0
    
    # Calculate average response time
    response_times = []
    for device in online:
        rt = device.get("Response Time", "N/A")
        if rt and rt != "N/A" and "ms" in str(rt):
            try:
                response_times.append(float(str(rt).replace("ms", "")))
            except ValueError:
                pass
    
    avg_response = f"{sum(response_times) / len(response_times):.1f}ms" if response_times else "N/A"
    
    return {
        "total_scanned": total,
        "online_count": len(online),
        "offline_count": len(offline),
        "online_percentage": round(online_pct, 1),
        "offline_percentage": round(offline_pct, 1),
        "avg_response_time": avg_response
    }


# ============================================================================
# NETWORK INFORMATION FUNCTIONS
# ============================================================================

def get_network_info(network_range: str) -> Optional[Dict]:
    """
    Get detailed information about a network range.
    
    Args:
        network_range: Network range in CIDR notation
        
    Returns:
        Dictionary with network info or None if invalid
    """
    try:
        network = ipaddress.ip_network(network_range, strict=False)
        
        return {
            "network": str(network.network_address),
            "broadcast": str(network.broadcast_address),
            "netmask": str(network.netmask),
            "prefix": network.prefixlen,
            "total_addresses": network.num_addresses,
            "total_hosts": network.num_addresses - 2
        }
    except Exception as e:
        logger.error(f"Failed to get network info: {e}")
        return None


def is_private_ip(ip_address: str) -> bool:
    """
    Check if IP is private (RFC 1918).
    
    Args:
        ip_address: IP to check
        
    Returns:
        True if private, False if public
    """
    try:
        return ipaddress.ip_address(ip_address).is_private
    except Exception:
        return False


def is_local_ip(ip_address: str) -> bool:
    """
    Check if IP is localhost/loopback.
    
    Args:
        ip_address: IP to check
        
    Returns:
        True if local, False otherwise
    """
    try:
        return ipaddress.ip_address(ip_address).is_loopback
    except Exception:
        return False


def get_default_gateway() -> Optional[str]:
    """
    Get default gateway IP address.
    
    Returns:
        Gateway IP or None if detection fails
    """
    try:
        import socket
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).connect(("8.8.8.8", 80))
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM).getsockname()[0]
        
        # Get local network by assuming /24
        parts = ip.split(".")
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    except Exception as e:
        logger.debug(f"Failed to detect default gateway: {e}")
        return None


# ============================================================================
# DEVICE CLASSIFICATION
# ============================================================================

def identify_device_type(hostname: str, ip_address: str) -> str:
    """
    Identify device type based on hostname and IP patterns.
    
    Args:
        hostname: Device hostname
        ip_address: Device IP address
        
    Returns:
        Device type string
    """
    hostname_lower = (hostname or "").lower()
    
    # Define patterns
    patterns = {
        "Router": ["router", "gateway", "modem", "192.168.1.1", "192.168.0.1"],
        "Printer": ["printer", "hp-", "canon", "brother", "xerox", "ricoh"],
        "Mobile": ["iphone", "android", "galaxy", "pixel", "mobile"],
        "Computer": ["desktop", "laptop", "pc", "windows", "linux", "macbook"],
        "Server": ["server", "nas", "host", "www"],
        "IoT": ["alexa", "echo", "camera", "light", "thermostat", "iot"]
    }
    
    # Check patterns
    for device_type, keywords in patterns.items():
        for keyword in keywords:
            if keyword in hostname_lower or keyword in ip_address:
                return device_type
    
    return "Unknown"


# ============================================================================
# DATA FILTERING AND SORTING
# ============================================================================

def filter_results(
    results: List[Dict],
    status: Optional[str] = None,
    hostname: Optional[str] = None,
    ip: Optional[str] = None
) -> List[Dict]:
    """
    Filter scan results based on criteria.
    
    Args:
        results: List of scan results
        status: Filter by status ("Online", "Offline", None for all)
        hostname: Filter by hostname (partial match)
        ip: Filter by IP (partial match)
        
    Returns:
        Filtered results
    """
    filtered = results
    
    if status:
        filtered = [r for r in filtered if r.get("Status") == status]
    
    if hostname:
        hostname_lower = hostname.lower()
        filtered = [
            r for r in filtered
            if hostname_lower in r.get("Hostname", "").lower()
        ]
    
    if ip:
        filtered = [r for r in filtered if ip in r.get("IP", "")]
    
    return filtered


def search_results(results: List[Dict], query: str) -> List[Dict]:
    """
    Search results by IP or hostname.
    
    Args:
        results: List of scan results
        query: Search query
        
    Returns:
        Matching results
    """
    query_lower = query.lower()
    
    return [
        r for r in results
        if (query_lower in r.get("IP", "").lower() or
            query_lower in r.get("Hostname", "").lower())
    ]


# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================

def get_default_settings() -> Dict:
    """
    Get default application settings.
    
    Returns:
        Dictionary with default settings
    """
    return {
        "timeout": 2,
        "max_threads": 20,
        "theme": "light",
        "auto_resolve_hostnames": True,
        "groq_api_key": ""
    }
