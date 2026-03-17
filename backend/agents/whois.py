"""WHOIS lookup for domains"""
import subprocess
import socket

def whois_lookup(domain):
    """Perform WHOIS lookup"""
    try:
        # Simple whois via CLI
        result = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=10)
        return result.stdout
    except:
        return "WHOIS not available"

def get_domain_info(domain):
    """Get basic domain info"""
    info = {
        'domain': domain,
        'ip': None,
        'resolved': False
    }
    
    try:
        info['ip'] = socket.gethostbyname(domain)
        info['resolved'] = True
    except:
        pass
    
    return info
