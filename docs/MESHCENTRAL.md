# MeshCentral Integration

## Overview
MeshCentral is a web-based remote desktop/terminal solution. We integrate with it for:
- Remote desktop control
- Remote terminal/shell
- File transfer

## Setup

### 1. Deploy MeshCentral Server
```bash
# Using Docker
docker run -d -p 443:443 -p 80:80 -p 22:22 --name mesh \
  -v meshdata:/data \
  -e HOSTNAME=mesh.yourdomain.com \
  ajpuck/meshcentral:latest
```

### 2. Configure Agent
The agent includes MeshAgent. When installed, it will:
- Connect to MeshCentral server
- Register itself for remote access
- Enable terminal, desktop, and file transfer

### 3. Integration in RMM

```python
# In agents/views.py - get mesh agent info
def get_mesh_info(request, agent_id):
    """Get MeshCentral connection info for agent"""
    agent = Agent.objects.get(agent_id=agent_id)
    
    # MeshCentral typically uses mesh agent ID
    mesh_url = settings.MESHCENTRAL_URL
    
    return {
        'desktop_url': f'{mesh_url}/mesh?id={agent.agent_id}',
        'terminal_url': f'{mesh_url}/terminal?id={agent.agent_id}',
        'files_url': f'{mesh_url}/files?id={agent.agent_id}',
    }
```

## MeshAgent Integration

### Windows
```powershell
# Install MeshAgent via group policy or script
# Download from MeshCentral server
Invoke-WebRequest -Uri "https://your-mesh-server/meshagent.msi" -OutFile meshagent.msi
msiexec /i meshagent.msi
```

### Linux
```bash
# Download and install
curl -o meshagent https://your-mesh-server/meshagent
chmod +x meshagent
./meshagent -server https://your-mesh-server -username admin -password xxx
```

### macOS
```bash
# Download and install
curl -o meshagent.pkg https://your-mesh-server/meshagent-macos.pkg
sudo installer -pkg meshagent.pkg -target /
```

## Environment Variables

```bash
# Backend settings
MESHCENTRAL_URL=https://mesh.yourdomain.com
MESHCENTRAL_API_KEY=your-api-key
```

## Features Enabled
- 🖥️ Remote Desktop
- 💻 Terminal/Shell
- 📁 File Transfer
- 📋 Clipboard Sync
