"""Enhanced system monitoring for agent"""
import psutil
import platform

def get_all_metrics():
    """Get comprehensive system metrics"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    
    return {
        'cpu': cpu,
        'cpu_count': psutil.cpu_count(),
        'memory_total': memory.total,
        'memory_available': memory.available,
        'memory_percent': memory.percent,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_free': disk.free,
        'disk_percent': disk.percent,
        'network_sent': network.bytes_sent,
        'network_recv': network.bytes_recv,
        'uptime': psutil.boot_time(),
        'platform': platform.platform(),
        'python_version': platform.python_version(),
    }
    
    boot_time = psutil.boot_time()
    uptime_seconds = now - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return {
        'cpu': cpu,
        'memory': memory.percent,
        'disk': disk.percent,
        'network_sent': network.bytes_sent,
        'network_recv': network.bytes_recv,
        'uptime_hours': hours,
    }

