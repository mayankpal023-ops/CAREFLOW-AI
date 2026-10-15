"""Patient Requests Page"""
import streamlit as st
import pandas as pd
from utils.database import get_all_patient_requests, get_request_history

STATUS_OPTIONS = ["All", "submitted", "pending", "waiting_for_info", "processing", "completed", "cancelled"]

STATUS_LABELS = {
    'submitted': 'Submitted',
    'pending': 'Pending',
    'waiting_for_info': 'Waiting for Info',
    'processing': 'Processing',
    'completed': 'Completed',
    'cancelled': 'Cancelled'
}

def render_patient_requests():
    """Render the patient requests view."""
    st.header("Patient Requests")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", STATUS_OPTIONS, 
                                    format_func=lambda x: STATUS_LABELS.get(x, x.replace('_', ' ').title()) if x != "All" else "All")
    with col2:
        search = st.text_input("Search by Patient Name", placeholder="Type name...")
    with col3:
        st.write("")
        if st.button("Refresh", width="content"):
            st.rerun()
    
    # Get filtered data
    status_arg = None if status_filter == "All" else status_filter
    requests = get_all_patient_requests(status=status_arg)
    
    if search:
        requests = [r for r in requests if search.lower() in r['patient_name'].lower()]
    
    if not requests:
        st.info("No requests found. Try adjusting your filters or load demo data.")
        return
    
    st.write(f"**{len(requests)} request(s) found**")
    
    # Display requests
    for req in requests:
        status_label = STATUS_LABELS.get(req['status'], req['status'].replace('_', ' ').title())
        with st.expander(f"{req['patient_name']} — {req['category']} ({status_label})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Description:** {req['description']}")
                st.write(f"**Urgency:** {req['urgency']}")
                st.write(f"**Language:** {req.get('language', 'en')}")
                if req.get('accessibility_needs'):
                    st.write(f"**Accessibility Needs:** {req['accessibility_needs']}")
                if req.get('preferred_appointment_date'):
                    st.write(f"**Preferred Date:** {req['preferred_appointment_date']}")
                st.caption(f"Submitted: {req['created_at']}")
                
                if req.get('processing_time_minutes'):
                    st.write(f"**Processing Time:** {req['processing_time_minutes']} minutes")
            
            with col2:
                st.write("**Status History**")
                history = get_request_history(req['id'])
                for h in history[-3:]:
                    st.caption(f"- {STATUS_LABELS.get(h['new_status'], h['new_status'].replace('_', ' ').title())} ({h['created_at'][:16]})")