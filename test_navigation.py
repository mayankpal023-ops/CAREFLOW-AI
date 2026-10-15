#!/usr/bin/env python
"""Test CareFlow AI navigation functionality."""
import streamlit as st

st.set_page_config(layout="wide", page_title="CareFlow AI Navigation Test")

st.sidebar.title("CareFlow AI")
st.sidebar.caption("Healthcare Access & Clinic Operations")

page_names = ["Overview", "Patient Portal", "Patient Requests", "Clinic Operations", 
              "Accessibility Assistant", "AI Intelligence", "Analytics", "About & Responsible AI"]

# Use st.radio for navigation (single system, no duplication)
page = st.sidebar.radio(
    "Navigation",
    page_names,
    label_visibility="collapsed"
)

st.sidebar.divider()

# Demo data section
st.sidebar.subheader("Demo data")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("Load Demo data", key="sidebar_load_demo"):
        st.sidebar.success("Demo data loaded")
with col2:
    if st.sidebar.button("Clear data", key="sidebar_clear_data"):
        st.sidebar.success("Data cleared")

st.sidebar.divider()

# Quick stats area
st.sidebar.subheader("Quick Stats")

# Now render the selected page - this is the critical part
st.title(f"CareFlow AI - {page}")

# Render each page based on selection
if page == "Overview":
    st.write("## Overview Dashboard")
    st.write("Operational dashboard with metrics and charts")
    st.info("This is the overview page content area.")
elif page == "Patient Portal":
    st.write("# Patient Portal")
    st.write("Patient request submission form area.")
    st.info("This is the patient portal page content area.")
elif page == "Patient Requests":
    st.write("# Patient Requests")
    st.write("Request management and search area.")
    st.info("This is the patient requests page content area.")
elif page == "Clinic Operations":
    st.write("# Clinic Operations")
    st.write("Operations dashboard area.")
    st.info("This is the clinic operations page content area.")
elif page == "Accessibility Assistant":
    st.write("# Accessibility Assistant")
    st.write("Accessibility tools and guidance area.")
    st.info("This is the accessibility assistant page content area.")
elif page == "AI Intelligence":
    st.write("# AI Intelligence")
    st.write("AI-assisted workflow insights area.")
    st.info("This is the AI intelligence page content area.")
elif page == "Analytics":
    st.write("# Analytics")
    st.write("Analytics dashboard area.")
    st.info("This is the analytics page content area.")
elif page == "About & Responsible AI":
    st.write("# About & Responsible AI")
    st.write("Project information and responsible AI commitments area.")
    st.info("This is the about page content area.")

st.sidebar.divider()
st.sidebar.success(f"Navigated to: {page}")
PYEOF