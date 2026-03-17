"""Alert generation for monitoring"""
from .models import Agent, Alert
from .monitoring import SystemMonitor

def check_agent(agent):
    """Check agent and generate alerts if needed"""
    monitor = SystemMonitor()
    alerts_created = []
    
    # Get current values
    cpu = monitor.get_cpu_usage()
    memory = monitor.get_memory()['percent']
    disk = monitor.get_disk()['percent']
    
    # Check CPU
    if cpu > 90:
        alert, created = Alert.objects.get_or_create(
            agent=agent,
            title='High CPU Usage',
            defaults={
                'severity': 'critical',
                'message': f'CPU usage at {cpu}%'
            }
        )
        if created:
            alerts_created.append('CPU')
    
    # Check Memory
    if memory > 90:
        alert, created = Alert.objects.get_or_create(
            agent=agent,
            title='High Memory Usage',
            defaults={
                'severity': 'critical',
                'message': f'Memory usage at {memory}%'
            }
        )
        if created:
            alerts_created.append('Memory')
    
    # Check Disk
    if disk > 90:
        alert, created = Alert.objects.get_or_create(
            agent=agent,
            title='High Disk Usage',
            defaults={
                'severity': 'warning',
                'message': f'Disk usage at {disk}%'
            }
        )
        if created:
            alerts_created.append('Disk')
    
    # Check offline
    from django.utils import timezone
    if agent.last_seen:
        import datetime
        if timezone.now() - agent.last_seen > datetime.timedelta(minutes=10):
            alert, created = Alert.objects.get_or_create(
                agent=agent,
                title='Agent Offline',
                defaults={
                    'severity': 'error',
                    'message': f'Agent last seen {agent.last_seen}'
                }
            )
            if created:
                alerts_created.append('Offline')
    
    return alerts_created

def check_all_agents():
    """Check all agents and generate alerts"""
    total = 0
    for agent in Agent.objects.all():
        alerts = check_agent(agent)
        total += len(alerts)
    return total
