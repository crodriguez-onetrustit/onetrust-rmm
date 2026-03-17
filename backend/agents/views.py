from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Client, Site, Agent, Script, Task, Alert, Check
from .serializers import (
    ClientSerializer, SiteSerializer, AgentSerializer, 
    ScriptSerializer, TaskSerializer, AlertSerializer, CheckSerializer
)

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
