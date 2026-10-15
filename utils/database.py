"""
CareFlow AI - Database Layer
SQLite database operations for patient requests and clinic operations.
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from contextlib import contextmanager
import uuid

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'careflow.db')

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_connection():
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def db_transaction():
    """Context manager for database transactions."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_database():
    """Initialize the database with required tables."""
    with db_transaction() as conn:
        cursor = conn.cursor()
        
        # Patient requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_requests (
                id TEXT PRIMARY KEY,
                patient_name TEXT NOT NULL,
                patient_email TEXT,
                patient_phone TEXT,
                preferred_contact_method TEXT DEFAULT 'email',
                category TEXT NOT NULL,
                urgency TEXT NOT NULL,
                description TEXT NOT NULL,
                preferred_appointment_date TEXT,
                status TEXT NOT NULL DEFAULT 'submitted',
                assigned_staff TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                processing_time_minutes INTEGER,
                language TEXT DEFAULT 'en',
                accessibility_needs TEXT,
                notes TEXT
            )
        ''')
        
        # Staff members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                email TEXT,
                department TEXT,
                active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Request status history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS request_history (
                id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                old_status TEXT,
                new_status TEXT NOT NULL,
                changed_by TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (request_id) REFERENCES patient_requests (id)
            )
        ''')
        
        # Clinic metrics cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clinic_metrics (
                id TEXT PRIMARY KEY,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_date DATE DEFAULT (DATE('now')),
                details TEXT
            )
        ''')
        
        # Demo data flag
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()

def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())[:8].upper()

# Patient Requests CRUD
def create_patient_request(data: Dict[str, Any]) -> str:
    """Create a new patient request."""
    request_id = generate_id()
    with db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_requests (
                id, patient_name, patient_email, patient_phone, preferred_contact_method,
                category, urgency, description, preferred_appointment_date,
                status, language, accessibility_needs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request_id,
            data.get('patient_name'),
            data.get('patient_email'),
            data.get('patient_phone'),
            data.get('preferred_contact_method', 'email'),
            data.get('category'),
            data.get('urgency'),
            data.get('description'),
            data.get('preferred_appointment_date', ''),
            'submitted',
            data.get('language', 'en'),
            data.get('accessibility_needs', '')
        ))
        
        # Add to history
        cursor.execute('''
            INSERT INTO request_history (id, request_id, new_status, changed_by, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (generate_id(), request_id, 'submitted', 'Patient Portal', 'Request submitted via patient portal'))
        
    return request_id

def get_patient_request(request_id: str) -> Optional[Dict]:
    """Get a patient request by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patient_requests WHERE id = ?', (request_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_all_patient_requests(status: Optional[str] = None, category: Optional[str] = None) -> List[Dict]:
    """Get all patient requests with optional filters."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM patient_requests WHERE 1=1'
        params = []
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        if category:
            query += ' AND category = ?'
            params.append(category)
            
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def update_request_status(request_id: str, new_status: str, changed_by: str, notes: str = '') -> bool:
    """Update request status and log history."""
    with db_transaction() as conn:
        cursor = conn.cursor()
        
        # Get current status
        cursor.execute('SELECT status, created_at FROM patient_requests WHERE id = ?', (request_id,))
        row = cursor.fetchone()
        if not row:
            return False
            
        old_status = row['status']
        created_at = row['created_at']
        
        # Calculate processing time if completing
        processing_time = None
        completed_at = None
        if new_status == 'completed' and old_status != 'completed':
            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            completed_dt = datetime.now()
            processing_time = int((completed_dt - created_dt).total_seconds() / 60)
            completed_at = completed_dt.isoformat()
        
        # Update request
        if processing_time:
            cursor.execute('''
                UPDATE patient_requests 
                SET status = ?, updated_at = ?, completed_at = ?, processing_time_minutes = ?
                WHERE id = ?
            ''', (new_status, datetime.now().isoformat(), completed_at, processing_time, request_id))
        else:
            cursor.execute('''
                UPDATE patient_requests 
                SET status = ?, updated_at = ?
                WHERE id = ?
            ''', (new_status, datetime.now().isoformat(), request_id))
        
        # Add to history
        cursor.execute('''
            INSERT INTO request_history (id, request_id, old_status, new_status, changed_by, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (generate_id(), request_id, old_status, new_status, changed_by, notes))
        
    return True

def assign_staff_to_request(request_id: str, staff_id: str) -> bool:
    """Assign a staff member to a request."""
    with db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE patient_requests 
            SET assigned_staff = ?, status = 'processing', updated_at = ?
            WHERE id = ?
        ''', (staff_id, datetime.now().isoformat(), request_id))
        
        # Add to history
        cursor.execute('''
            INSERT INTO request_history (id, request_id, old_status, new_status, changed_by, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (generate_id(), request_id, 'pending', 'processing', staff_id, f'Assigned to staff member'))
        
    return True

def get_request_history(request_id: str) -> List[Dict]:
    """Get status history for a request."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM request_history WHERE request_id = ? ORDER BY created_at ASC
        ''', (request_id,))
        return [dict(row) for row in cursor.fetchall()]

