"""Patient Requests Page"""
import streamlit as st
import pandas as pd
from utils.database import get_all_patient_requests, get_patient_request, get_request_history

STATUS_OPTIONS = ["All", "submitted", "pending", "processing", "completed", "cancelled"]

def render_patient_requests():
    """Render the patient requests view."""
    st.markdown('<p class="section-title">Patient Requests</p>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        status_filter = st.selectbox("Filter by Status", STATUS_OPTIONS)
    with col2:
        search = st.text_input("Search by Patient Name", placeholder="Type name...")
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Refresh", use_container_width=True):
            st.rerun()
    
    # Get filtered data
    status_arg = None if status_filter == "All" else status_filter
    requests = get_all_patient_requests(status=status_arg)
    
    if search:
        requests = [r for r in requests if search.lower() in r['patient_name'].lower()]
    
    if not requests:
        st.markdown("""
        <div class="empty-state">
            <h3>No requests found</h3>
            <p>Try adjusting your filters or load demo data.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"**{len(requests)} request(s) found**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display requests
    for req in requests:
        with st.expander(f"{req['patient_name']} — {req['category']} ({req['status'].replace('_', ' ').title()})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {req['description']}")
                st.markdown(f"**Urgency:** {req['urgency']}")
                st.markdown(f"**Language:** {req['language']}")
                if req.get('accessibility_needs'):
                    st.markdown(f"**Accessibility Needs:** {req['accessibility_needs']}")
                st.markdown(f"**Submitted:** {req['created_at']}")
                
                if req.get('processing_time_minutes'):
                    st.markdown(f"**Processing Time:** {req['processing_time_minutes']} minutes")
            
            with col2:
                st.markdown("**Status History**")
                history = get_request_history(req['id'])
                for h in history[-3:]:
                    st.markdown(f"- {h['new_status'].replace('_', ' ').title()} ({h['created_at'][:16]})")