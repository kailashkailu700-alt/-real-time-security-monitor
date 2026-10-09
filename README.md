\# 🛡️ Real-Time External Device Intrusion Detection \& Security Monitoring System



Full-stack cybersecurity project that monitors an external device in real time and detects suspicious activity.



\## Architecture



External Device → Python Agent → FastAPI Backend → Detection Engine → PostgreSQL → React Dashboard



\## Tech Stack



\- Frontend: React + Vite + Axios

\- Backend: FastAPI + SQLAlchemy

\- Database: PostgreSQL 17

\- Agent: Python + psutil



\## Features



\- Real-time device monitoring

\- Detection rules: failed logins, suspicious ports, port scan, high traffic

\- SOC-style dashboard with live updates

\- Alert deduplication



\## Setup



\### Backend

cd backend

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

python -m uvicorn app.main:app --reload



\### Agent

cd agent

python agent.py



\### Frontend

cd frontend

npm install

npm run dev



\## Detection Rules



| Rule | Severity |

|------|----------|

| 5+ failed logins in 5 min | CRITICAL |

| Suspicious port activity | HIGH |

| Port scan detected | HIGH |

| High network traffic | MEDIUM |



\## Author



\[Your Name] — B.Sc Computer Science with Cyber Security

