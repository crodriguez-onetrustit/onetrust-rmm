# OneTrust RMM

Remote Monitoring & Management Platform

## Tech Stack
- Backend: Django + Django REST Framework
- Frontend: Vue.js 3
- Database: PostgreSQL
- Real-time: Django Channels

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Features
- Agent management (Windows, Mac, Linux)
- Remote shell execution
- Script management
- Monitoring & alerts
- MeshCentral integration (planned)
