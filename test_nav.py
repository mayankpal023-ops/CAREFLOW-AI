import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title("CareFlow AI")
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Patient Portal", "Patient Requests", "Clinic Operations", 
     "Accessibility Assistant", "AI Intelligence", "Analytics", "About & Responsible AI"],
    label_visibility="collapsed"
)

page_map = {
    'Overview': 'overview',
    'Patient Portal': 'patient_portal', 
    'Patient Requests': 'patient_requests',
    'Clinic Operations': 'clinic_operations',
    'Accessibility Assistant': 'accessibility',
    'AI Intelligence': 'ai_intelligence',
    'Analytics': 'analytics',
    'About & Responsible AI': 'about'
}

selected = page_map.get(page, 'unknown')
st.sidebar.write(f"Selected: {page} -> {selected}")

# Now render the appropriate page
if page == "Overview":
    st.write("# Overview Page Content")
elif page == "Patient Portal":
    st.write("# Patient Portal Page Content")
elif page == "Patient Requests":
    st.write("# Patient Requests Page Content")
elif page == "Clinic Operations":
    st.write("# Clinic Operations Page Content")
elif page == "Accessibility Assistant":
    st.write("# Accessibility Assistant Page Content")
elif page == "AI Intelligence":
    st.write("# AI Intelligence Page Content")
elif page == "Analytics":
    st.write("# Analytics Page Content")
elif page == "About & Responsible AI":
    st.write("# About Page Content")
else:
    st.write(f"Page '{page}' selected (mapped to {selected})")
PYEOF