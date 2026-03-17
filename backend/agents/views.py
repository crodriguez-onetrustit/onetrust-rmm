from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Client, Site, Agent, Script, Task, Alert, Check
from .serializers import (
    ClientSerializer, SiteSerializer, AgentSerializer, 
    ScriptSerializer, TaskSerializer, AlertSerializer, CheckSerializer
)

# Agent API - public endpoints for agent communication
@permission_classes([AllowAny])
def agent_heartbeat(request):
    """Agent heartbeat - no auth required"""
    from django.utils import timezone
    
    agent_id = request.data.get('agent_id')
    hostname = request.data.get('hostname')
    os_type = request.data.get('os')
    ip_address = request.data.get('ip_address')
    cpu = request.data.get('cpu_usage', 0)
    memory = request.data.get('memory_usage', 0)
    disk = request.data.get('disk_usage', 0)
    
    try:
        agent = Agent.objects.get(agent_id=agent_id)
        agent.status = 'online'
        agent.last_seen = timezone.now()
        agent.ip_address = ip_address
        agent.cpu_usage = cpu
        agent.memory_usage = memory
        agent.disk_usage = disk
        agent.save()
        return Response({'status': 'ok', 'action': 'updated'})
    except Agent.DoesNotExist:
        # Create new agent if doesn't exist
        site, _ = Site.objects.get_or_create(
            name='Default Site',
            client=Client.objects.first() or Client.objects.create(name='Default Client')
        )
        agent = Agent.objects.create(
            site=site,
            agent_id=agent_id,
            hostname=hostname,
            os=os_type,
            ip_address=ip_address,
            status='online',
            cpu_usage=cpu,
            memory_usage=memory,
            disk_usage=disk,
            last_seen=timezone.now()
        )
        return Response({'status': 'ok', 'action': 'created', 'agent_id': agent.id})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)

@permission_classes([AllowAny])
def agent_task(request):
    """Get pending tasks for agent"""
    agent_id = request.data.get('agent_id')
    
    try:
        agent = Agent.objects.get(agent_id=agent_id)
        pending_tasks = agent.tasks.filter(status='pending')
        
        tasks_data = []
        for task in pending_tasks:
            tasks_data.append({
                'id': task.id,
                'command': task.command or task.script.content if task.script else '',
                'script_type': task.script.script_type if task.script else 'bash'
            })
        
        return Response({'tasks': tasks_data})
    except Agent.DoesNotExist:
        return Response({'tasks': []})

@permission_classes([AllowAny])
def agent_task_complete(request):
    """Mark task as completed"""
    task_id = request.data.get('task_id')
    output = request.data.get('output', '')
    error = request.data.get('error', '')
    status_result = request.data.get('status', 'completed')
    
    try:
        task = Task.objects.get(id=task_id)
        task.status = status_result
        task.output = output
        task.error = error
        task.save()
        return Response({'status': 'ok'})
    except Task.DoesNotExist:
        return Response({'status': 'error', 'message': 'Task not found'}, status=404)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Site.objects.filter(client__id=self.kwargs.get('client_pk'))

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Agent.objects.filter(site__id=self.kwargs.get('site_pk'))
    
    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        """Agent heartbeat - updates status and system info"""
        agent = self.get_object()
        agent.status = request.data.get('status', 'online')
        agent.cpu_usage = request.data.get('cpu_usage', 0)
        agent.memory_usage = request.data.get('memory_usage', 0)
        agent.disk_usage = request.data.get('disk_usage', 0)
        agent.ip_address = request.data.get('ip_address')
        agent.save()
        return Response({'status': 'ok'})
    
    @action(detail=True, methods=['post'])
    def run_command(self, request, pk=None):
        """Run a command on agent"""
        agent = self.get_object()
        command = request.data.get('command', '')
        
        # Create task
        task = Task.objects.create(
            agent=agent,
            command=command,
            status='pending'
        )
        
        return Response({
            'task_id': task.id,
            'status': 'pending'
        })

class ScriptViewSet(viewsets.ModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark task as completed with output"""
        task = self.get_object()
        task.status = request.data.get('status', 'completed')
        task.output = request.data.get('output', '')
        task.error = request.data.get('error', '')
        task.save()
        return Response({'status': 'ok'})

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.acknowledged = True
        alert.acknowledged_by = request.user
        alert.save()
        return Response({'status': 'ok'})

class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = [IsAuthenticated]
