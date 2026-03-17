#!/usr/bin/env python3
"""
OneTrust RMM Agent
Lightweight agent that reports to the RMM server
"""

import os
import sys
import time
import json
import uuid
import socket
import platform
import subprocess
import requests
from datetime import datetime

class RMMAgent:
    def __init__(self, server_url, api_key=None):
        self.server_url = server_url.rstrip('/')
        self.agent_id = self.get_or_create_agent_id()
        self.hostname = socket.gethostname()
        self.os = self.get_os()
        
    def get_or_create_agent_id(self):
        """Get or create unique agent ID"""
        id_file = '/etc/onetrust-agentid' if os.name != 'nt' else 'C:\\ProgramData\\onetrust-agentid'
        
        if os.path.exists(id_file):
            with open(id_file, 'r') as f:
                return f.read().strip()
        
        agent_id = str(uuid.uuid4())
        try:
            os.makedirs(os.path.dirname(id_file), exist_ok=True)
            with open(id_file, 'w') as f:
                f.write(agent_id)
        except:
            pass
        return agent_id
    
    def get_os(self):
        """Detect OS"""
        system = platform.system().lower()
        if system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'macos'
        return 'linux'
    
    def get_system_info(self):
        """Get system metrics"""
        info = {
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
        }
        
        try:
            if self.os == 'windows':
                # CPU
                result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage'], 
                    capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        info['cpu_usage'] = int(lines[1])
                
                # Memory
                result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize'], 
                    capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        parts = lines[1].split()
                        if len(parts) >= 2:
                            free = int(parts[0])
                            total = int(parts[1])
                            info['memory_usage'] = round((total - free) / total * 100, 1)
                
                # Disk
                result = subprocess.run(['wmic', 'logicaldisk', 'get', 'size,freespace,caption'], 
                    capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    total = free = 0
                    for line in lines[1:]:
                        parts = line.split()
                        if len(parts) >= 3:
                            free += int(parts[1]) if parts[1].isdigit() else 0
                            total += int(parts[2]) if parts[2].isdigit() else 0
                    if total > 0:
                        info['disk_usage'] = round((total - free) / total * 100, 1)
            
            elif self.os == 'linux' or self.os == 'macos':
                # CPU
                result = subprocess.run(['top', '-bn1'], capture_output=True, text=True)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'Cpu(s)' in line or 'CPU' in line:
                            parts = line.split(',')
                            for p in parts:
                                if 'id' in p.lower():
                                    idle = float(p.split()[0])
                                    info['cpu_usage'] = round(100 - idle, 1)
                
                # Memory
                result = subprocess.run(['free', '-m'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    if len(lines) > 1:
                        parts = lines[1].split()
                        if len(parts) >= 3:
                            total = int(parts[1])
                            used = int(parts[2])
                            info['memory_usage'] = round(used / total * 100, 1) if total > 0 else 0
                
                # Disk
                result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    if len(lines) > 1:
                        parts = lines[1].split()
                        if len(parts) >= 5:
                            info['disk_usage'] = float(parts[4].rstrip('%'))
        except Exception as e:
            print(f"Error getting system info: {e}")
        
        return info
    
    def get_ip_address(self):
        """Get IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'
    
    def register(self):
        """Register agent with server"""
        # For now, return True - registration handled by server
        return True
    
    def heartbeat(self):
        """Send heartbeat to server"""
        info = self.get_system_info()
        
        data = {
            'agent_id': self.agent_id,
            'hostname': self.hostname,
            'os': self.os,
            'ip_address': self.get_ip_address(),
            'status': 'online',
            'cpu_usage': info['cpu_usage'],
            'memory_usage': info['memory_usage'],
            'disk_usage': info['disk_usage'],
        }
        
        try:
            response = requests.post(
                f'{self.server_url}/api/agents/heartbeat/',
                json=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Heartbeat failed: {e}")
            return False
    
    def run(self, interval=60):
        """Main agent loop"""
        print(f"OneTrust RMM Agent starting...")
        print(f"Agent ID: {self.agent_id}")
        print(f"Hostname: {self.hostname}")
        print(f"OS: {self.os}")
        print(f"Server: {self.server_url}")
        
        while True:
            try:
                if self.heartbeat():
                    print(f"[{datetime.now()}] Heartbeat sent successfully")
                else:
                    print(f"[{datetime.now()}] Heartbeat failed")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(interval)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='OneTrust RMM Agent')
    parser.add_argument('--server', default='http://localhost:8000', help='RMM Server URL')
    parser.add_argument('--interval', type=int, default=60, help='Heartbeat interval in seconds')
    args = parser.parse_args()
    
    agent = RMMAgent(args.server)
    agent.run(interval=args.interval)
