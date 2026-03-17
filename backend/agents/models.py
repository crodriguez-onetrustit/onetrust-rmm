from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    """Organization/client"""
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Site(models.Model):
    """Location/site under a client"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.client.name} - {self.name}"

class Agent(models.Model):
    """Managed agent on a client machine"""
    OS_CHOICES = [
        ('windows', 'Windows'),
        ('macos', 'macOS'),
        ('linux', 'Linux'),
    ]
    
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('pending', 'Pending'),
    ]
    
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='agents')
    hostname = models.CharField(max_length=255)
    agent_id = models.CharField(max_length=255, unique=True)
    os = models.CharField(max_length=20, choices=OS_CHOICES)
    os_version = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    cpu_usage = models.FloatField(default=0)
    memory_usage = models.FloatField(default=0)
    disk_usage = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.hostname} ({self.get_os_display()})"

class Script(models.Model):
    """Reusable scripts"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script_type = models.CharField(max_length=20, choices=[
        ('powershell', 'PowerShell'),
        ('bash', 'Bash'),
        ('python', 'Python'),
        ('batch', 'Batch'),
    ])
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """Scheduled or one-time tasks"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tasks')
    script = models.ForeignKey(Script, on_delete=models.SET_NULL, null=True, blank=True)
    command = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.agent.hostname} - {self.status}"

class Alert(models.Model):
    """Monitoring alerts"""
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='alerts')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.severity}: {self.title}"

class Check(models.Model):
    """Monitoring checks"""
    TYPE_CHOICES = [
        ('cpu', 'CPU Usage'),
        ('memory', 'Memory Usage'),
        ('disk', 'Disk Usage'),
        ('service', 'Service'),
        ('script', 'Script'),
    ]
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='checks')
    check_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    threshold = models.FloatField(null=True, blank=True)
    service_name = models.CharField(max_length=255, blank=True)
    enabled = models.BooleanField(default=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.agent.hostname} - {self.name}"
