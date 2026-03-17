"""Monitoring checks for agents"""
import psutil
import subprocess
from datetime import datetime

class SystemMonitor:
    @staticmethod
    def get_cpu_usage():
        return psutil.cpu_percent(interval=1)
    
    @staticmethod
    def get_memory():
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used
        }
    
    @staticmethod
    def get_disk():
        disk = psutil.disk_usage('/')
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    
    @staticmethod
    def get_processes():
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'cpu': p.info['cpu_percent'],
                    'memory': p.info['memory_percent']
                })
            except:
                pass
        return sorted(processes, key=lambda x: x['cpu'] or 0, reverse=True)[:10]
    
    @staticmethod
    def get_services():
        """Get running services"""
        services = []
        try:
            if hasattr(psutil, 'win_service_iter'):
                for s in psutil.win_service_iter():
                    services.append({
                        'name': s.name(),
                        'status': s.status()
                    })
        except:
            pass
        return services
    
    @staticmethod
    def check_service(name):
        """Check if a service is running"""
        try:
            if hasattr(psutil, 'win_service_get'):
                return psutil.win_service_get(name).status() == 'running'
        except:
            pass
        return False
    
    @staticmethod
    def get_network_stats():
        net = psutil.net_io_counters()
        return {
            'bytes_sent': net.bytes_sent,
            'bytes_recv': net.bytes_recv,
            'packets_sent': net.packets_sent,
            'packets_recv': net.packets_recv
        }
    
    @staticmethod
    def get_temperature():
        """Get CPU temperature if available"""
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        if entries:
                            return entries[0].current
        except:
            pass
        return None

def run_check(check_type, threshold=None, service_name=None):
    """Run a monitoring check"""
    monitor = SystemMonitor()
    
    if check_type == 'cpu':
        cpu = monitor.get_cpu_usage()
        return {
            'status': 'warning' if cpu > threshold else 'ok',
            'value': cpu,
            'threshold': threshold
        }
    
    elif check_type == 'memory':
        mem = monitor.get_memory()
        return {
            'status': 'warning' if mem['percent'] > threshold else 'ok',
            'value': mem['percent'],
            'threshold': threshold
        }
    
    elif check_type == 'disk':
        disk = monitor.get_disk()
        return {
            'status': 'warning' if disk['percent'] > threshold else 'ok',
            'value': disk['percent'],
            'threshold': threshold
        }
    
    elif check_type == 'service':
        is_running = monitor.check_service(service_name)
        return {
            'status': 'ok' if is_running else 'error',
            'service': service_name,
            'running': is_running
        }
    
    return {'status': 'unknown', 'error': 'Unknown check type'}
