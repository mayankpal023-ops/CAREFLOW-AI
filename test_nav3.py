import streamlit as st

st.set_page_config(layout='wide', page_title='Nav Test')

# Simulate the app navigation logic
if 'page' not in st.session_state:
    st.session_state.page = 'Overview'

page_names = ['Overview', 'Patient Portal', 'Patient Requests', 'Clinic Operations', 
              'Accessibility Assistant', 'AI Intelligence', 'Analytics', 'About & Responsible AI']

# Simulate radio selection
selected_page = st.sidebar.radio(
    'Navigation', 
    page_names, 
    index=page_names.index(st.session_state.page), 
    label_visibility='collapsed'
)

# Only update if changed
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

# Display the selected page
st.title(f"CareFlow AI - {st.session_state.page}")

# Render the appropriate page
if st.session_state.page == 'Overview':
    st.write("## Overview Page Content")
    st.write("This is the overview dashboard.")
elif st.session_state.page == 'Patient Portal':
    st.write("## Patient Portal Page Content")
elif st.session_state.page == 'Patient Requests':
    st.write("## Patient Requests Page Content")
elif st.session_state.page == 'Clinic Operations':
    st.write("## Clinic Operations Page Content")
elif st.session_state.page == 'Accessibility Assistant':
    st.write("## Accessibility Assistant Page Content")
elif st.session_state.page == 'AI Intelligence':
    st.write("## AI Intelligence Page Content")
elif st.session_state.page == 'Analytics':
    st.write("## Analytics Page Content")
elif st.session_state.page == 'About & Responsible AI':
    st.write("## About Page Content")

st.sidebar.success(f"Now on: {st.session_state.page}")