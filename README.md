# CareFlow AI

**Better Access. Smarter Clinics. Faster Workflows.**

A healthcare operations platform for improved patient access and clinic workflows.

## Quick Start

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
streamlit run app.py
```

### 3. Access the App

Open your browser and navigate to `http://localhost:8501`

## Features

### Overview Dashboard
- Real-time operational metrics
- Request status visualization
- Bottleneck identification
- Recent activity feed

### Patient Portal
- Submit new healthcare requests
- Specify urgency and accessibility needs
- Multi-language support
- Request tracking

### Patient Requests
- View all submitted requests
- Filter by status and search by name
- Track request history and status changes

### Clinic Operations
- Process and assign requests
- Manage staff directory
- Monitor workload distribution
- Update request statuses

### Accessibility Assistant
- Identify accessibility needs in pending requests
- Language support dashboard
- Best practices guidelines

### Analytics
- Key performance indicators
- Category and status breakdowns
- Trend analysis over time

### About & Responsible AI
- Project information
- Responsible AI commitments
- Technical architecture details

## Project Structure

```
careflow-ai/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   └── careflow.db       # SQLite database (auto-generated)
├── pages/
│   ├── __init__.py
│   ├── overview.py       # Overview dashboard
│   ├── patient_portal.py # Patient request submission
│   ├── patient_requests.py # Request listing
│   ├── clinic_operations.py # Staff operations
│   ├── accessibility.py  # Accessibility tools
│   ├── analytics.py      # Analytics dashboard
│   └── about.py          # About page
└── utils/
    └── database.py       # Database operations
```

## Demo Data

Click "Load Demo Data" in the sidebar to populate the database with sample patient requests and staff members. This data is only loaded once to prevent duplicates.

## Responsible AI

CareFlow AI is built with responsible AI principles:
- **Fairness:** Multi-language and accessibility support
- **Transparency:** Clear status tracking and audit trails
- **Privacy:** Local data storage only
- **Accountability:** Human oversight of all decisions
- **Safety:** Urgent request flagging and escalation

## License

MIT License - Built for Hackathon 2026