# Staff CRUD
def create_staff(data: Dict[str, Any]) -> str:
    """Create a new staff member."""
    staff_id = generate_id()
    with db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO staff (id, name, role, email, department)
            VALUES (?, ?, ?, ?, ?)
        ''', (staff_id, data['name'], data['role'], data.get('email'), data.get('department')))
    return staff_id

def get_all_staff(active_only: bool = True) -> List[Dict]:
    """Get all staff members."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM staff'
        if active_only:
            query += ' WHERE active = 1'
        query += ' ORDER BY name'
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]

def get_staff_by_id(staff_id: str) -> Optional[Dict]:
    """Get staff member by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM staff WHERE id = ?', (staff_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# Analytics
def get_dashboard_metrics() -> Dict[str, Any]:
    """Get all metrics for the overview dashboard."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total requests
        cursor.execute('SELECT COUNT(*) as count FROM patient_requests')
        total = cursor.fetchone()['count']
        
        # By status
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM patient_requests 
            GROUP BY status
        ''')
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # By category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM patient_requests 
            GROUP BY category
        ''')
        by_category = {row['category']: row['count'] for row in cursor.fetchall()}
        
        # Average processing time (completed requests only)
        cursor.execute('''
            SELECT AVG(processing_time_minutes) as avg_time
            FROM patient_requests 
            WHERE processing_time_minutes IS NOT NULL
        ''')
        avg_time_row = cursor.fetchone()
        avg_processing_time = round(avg_time_row['avg_time'], 1) if avg_time_row['avg_time'] else None
        
        # Recent requests (last 10)
        cursor.execute('''
            SELECT * FROM patient_requests 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        recent = [dict(row) for row in cursor.fetchall()]
        
        # Status counts
        pending = by_status.get('pending', 0) + by_status.get('submitted', 0)
        processing = by_status.get('processing', 0)
        waiting_for_info = by_status.get('waiting_for_info', 0)
        completed = by_status.get('completed', 0)
        
        # Old unresolved (pending for more than 24 hours)
        cursor.execute('''
            SELECT COUNT(*) as count FROM patient_requests
            WHERE status IN ('submitted', 'pending', 'waiting_for_info')
            AND created_at < DATETIME('now', '-1 day')
        ''')
        old_unresolved = cursor.fetchone()['count']
        
        return {
            'total_requests': total,
            'pending_requests': pending,
            'processing_requests': processing,
            'waiting_for_info': waiting_for_info,
            'completed_requests': completed,
            'avg_processing_time': avg_processing_time,
            'by_status': by_status,
            'by_category': by_category,
            'recent_requests': recent,
            'old_unresolved': old_unresolved
        }

def get_category_trends(days: int = 30) -> List[Dict]:
    """Get request trends by category over time."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                DATE(created_at) as date,
                category,
                COUNT(*) as count
            FROM patient_requests
            WHERE created_at >= DATE('now', ?)
            GROUP BY DATE(created_at), category
            ORDER BY date
        ''', (f'-{days} days',))
        return [dict(row) for row in cursor.fetchall()]

def get_status_distribution() -> List[Dict]:
    """Get current status distribution."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM patient_requests
            GROUP BY status
        ''')
        return [dict(row) for row in cursor.fetchall()]

def get_staff_workload() -> List[Dict]:
    """Get current workload per staff member."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                s.name,
                s.role,
                COUNT(pr.id) as active_requests
            FROM staff s
            LEFT JOIN patient_requests pr ON pr.assigned_staff = s.id 
                AND pr.status IN ('pending', 'processing', 'submitted')
            WHERE s.active = 1
            GROUP BY s.id, s.name, s.role
            ORDER BY active_requests DESC
        ''')
        return [dict(row) for row in cursor.fetchall()]

