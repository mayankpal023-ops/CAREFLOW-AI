"""Regression tests for CareFlow AI application."""
import tempfile
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import utils.database as db
from utils.database import create_patient_request, get_patient_request, get_dashboard_metrics, get_db_connection

# Use a temporary database for testing - define at module level
test_db = tempfile.mktemp(suffix='.db')


def reset_db():
    """Set DATABASE_PATH to use temp database."""
    original_db = db.DB_PATH
    db.DB_PATH = test_db
    db.init_database()
    db.migrate_database()
    return original_db


def restore_db(original_db):
    """Restore original database path."""
    import utils.database as db2
    db2.DB_PATH = original_db


def test_empty_database():
    """Test dashboard metrics with an empty database."""
    print("TEST 1: Empty database...")
    original_db = reset_db()
    try:
        metrics = get_dashboard_metrics()
        assert metrics['total_requests'] == 0, f"Expected 0 total, got {metrics['total_requests']}"
        assert metrics['pending_requests'] == 0
        assert metrics['processing_requests'] == 0
        assert metrics['completed_requests'] == 0
        assert metrics['by_category'] == {}
        assert metrics['by_status'] == {}
        print("  PASS: Empty database returns zero metrics")
    finally:
        restore_db(original_db)


def test_sample_requests():
    """Test dashboard metrics with sample requests."""
    print("TEST 2: Sample requests...")
    original_db = reset_db()
    try:
        request_data = {
            'patient_name': 'Test Patient',
            'patient_email': 'test@test.com',
            'patient_phone': '555-0000',
            'preferred_contact_method': 'email',
            'category': 'Appointment booking',
            'urgency': 'Routine',
            'description': 'Test request for regression testing',
            'preferred_appointment_date': '2026-11-15',
            'language': 'en',
            'accessibility_needs': ''
        }
        request_id = create_patient_request(request_data)
        
        metrics = get_dashboard_metrics()
        
        assert metrics['total_requests'] >= 1, f"Expected >= 1 total, got {metrics['total_requests']}"
        assert 'Appointment booking' in metrics['by_category'], f"Expected 'Appointment booking' in categories, got {metrics['by_category']}"
        print("  PASS: Sample requests populate metrics correctly")
    finally:
        restore_db(original_db)


def test_status_counts():
    """Test that status counts are consistent."""
    print("TEST 3: Status counts consistency...")
    original_db = reset_db()
    try:
        from utils.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        test_requests = [
            ('TEST_SUBMITTED', 'Patient Submitted', 'submitted', 'General', 'Routine'),
            ('TEST_PENDING', 'Patient Pending', 'pending', 'General', 'Routine'),
            ('TEST_COMPLETED', 'Patient Completed', 'completed', 'General', 'Routine'),
        ]
        
        for req_id, name, status, cat, urg in test_requests:
            cursor.execute('''
                INSERT INTO patient_requests (id, patient_name, patient_email, patient_phone, 
                    category, urgency, description, status, language, accessibility_needs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (req_id, name, f'{name.lower()}@test.com', '555-0000', 
                  cat, urg, f'Test {status.lower()}', status, 'en', ''))
        
        conn.commit()
        conn.close()
        
        metrics = get_dashboard_metrics()
        
        status_keys = list(metrics['by_status'].keys())
        print(f"  Debug: Status keys in metrics = {status_keys}")
        assert 'submitted' in status_keys, f"Missing 'submitted' status. Keys: {status_keys}"
        assert 'pending' in status_keys, f"Missing 'pending' status. Keys: {status_keys}"
        assert 'completed' in status_keys, f"Missing 'completed' status. Keys: {status_keys}"
        assert metrics['by_status']['submitted'] >= 1, f"Expected >= 1 submitted, got {metrics['by_status'].get('submitted')}"
        assert metrics['by_status']['pending'] >= 1, f"Expected >= 1 pending, got {metrics['by_status'].get('pending')}"
        assert metrics['by_status']['completed'] >= 1, f"Expected >= 1 completed, got {metrics['by_status'].get('completed')}"
        print("  PASS: Status counts are consistent")
    finally:
        restore_db(original_db)


def test_demo_data_idempotency():
    """Test that loading demo data twice doesn't create duplicates."""
    print("TEST 4: Demo data idempotency...")
    original_db = reset_db()
    try:
        result1 = db.load_demo_data()
        assert 'requests' in result1
        assert result1['requests'] > 0
        
        result2 = db.load_demo_data()
        assert result2['message'] == 'Demo data already loaded', f"Expected 'already loaded' message, got: {result2['message']}"
        
        print("  PASS: Demo data idempotency check passed")
    finally:
        restore_db(original_db)


def test_reference_id_lookup():
    """Test request retrieval by reference ID."""
    print("TEST 5: Reference ID lookup...")
    original_db = reset_db()
    try:
        request_data = {
            'patient_name': 'Lookup Test',
            'patient_email': 'lookup@test.com',
            'patient_phone': '555-0000',
            'preferred_contact_method': 'email',
            'category': 'General clinic enquiry',
            'urgency': 'Routine',
            'description': 'Testing reference ID lookup',
            'preferred_appointment_date': '',
            'language': 'en',
            'accessibility_needs': ''
        }
        request_id = create_patient_request(request_data)
        
        retrieved = get_patient_request(request_id)
        
        assert retrieved is not None, "Request not found by reference ID"
        assert retrieved['patient_name'] == 'Lookup Test', f"Expected 'Lookup Test', got '{retrieved['patient_name']}'"
        assert retrieved['status'] == 'submitted', f"Expected 'submitted', got '{retrieved['status']}'"
        print("  PASS: Reference ID lookup works correctly")
    finally:
        restore_db(original_db)


def test_clear_data_preserves_real():
    """Test that clear_demo_data preserves real user requests."""
    print("TEST 6: Clear data preserves real records...")
    original_db = reset_db()
    try:
        request_data = {
            'patient_name': 'Real User',
            'patient_email': 'real@test.com',
            'patient_phone': '555-0000',
            'preferred_contact_method': 'email',
            'category': 'General clinic enquiry',
            'urgency': 'Routine',
            'description': 'This is a real user request that should survive clearing',
            'preferred_appointment_date': '',
            'language': 'en',
            'accessibility_needs': ''
        }
        real_id = create_patient_request(request_data)
        
        db.load_demo_data()
        
        db.clear_demo_data()
        
        retrieved = get_patient_request(real_id)
        assert retrieved is not None, "Real user request was deleted by clear_demo_data()"
        assert retrieved['patient_name'] == 'Real User', "Real user request name was changed"
        print("  PASS: Clear data preserves real records")
    finally:
        restore_db(original_db)


if __name__ == "__main__":
    print("=" * 60)
    print("CAREFLOW AI REGRESSION TESTS")
    print("=" * 60)
    
    tests = [
        test_empty_database,
        test_sample_requests,
        test_status_counts,
        test_demo_data_idempotency,
        test_reference_id_lookup,
        test_clear_data_preserves_real,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)
    
    if os.path.exists(test_db):
        try:
            os.unlink(test_db)
        except PermissionError:
            pass
    
    sys.exit(0 if failed == 0 else 1)