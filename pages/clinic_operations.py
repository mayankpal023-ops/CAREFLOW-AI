"""Clinic Operations Page"""
import streamlit as st
import pandas as pd
from utils.database import (
    get_all_patient_requests, update_request_status, get_all_staff,
    assign_staff_to_request, get_staff_workload, create_staff, get_staff_by_id
)

STATUSES = ["submitted", "pending", "waiting_for_info", "processing", "completed", "cancelled"]

def _invalidate_metrics_cache():
    """Invalidate the cached metrics so dashboard updates immediately."""
    try:
        from app import cached_metrics
        cached_metrics.clear()
    except Exception:
        pass

def render_clinic_operations():
    """Render the clinic operations dashboard."""
    st.header("Clinic Operations")
    
    tab1, tab2, tab3 = st.tabs(["Process Requests", "Staff Management", "Staff Workload"])
    
    # Tab 1: Process Requests
    with tab1:
        st.subheader("Active Requests Queue")
        
        # Get non-completed requests
        active_requests = get_all_patient_requests()
        active_requests = [r for r in active_requests if r['status'] not in ['completed', 'cancelled']]
        
        if not active_requests:
            st.info("Queue is empty. No pending requests to process.")
        else:
            # Summary table
            st.write("**Queue Summary:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Submitted", sum(1 for r in active_requests if r['status'] == 'submitted'))
            with col2:
                st.metric("Pending", sum(1 for r in active_requests if r['status'] == 'pending'))
            with col3:
                st.metric("Waiting for Info", sum(1 for r in active_requests if r['status'] == 'waiting_for_info'))
            with col4:
                st.metric("Processing", sum(1 for r in active_requests if r['status'] == 'processing'))
            
            st.write("")
            
            # Full table view
            if active_requests:
                df = pd.DataFrame([{
                    'ID': r['id'],
                    'Patient': r['patient_name'],
                    'Category': r['category'],
                    'Urgency': r['urgency'],
                    'Status': r['status'].replace('_', ' ').title(),
                    'Language': r.get('language', 'en'),
                    'Submitted': r['created_at'][:10]
                } for r in active_requests])
                st.dataframe(df, width="stretch", hide_index=True, alt="Active requests queue table")
            
            st.write("")
            st.subheader("Process Individual Requests")
            
            for req in active_requests:
                with st.expander(f"{req['patient_name']} — {req['category']} ({req['status'].replace('_', ' ').title()})"):
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.write(f"**Description:** {req['description']}")
                        st.write(f"**Urgency:** {req['urgency']}")
                        st.caption(f"Submitted: {req['created_at']}")
                        if req.get('preferred_appointment_date'):
                            st.write(f"**Preferred Date:** {req['preferred_appointment_date']}")
                        if req.get('accessibility_needs'):
                            st.write(f"**Accessibility:** {req['accessibility_needs']}")
                        if req.get('assigned_staff'):
                            staff = get_all_staff()
                            staff_names = {s['id']: s['name'] for s in staff}
                            st.write(f"**Assigned to:** {staff_names.get(req['assigned_staff'], 'Unknown')}")
                    
                    with col2:
                        st.write("**Actions**")
                        
                        staff_list = get_all_staff()
                        staff_options = {s['id']: f"{s['name']} ({s['role']})" for s in staff_list}
                        
                        selected_staff = st.selectbox(
                            "Assign to", 
                            list(staff_options.keys()),
                            format_func=lambda x: staff_options.get(x, "Unassigned"),
                            key=f"assign_{req['id']}"
                        )
                        
                        if st.button("Assign", key=f"btn_assign_{req['id']}", width="stretch"):
                            assign_staff_to_request(req['id'], selected_staff)
                            st.success(f"Assigned to {staff_options[selected_staff]}")
                            _invalidate_metrics_cache()
                            st.rerun()
                        
                        new_status = st.selectbox(
                            "Update Status",
                            STATUSES,
                            index=STATUSES.index(req['status']) if req['status'] in STATUSES else 0,
                            key=f"status_{req['id']}"
                        )
                        
                        if st.button("Update Status", key=f"btn_status_{req['id']}", width="stretch"):
                            update_request_status(req['id'], new_status, "Clinic Staff")
                            st.success(f"Status updated to {new_status.replace('_', ' ').title()}")
                            _invalidate_metrics_cache()
                            st.rerun()
                        
                        # Quick action buttons
                        if new_status == 'waiting_for_info':
                            if st.button("Request More Info", key=f"btn_info_{req['id']}", width="stretch", type="primary"):
                                update_request_status(req['id'], 'waiting_for_info', 'Clinic Staff', 'Additional information requested from patient')
                                st.success("Status updated to Waiting for Info")
                                _invalidate_metrics_cache()
                                st.rerun()
    
    # Tab 2: Staff Management
    with tab2:
        st.subheader("Staff Directory")
        
        staff = get_all_staff()
        if staff:
            df = pd.DataFrame(staff)
            st.dataframe(df[['name', 'role', 'department', 'email']], width="stretch", hide_index=True, alt="Staff directory table")
        else:
            st.info("No staff members found.")
        
        st.write("")
        st.subheader("Add New Staff Member")
        
        with st.form("add_staff_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                role = st.text_input("Role *")
            with col2:
                email = st.text_input("Email")
                department = st.text_input("Department")
            
            if st.form_submit_button("Add Staff Member", type="primary"):
                if name and role:
                    create_staff({'name': name, 'role': role, 'email': email, 'department': department})
                    st.success(f"Added {name} to staff directory")
                    _invalidate_metrics_cache()
                    st.rerun()
                else:
                    st.error("Name and Role are required")
    
    # Tab 3: Staff Workload
    with tab3:
        st.subheader("Current Workload Distribution")
        
        workload = get_staff_workload()
        if workload:
            df = pd.DataFrame(workload)
            st.dataframe(df, width="stretch", hide_index=True, alt="Staff workload distribution table")
            
            st.write("")
            st.write("**Workload Tips:**")
            st.info("Requests are assigned to staff members. Consider redistributing if any team member has more than 3 active requests.")
        else:
            st.info("No workload data available.")