# Demo data
DEMO_PATIENTS = [
    {
        'patient_name': 'Maria Santos',
        'patient_email': 'maria.santos@email.com',
        'patient_phone': '(555) 123-4567',
        'preferred_contact_method': 'email',
        'category': 'Appointment booking',
        'urgency': 'Routine',
        'description': 'Need to schedule annual wellness checkup. Prefer morning appointments.',
        'preferred_appointment_date': '2026-11-15',
        'language': 'es',
        'accessibility_needs': 'Spanish language support required'
    },
    {
        'patient_name': 'James Chen',
        'patient_email': 'j.chen@email.com',
        'patient_phone': '(555) 234-5678',
        'preferred_contact_method': 'phone',
        'category': 'Medical report collection',
        'urgency': 'Urgent',
        'description': 'Need copies of recent lab results sent to specialist office before Friday.',
        'preferred_appointment_date': '2026-10-20',
        'language': 'en',
        'accessibility_needs': ''
    },
    {
        'patient_name': 'Aisha Johnson',
        'patient_email': 'aisha.j@email.com',
        'patient_phone': '(555) 345-6789',
        'preferred_contact_method': 'email',
        'category': 'Billing and insurance assistance',
        'urgency': 'Routine',
        'description': 'Question about coverage for recent lab work. Received unexpected bill and need help understanding charges.',
        'preferred_appointment_date': '',
        'language': 'en',
        'accessibility_needs': 'Screen reader compatible communications'
    },
    {
        'patient_name': 'Robert Kim',
        'patient_email': 'r.kim@email.com',
        'patient_phone': '(555) 456-7890',
        'preferred_contact_method': 'phone',
        'category': 'Appointment rescheduling',
        'urgency': 'Soon',
        'description': 'Need to reschedule appointment from Oct 25 to Nov 2 due to work conflict.',
        'preferred_appointment_date': '2026-11-02',
        'language': 'en',
        'accessibility_needs': ''
    },
    {
        'patient_name': 'Fatima Al-Rashid',
        'patient_email': 'fatima.rashid@email.com',
        'patient_phone': '(555) 567-8901',
        'preferred_contact_method': 'email',
        'category': 'Registration assistance',
        'urgency': 'Soon',
        'description': 'New patient, need help completing registration forms. Prefer Arabic-speaking staff.',
        'preferred_appointment_date': '2026-10-22',
        'language': 'ar',
        'accessibility_needs': 'Arabic language support, large print materials'
    },
    {
        'patient_name': 'David Thompson',
        'patient_email': 'd.thompson@email.com',
        'patient_phone': '(555) 678-9012',
        'preferred_contact_method': 'phone',
        'category': 'Accessibility assistance',
        'urgency': 'Urgent',
        'description': 'Wheelchair user, need to confirm ground-floor appointment room and accessible parking.',
        'preferred_appointment_date': '2026-10-18',
        'language': 'en',
        'accessibility_needs': 'Wheelchair accessible facility required'
    },
    {
        'patient_name': 'Elena Rodriguez',
        'patient_email': 'elena.r@email.com',
        'patient_phone': '(555) 789-0123',
        'preferred_contact_method': 'email',
        'category': 'General clinic enquiry',
        'urgency': 'Routine',
        'description': 'Follow up on blood work from last week. Want to understand what the results mean and next steps.',
        'preferred_appointment_date': '',
        'language': 'es',
        'accessibility_needs': 'Spanish language support required'
    },
    {
        'patient_name': 'Michael Okafor',
        'patient_email': 'm.okafor@email.com',
        'patient_phone': '(555) 890-1234',
        'preferred_contact_method': 'phone',
        'category': 'Billing and insurance assistance',
        'urgency': 'Soon',
        'description': 'Need to update insurance information and confirm coverage for upcoming procedure.',
        'preferred_appointment_date': '',
        'language': 'en',
        'accessibility_needs': 'Visual impairment - needs audio instructions'
    }
]

