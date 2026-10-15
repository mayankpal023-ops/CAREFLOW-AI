"""Patient Portal Page"""
import streamlit as st
from utils.database import create_patient_request, get_patient_request

CATEGORIES = [
    "Appointment booking",
    "Appointment rescheduling",
    "Registration assistance",
    "Medical report collection",
    "Billing and insurance assistance",
    "Accessibility assistance",
    "General clinic enquiry"
]

URGENCIES = ["Routine", "Soon", "Urgent"]

LANGUAGES = {
    "en": "English",
    "es": "Espanol (Spanish)",
    "ar": "Arabic",
    "zh": "Chinese",
    "fr": "Francais (French)"
}

CONTACT_METHODS = ["email", "phone", "text"]

def render_patient_portal():
    """Render the patient portal for submitting requests."""
    st.header("Patient Request Portal")
    
    st.info("Submit a new request to our care team. All fields marked with * are required. We typically respond within 24 hours for routine requests.")
    
    # Reference ID lookup
    with st.expander("Check request status"):
        ref_id = st.text_input("Enter your reference ID", placeholder="e.g., ABC12345")
        if st.button("Look up request", key="lookup_btn"):
            if ref_id:
                req = get_patient_request(ref_id.upper().strip())
                if req:
                    st.success(f"Request found! Status: {req['status'].replace('_', ' ').title()}")
                    st.write(f"**Patient:** {req['patient_name']}")
                    st.write(f"**Category:** {req['category']}")
                    st.write(f"**Submitted:** {req['created_at'][:10]}")
                    st.write(f"**Description:** {req['description']}")
                else:
                    st.error("No request found with that reference ID. Please check and try again.")
            else:
                st.warning("Please enter a reference ID.")
    
    st.divider()
    
    st.subheader("Submit a new request")
    
    with st.form("patient_request_form", clear_on_submit=True):
        st.subheader("Patient Information")
        
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Full Name *", placeholder="Enter your full name", max_chars=100)
        with col2:
            preferred_contact = st.selectbox("Preferred Contact Method", CONTACT_METHODS)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            patient_email = st.text_input("Email", placeholder="your@email.com")
        with col2:
            patient_phone = st.text_input("Phone", placeholder="(555) 000-0000")
        with col3:
            language = st.selectbox("Preferred Language", list(LANGUAGES.keys()), 
                                   format_func=lambda x: LANGUAGES[x])
        
        st.write("")
        st.subheader("Request Details")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Request Category *", CATEGORIES)
        with col2:
            urgency = st.selectbox("Urgency Level *", URGENCIES)
        
        # Show date picker only for appointment-related categories
        preferred_date = ""
        if category in ("Appointment booking", "Appointment rescheduling"):
            col1, _ = st.columns(2)
            with col1:
                preferred_date = st.date_input(
                    "Preferred Appointment Date",
                    min_value=None,
                    help="Select your preferred date for this request"
                )
                preferred_date = preferred_date.strftime("%Y-%m-%d") if preferred_date else ""
        
        description = st.text_area("Description *", 
                                  placeholder="Please describe your request in detail...",
                                  height=120,
                                  max_chars=2000,
                                  help="Provide as much detail as possible to help us assist you quickly")
        
        accessibility_needs = st.text_input("Accessibility Needs (optional)", 
                                           placeholder="e.g., wheelchair access, interpreter, large print materials")
        
        st.write("")
        submitted = st.form_submit_button("Submit Request", type="primary")
        
        if submitted:
            # Validation
            errors = []
            if not patient_name or len(patient_name.strip()) < 2:
                errors.append("Please enter your full name (at least 2 characters)")
            if not description or len(description.strip()) < 10:
                errors.append("Please provide a description (at least 10 characters)")
            if not patient_email and not patient_phone:
                errors.append("Please provide either an email or phone number for contact")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                request_data = {
                    'patient_name': patient_name.strip(),
                    'patient_email': patient_email.strip() if patient_email else '',
                    'patient_phone': patient_phone.strip() if patient_phone else '',
                    'preferred_contact_method': preferred_contact,
                    'category': category,
                    'urgency': urgency,
                    'description': description.strip(),
                    'preferred_appointment_date': preferred_date,
                    'language': language,
                    'accessibility_needs': accessibility_needs.strip() if accessibility_needs else ''
                }
                
                try:
                    request_id = create_patient_request(request_data)
                    st.success(f"Request submitted successfully!")
                    st.info(f"**Your reference ID: {request_id}**\n\nPlease save this ID to check your status later.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error submitting request: {str(e)}")
                
                # Invalidate cached metrics so dashboard updates immediately
                try:
                    from app import cached_metrics
                    cached_metrics.clear()
                except Exception:
                    pass