# OneTrust RMM

A modern Remote Monitoring & Management (RMM) platform for MSPs.

## Features

### Core
- **Agent Monitoring**: CPU, Memory, Disk, Network
- **Remote Commands**: Execute scripts on agents
- **Alerting**: Automatic alerts for threshold breaches
- **Task Queue**: Push tasks to agents

### Agent
- Cross-platform (Windows, macOS, Linux)
- Automatic registration
- Heartbeat system
- Task execution

### Integration
- MeshCentral ready for remote desktop
- REST API
- Vue.js frontend

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: Vue.js 3
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Agent**: Python 3

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Agent
```bash
cd agent
pip install -r requirements.txt
python agent.py --server http://localhost:8000
```

## API Endpoints

- `POST /api/agent/heartbeat/` - Agent check-in
- `POST /api/agent/tasks/` - Get pending tasks
- `POST /api/agent/task/complete/` - Report task result
- `GET /api/agents/` - List all agents
- `POST /api/tasks/` - Create task

## License

MIT