DEMO_STAFF = [
    {'name': 'Dr. Sarah Mitchell', 'role': 'Physician', 'email': 's.mitchell@clinic.com', 'department': 'Primary Care'},
    {'name': 'Nurse Practitioner Lisa Chen', 'role': 'Nurse Practitioner', 'email': 'l.chen@clinic.com', 'department': 'Primary Care'},
    {'name': 'Maria Gonzalez', 'role': 'Patient Coordinator', 'email': 'm.gonzalez@clinic.com', 'department': 'Front Desk'},
    {'name': 'James Wilson', 'role': 'Medical Assistant', 'email': 'j.wilson@clinic.com', 'department': 'Clinical Support'},
    {'name': 'Priya Patel', 'role': 'Insurance Specialist', 'email': 'p.patel@clinic.com', 'department': 'Billing'},
    {'name': 'David Park', 'role': 'Referral Coordinator', 'email': 'd.park@clinic.com', 'department': 'Care Coordination'},
]

def load_demo_data() -> Dict[str, int]:
    """Load demo data if not already loaded."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM app_state WHERE key = 'demo_loaded'")
        row = cursor.fetchone()
        if row and row['value'] == 'true':
            return {'requests': 0, 'staff': 0, 'message': 'Demo data already loaded'}
    
    requests_created = 0
    staff_created = 0
    
    # Create staff
    for staff in DEMO_STAFF:
        create_staff(staff)
        staff_created += 1
    
    # Create patient requests with varied statuses
    statuses = ['submitted', 'pending', 'processing', 'completed']
    for i, patient in enumerate(DEMO_PATIENTS):
        request_id = create_patient_request(patient)
        requests_created += 1
        
        # Update some to different statuses for demo
        if i < 2:
            update_request_status(request_id, 'pending', 'System', 'Demo: moved to pending')
        elif i < 4:
            update_request_status(request_id, 'processing', 'System', 'Demo: assigned to staff')
            # Assign staff
            staff_list = get_all_staff()
            if staff_list:
                assign_staff_to_request(request_id, staff_list[i % len(staff_list)]['id'])
        elif i < 6:
            update_request_status(request_id, 'completed', 'System', 'Demo: completed')
    
    # Mark demo as loaded
    with db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO app_state (key, value) VALUES (?, ?)
        ''', ('demo_loaded', 'true'))
    
    return {'requests': requests_created, 'staff': staff_created, 'message': f'Loaded {requests_created} demo requests and {staff_created} staff members'}

def clear_demo_data():
    """Clear only demo records, preserving real user requests."""
    with db_transaction() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM app_state WHERE key = 'demo_loaded'")
        # Only delete staff created during demo load
        cursor.execute("DELETE FROM staff WHERE email LIKE '%@clinic.com'")
        # Delete demo requests (those created by the demo system)
        cursor.execute('''
            DELETE FROM patient_requests 
            WHERE id IN (
                SELECT DISTINCT pr.id FROM patient_requests pr
                JOIN request_history rh ON rh.request_id = pr.id
                WHERE rh.changed_by = 'System' AND rh.notes LIKE 'Demo:%'
            )
        ''')
        # Clean up orphaned history
        cursor.execute('''
            DELETE FROM request_history 
            WHERE request_id NOT IN (SELECT id FROM patient_requests)
        ''')

def migrate_database():
    """Add new columns to existing database if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Check if preferred_contact_method column exists
        cursor.execute("PRAGMA table_info(patient_requests)")
        columns = [row['name'] for row in cursor.fetchall()]
        
        if 'preferred_contact_method' not in columns:
            cursor.execute("ALTER TABLE patient_requests ADD COLUMN preferred_contact_method TEXT DEFAULT 'email'")
        
        if 'preferred_appointment_date' not in columns:
            cursor.execute("ALTER TABLE patient_requests ADD COLUMN preferred_appointment_date TEXT")
        
        conn.commit()

# Initialize on import
init_database()
migrate_database()