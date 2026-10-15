"""About & Responsible AI Page"""
import streamlit as st

def render_about():
    """Render the about and responsible AI page."""
    st.markdown('<p class="section-title">About & Responsible AI</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["About CareFlow AI", "Responsible AI", "Technical Details"])
    
    # Tab 1: About
    with tab1:
        st.markdown("""
        ## CareFlow AI
        
        **Tagline:** Better Access. Smarter Clinics. Faster Workflows.
        
        CareFlow AI is a healthcare operations platform designed to improve 
        patient access to care and streamline clinic administrative workflows.
        
        ### Problem Statement
        
        Healthcare administrative tasks create significant barriers:
        - Patients struggle to navigate complex appointment and referral systems
        - Clinic staff spend excessive time on repetitive administrative work
        - Language and accessibility needs often go unmet
        - No real-time visibility into operational bottlenecks
        
        ### Our Solution
        
        CareFlow AI provides:
        - A patient-friendly request portal with accessibility support
        - Real-time operational dashboard for clinic staff
        - Analytics to identify and resolve bottlenecks
        - Language support for diverse patient populations
        
        ### Key Features
        
        1. **Patient Portal** - Easy request submission with accessibility options
        2. **Operations Dashboard** - Real-time visibility into request status
        3. **Staff Management** - Workload tracking and assignment tools
        4. **Analytics** - Data-driven insights for operational improvements
        5. **Accessibility Assistant** - Tools to identify and address patient needs
        
        ### Impact Metrics
        
        - Reduced administrative processing time
        - Improved patient satisfaction through faster response times
        - Better identification of operational bottlenecks
        - Enhanced accessibility for underserved populations
        """)
    
    # Tab 2: Responsible AI
    with tab2:
        st.markdown("""
        ## Responsible AI Commitments
        
        ### Fairness & Equity
        
        - **Language Equity:** Multi-language support ensures non-English speakers 
          receive equal quality of care
        - **Accessibility First:** Built-in accessibility needs tracking ensures 
          patients with disabilities are properly accommodated
        - **Bias Monitoring:** Regular analysis of processing times across 
          demographic groups to identify disparities
        
        ### Transparency
        
        - **Clear Status Tracking:** Patients can see exactly where their request 
          stands in the process
        - **Explainable Metrics:** All analytics are derived from transparent, 
          auditable data sources
        - **No Black Box Decisions:** Human staff make all final decisions about 
          request prioritization and handling
        
        ### Privacy & Security
        
        - **Data Minimization:** Only essential patient information is collected
        - **Local Storage:** Patient data stays on local systems, not external servers
        - **Access Controls:** Only authorized staff can access patient information
        
        ### Accountability
        
        - **Audit Trail:** All status changes are logged with timestamps and staff IDs
        - **Human Oversight:** AI-assisted tools support, not replace, human judgment
        - **Error Reporting:** Clear channels for reporting issues or concerns
        
        ### Safety
        
        - **Urgent Request Flagging:** System highlights urgent cases for immediate attention
        - **Escalation Protocols:** Clear procedures for requests that exceed normal timeframes
        - **Fallback Procedures:** Manual processes available if technical systems fail
        
        ### Continuous Improvement
        
        - Regular review of system performance and user feedback
        - Ongoing accessibility audits and improvements
        - Staff training on responsible AI use
        """)
    
    # Tab 3: Technical Details
    with tab3:
        st.markdown("""
        ## Technical Architecture
        
        ### Technology Stack
        
        | Component | Technology |
        |-----------|------------|
        | Frontend | Streamlit (Python) |
        | Database | SQLite |
        | Data Processing | Pandas |
        | Visualization | Plotly |
        | Language | Python 3.9+ |
        
        ### Architecture Decisions
        
        **Why Streamlit?**
        - Rapid development for hackathon timelines
        - Native Python integration
        - Built-in responsive design
        - Easy deployment options
        
        **Why SQLite?**
        - Zero configuration required
        - File-based, no server needed
        - ACID compliant for data integrity
        - Perfect for local deployment
        
        **Why Pandas + Plotly?**
        - Industry standard for data manipulation
        - Beautiful, interactive visualizations
        - Excellent Streamlit integration
        
        ### Data Flow
        
        ```
        Patient Portal → SQLite Database → Streamlit UI
                              ↓
                    Analytics Engine
                              ↓
                    Operational Insights
        ```
        
        ### Scalability Considerations
        
        While built for local deployment, the architecture supports scaling:
        - Database can be migrated to PostgreSQL/MySQL
        - Streamlit can be deployed to Streamlit Cloud
        - Additional microservices can be added as needed
        
        ### Security Measures
        
        - Parameterized SQL queries prevent injection attacks
        - No external API calls required for core functionality
        - All data stored locally with no third-party sharing
        """)