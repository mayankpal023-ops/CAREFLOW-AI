"""Clinic Operations Page"""
import streamlit as st
from utils.database import (
    get_all_patient_requests, update_request_status, get_all_staff,
    assign_staff_to_request, get_staff_workload, create_staff
)

def render_clinic_operations():
    """Render the clinic operations dashboard."""
    st.markdown('<p class="section-title">Clinic Operations</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Process Requests", "Staff Management", "Staff Workload"])
    
    # Tab 1: Process Requests
    with tab1:
        st.markdown("### Active Requests Queue")
        
        # Get non-completed requests
        active_requests = get_all_patient_requests()
        active_requests = [r for r in active_requests if r['status'] not in ['completed', 'cancelled']]
        
        if not active_requests:
            st.markdown("""
            <div class="empty-state">
                <h3>Queue is empty</h3>
                <p>No pending requests to process.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for req in active_requests:
                with st.expander(f"{req['patient_name']} — {req['category']} ({req['status']})"):
                    col1, col2 = st.columns([3, 2])
                    
                    with col1:
                        st.markdown(f"**Description:** {req['description']}")
                        st.markdown(f"**Urgency:** {req['urgency']}")
                        st.markdown(f"**Submitted:** {req['created_at']}")
                        if req.get('assigned_staff'):
                            st.markdown(f"**Assigned to:** {req['assigned_staff']}")
                    
                    with col2:
                        st.markdown("**Actions**")
                        
                        staff_list = get_all_staff()
                        staff_options = {s['id']: f"{s['name']} ({s['role']})" for s in staff_list}
                        
                        selected_staff = st.selectbox(
                            "Assign to", 
                            list(staff_options.keys()),
                            format_func=lambda x: staff_options.get(x, "Unassigned"),
                            key=f"assign_{req['id']}"
                        )
                        
                        if st.button("Assign", key=f"btn_assign_{req['id']}"):
                            assign_staff_to_request(req['id'], selected_staff)
                            st.success(f"Assigned to {staff_options[selected_staff]}")
                            st.rerun()
                        
                        new_status = st.selectbox(
                            "Update Status",
                            ["submitted", "pending", "processing", "completed", "cancelled"],
                            key=f"status_{req['id']}"
                        )
                        
                        if st.button("Update Status", key=f"btn_status_{req['id']}"):
                            update_request_status(req['id'], new_status, "Clinic Staff")
                            st.success(f"Status updated to {new_status}")
                            st.rerun()
    
    # Tab 2: Staff Management
    with tab2:
        st.markdown("### Staff Directory")
        
        staff = get_all_staff()
        if staff:
            df = pd.DataFrame(staff)
            st.dataframe(df[['name', 'role', 'department', 'email']], use_container_width=True)
        else:
            st.info("No staff members found.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Add New Staff Member")
        
        with st.form("add_staff_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name *")
                role = st.text_input("Role *")
            with col2:
                email = st.text_input("Email")
                department = st.text_input("Department")
            
            if st.form_submit_button("Add Staff Member"):
                if name and role:
                    create_staff({'name': name, 'role': role, 'email': email, 'department': department})
                    st.success(f"Added {name} to staff directory")
                    st.rerun()
                else:
                    st.error("Name and Role are required")
    
    # Tab 3: Staff Workload
    with tab3:
        st.markdown("### Current Workload Distribution")
        
        workload = get_staff_workload()
        if workload:
            df = pd.DataFrame(workload)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No workload data available.")