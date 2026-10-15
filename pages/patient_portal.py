"""Patient Portal Page"""
import streamlit as st
from utils.database import create_patient_request, get_patient_request

CATEGORIES = [
    "Appointment Scheduling",
    "Prescription Refill",
    "Medical Records",
    "Test Results",
    "Referral Request",
    "Insurance & Billing",
    "General Question"
]

URGENCIES = ["Routine", "Soon", "Urgent"]

LANGUAGES = {
    "en": "English",
    "es": "Español (Spanish)",
    "ar": "العربية (Arabic)",
    "zh": "中文 (Chinese)",
    "fr": "Français (French)"
}

def render_patient_portal():
    """Render the patient portal for submitting requests."""
    st.markdown('<p class="section-title">Patient Request Portal</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        Submit a new request to our care team. All fields marked with * are required.
        We typically respond within 24 hours for routine requests.
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("patient_request_form", clear_on_submit=True):
        st.markdown("### Patient Information")
        
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("Full Name *", placeholder="Enter your full name")
        with col2:
            patient_email = st.text_input("Email", placeholder="your@email.com")
        
        col1, col2 = st.columns(2)
        with col1:
            patient_phone = st.text_input("Phone", placeholder="(555) 000-0000")
        with col2:
            language = st.selectbox("Preferred Language", list(LANGUAGES.keys()), 
                                   format_func=lambda x: LANGUAGES[x])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Request Details")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Request Category *", CATEGORIES)
        with col2:
            urgency = st.selectbox("Urgency Level *", URGENCIES)
        
        description = st.text_area("Description *", 
                                  placeholder="Please describe your request in detail...",
                                  height=120)
        
        accessibility_needs = st.text_input("Accessibility Needs (optional)", 
                                           placeholder="e.g., wheelchair access, interpreter, large print")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Request", use_container_width=True)
        
        if submitted:
            if not patient_name or not category or not description:
                st.error("Please fill in all required fields (Name, Category, Description)")
            else:
                request_data = {
                    'patient_name': patient_name,
                    'patient_email': patient_email,
                    'patient_phone': patient_phone,
                    'category': category,
                    'urgency': urgency,
                    'description': description,
                    'language': language,
                    'accessibility_needs': accessibility_needs
                }
                
                try:
                    request_id = create_patient_request(request_data)
                    st.success(f"Request submitted successfully! Reference ID: {request_id}")
                    st.info("You can check the status in the Patient Requests section.")
                except Exception as e:
                    st.error(f"Error submitting request: {str(e)}")