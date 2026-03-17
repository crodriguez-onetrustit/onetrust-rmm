# OneTrust RMM Agent

Lightweight cross-platform agent for OneTrust RMM.

## Requirements
- Python 3.7+
- psutil

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
# Basic
python agent.py --server http://your-rmm-server:8000

# With custom heartbeat interval (seconds)
python agent.py --server http://your-rmm-server:8000 --interval 30
```

## Windows Service

To run as a Windows service:
```bash
nssm install OneTrustAgent "C:\Python39\python.exe" "C:\path\to\agent.py --server http://server:8000"
```

## Linux Service

```bash
sudo cp onetrust-agent.service /etc/systemd/system/
sudo systemctl enable onetrust-agent
sudo systemctl start onetrust-agent
```

## Features
- Automatic system info collection (CPU, Memory, Disk)
- Heartbeat reporting
- Cross-platform (Windows, macOS, Linux)
