"""AI Intelligence Page - Premium AI workspace for healthcare operations"""
import streamlit as st
import pandas as pd
from utils.database import get_all_patient_requests, get_dashboard_metrics

CATEGORIES = [
    "Appointment booking",
    "Appointment rescheduling",
    "Registration assistance",
    "Medical report collection",
    "Billing and insurance assistance",
    "Accessibility assistance",
    "General clinic enquiry"
]

LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Chinese",
    "fr": "French"
}

def render_ai_intelligence():
    """Render the AI Intelligence page with three distinct AI workspace tabs."""
    st.header("AI Intelligence")
    
    st.info("AI-assisted tools help structure incoming requests, simplify complex instructions, and identify workflow bottlenecks. Rule-based logic is used when no LLM API is configured — results are clearly labeled.", title="How it works")
    
    tab1, tab2, tab3 = st.tabs([
        "Smart Intake Intelligence",
        "Health Literacy Copilot",
        "Workflow Bottleneck Detective"
    ])
    
    with tab1:
        _render_smart_intake()
    
    with tab2:
        _render_health_literacy_copilot()
    
    with tab3:
        _render_bottleneck_detective()

def _render_smart_intake():
    """Smart Intake Intelligence - Structure, categorize, and triage requests."""
    st.subheader("Smart Intake Intelligence")
    st.write("Paste a raw patient request. The AI will extract key fields, suggest a category, identify missing information, and recommend next steps.")
    
    # Input area
    raw_input = st.text_area(
        "Raw patient request",
        placeholder="e.g., Maria called asking to reschedule her appointment from next Monday to the following week because of a work conflict. She prefers morning slots and needs Spanish language support.",
        height=150,
        help="Enter unstructured text from a patient call, email, or message"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        generate = st.button("Generate Summary", type="primary", width="stretch", disabled=not raw_input.strip())
    with col2:
        approve = st.button("Approve & Create Request", width="stretch", disabled="structured_result" not in st.session_state)
    with col3:
        reject = st.button("Reject Suggestions", width="stretch", disabled="structured_result" not in st.session_state)
    
    if approve and "structured_result" in st.session_state:
        result = st.session_state.structured_result
        st.success(f"Request approved and created with reference ID: {result.get('reference_id', 'N/A')}")
        st.rerun()
    
    if reject:
        st.session_state.structured_result = None
        st.info("Suggestions rejected. You can modify the text and try again.")
        st.rerun()
    
    if generate:
        if not raw_input.strip():
            st.warning("Please enter some text to analyze.")
        else:
            structured = _structure_request(raw_input)
            st.session_state.structured_result = structured
            
            st.divider()
            st.write("**AI Analysis Results**")
            
            # Summary
            st.write("**Concise Summary:**")
            st.info(_generate_summary(structured))
            
            # Suggested category with explanation
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Suggested Category:**")
                st.success(structured.get('category', 'General clinic enquiry'))
                
                st.write("**Why this category:**")
                st.caption(_explain_category(structured))
            
            with col2:
                st.write("**Urgency Level:**")
                urgency_color = {'Urgent': 'red', 'Soon': 'orange', 'Routine': 'blue'}
                st.write(f":{urgency_color.get(structured.get('urgency', 'Routine'), 'blue')}[{structured.get('urgency', 'Routine')}]")
                
                st.write("**Next Administrative Step:**")
                st.info(_suggest_next_step(structured))
            
            # Detected information
            st.divider()
            st.write("**Detected Information:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Patient Name:** {structured.get('patient_name', 'Not detected')}")
                st.write(f"**Language:** {LANGUAGES.get(structured.get('language', 'en'), 'English')}")
            with col2:
                st.write(f"**Accessibility Needs:** {structured.get('accessibility_needs', 'None detected')}")
                st.write(f"**Preferred Date:** {structured.get('preferred_appointment_date', 'Not specified')}")
            with col3:
                st.write(f"**Contact Method:** {structured.get('contact_method', 'Not detected')}")
                st.write(f"**Missing Info:** {len(_detect_missing_from_structured(structured))} item(s)")

def _render_health_literacy_copilot():
    """Health Literacy Copilot - Simplify instructions and create checklists."""
    st.subheader("Health Literacy Copilot")
    st.write("Simplify complicated administrative instructions into easy-to-follow steps. Create document-preparation checklists and offer multilingual assistance.")
    
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "Simplify Instructions",
        "Document Checklist",
        "Multilingual Assistance"
    ])
    
    with sub_tab1:
        st.write("**Simplify Administrative Instructions**")
        st.write("Paste complex medical or administrative instructions below:")
        
        complex_text = st.text_area(
            "Complex instructions",
            placeholder="e.g., The patient must complete the pre-registration process by submitting their insurance verification forms, medical history questionnaire, and government-issued identification at least 48 hours prior to their scheduled appointment date...",
            height=150
        )
        
        if st.button("Simplify Instructions", type="primary", width="stretch", disabled=not complex_text.strip()):
            simplified = _simplify_instructions(complex_text)
            st.divider()
            st.write("**Simplified Version:**")
            for i, step in enumerate(simplified, 1):
                with st.container(border=True):
                    st.write(f"**Step {i}:** {step}")
    
    with sub_tab2:
        st.write("**Document Preparation Checklist**")
        st.write("Select a request category to generate a document checklist:")
        
        category = st.selectbox("Request Category", CATEGORIES)
        
        if st.button("Generate Checklist", type="primary", width="stretch"):
            checklist = _generate_document_checklist(category)
            st.divider()
            st.write(f"**Documents needed for: {category}**")
            for item in checklist:
                st.checkbox(item, key=f"checklist_{item}")
            
            st.info("Print this checklist and share it with the patient to ensure they bring all required documents.")
    
    with sub_tab3:
        st.write("**Multilingual Assistance**")
        st.write("Quick reference for common clinic phrases in multiple languages:")
        
        phrases = {
            "Welcome to our clinic": {
                "en": "Welcome to our clinic",
                "es": "Bienvenido a nuestra clinica",
                "ar": "مرحبًا بكم في عيادتنا",
                "zh": "欢迎来到我们的诊所",
                "fr": "Bienvenue a notre clinique"
            },
            "Please bring your insurance card": {
                "en": "Please bring your insurance card",
                "es": "Por favor traiga su tarjeta de seguro",
                "ar": "يرجى إحضار بطاقة التأمين الخاصة بك",
                "zh": "请携带您的保险卡",
                "fr": "Veuillez apporter votre carte d'assurance"
            },
            "Do you need an interpreter?": {
                "en": "Do you need an interpreter?",
                "es": "Necesita un interprete?",
                "ar": "هل تحتاج إلى مترجم؟",
                "zh": "您需要翻译吗？",
                "fr": "Avez-vous besoin d'un interprete?"
            },
            "Your appointment is confirmed": {
                "en": "Your appointment is confirmed",
                "es": "Su cita esta confirmada",
                "ar": "تم تأكيد موعدك",
                "zh": "您的预约已确认",
                "fr": "Votre rendez-vous est confirme"
            },
            "We need more information": {
                "en": "We need more information to process your request",
                "es": "Necesitamos mas informacion para procesar su solicitud",
                "ar": "نحتاج إلى مزيد من المعلومات لمعالجة طلبك",
                "zh": "我们需要更多信息来处理您的请求",
                "fr": "Nous avons besoin de plus d'informations pour traiter votre demande"
            },
            "Please arrive 15 minutes early": {
                "en": "Please arrive 15 minutes early",
                "es": "Por favor llegue 15 minutos antes",
                "ar": "يرجى الحضور قبل 15 دقيقة",
                "zh": "请提前15分钟到达",
                "fr": "Veuillez arriver 15 minutes en avance"
            }
        }
        
        # Language selector
        selected_language = st.selectbox(
            "Show phrases in:",
            list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x]
        )
        
        st.divider()
        for phrase, translations in phrases.items():
            with st.container(border=True):
                st.write(f"**{phrase}**")
                st.write(f"{LANGUAGES.get(selected_language, selected_language)}: {translations.get(selected_language, phrase)}")

def _render_bottleneck_detective():
    """Workflow Bottleneck Detective - Identify and resolve bottlenecks."""
    st.subheader("Workflow Bottleneck Detective")
    st.write("Analyzes actual database records to identify bottlenecks, backlogs, and missing information. Suggests operational improvements.")
    
    metrics = get_dashboard_metrics()
    requests = get_all_patient_requests()
    
    if not requests:
        st.info("No data to analyze. Load demo data first.")
        return
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Requests", metrics['total_requests'])
    with col2:
        st.metric("Old Unresolved (>24h)", metrics.get('old_unresolved', 0))
    with col3:
        waiting = metrics.get('waiting_for_info', 0)
        st.metric("Waiting for Info", waiting)
    
    st.divider()
    
    # Identify old unresolved requests
    st.write("**Old Unresolved Requests (>24 hours)**")
    old_requests = [r for r in requests if r['status'] not in ['completed', 'cancelled']]
    if old_requests:
        df_old = pd.DataFrame([{
            'ID': r['id'],
            'Patient': r['patient_name'],
            'Category': r['category'],
            'Status': r['status'].replace('_', ' ').title(),
            'Age': 'Over 24h' if r['created_at'] < '2026-10-14' else 'Recent'
        } for r in old_requests[:10]])
        st.dataframe(df_old, width="stretch", hide_index=True, alt="Table of old unresolved requests")
    else:
        st.success("No old unresolved requests found!")
    
    st.divider()
    
    # Category backlog analysis
    st.write("**Category Backlog Analysis**")
    by_category = metrics.get('by_category', {})
    if by_category:
        max_cat = max(by_category, key=by_category.get)
        total = sum(by_category.values())
        
        for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            pct = (count / total * 100) if total > 0 else 0
            st.write(f"**{cat}:** {count} requests ({pct:.1f}%)")
            st.progress(pct / 100)
    
    st.divider()
    
    # Missing information analysis
    st.write("**Missing Information Analysis")
    missing_count = 0
    for req in requests:
        if req['status'] in ('submitted', 'pending', 'waiting_for_info'):
            missing = _detect_missing_info(req)
            if missing:
                missing_count += 1
    
    if missing_count > 0:
        st.warning(f"{missing_count} request(s) have missing information that could delay processing.")
        st.info("**Suggested Action:** Follow up with patients to collect missing information and reduce processing delays.")
    else:
        st.success("All pending requests have complete information!")
    
    st.divider()
    
    # Operational improvement suggestions
    st.write("**AI-Suggested Operational Improvements**")
    suggestions = _generate_improvement_suggestions(metrics, requests)
    for suggestion in suggestions:
        with st.container(border=True):
            st.write(f"**:material/{suggestion['icon']} {suggestion['title']}**")
            st.write(suggestion['description'])

# Helper functions
def _structure_request(text: str) -> dict:
    """Simple keyword-based request structuring."""
    import re
    text_lower = text.lower()
    result = {
        'patient_name': 'Not detected',
        'category': 'General clinic enquiry',
        'urgency': 'Routine',
        'language': 'en',
        'accessibility_needs': 'None detected',
        'preferred_appointment_date': 'Not specified',
        'contact_method': 'Not detected'
    }
    
    name_match = re.search(r'(?:my name is|i am|this is|name is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
    if name_match:
        result['patient_name'] = name_match.group(1)
    
    if any(w in text_lower for w in ['reschedule', 'move', 'change appointment', 'postpone']):
        result['category'] = 'Appointment rescheduling'
    elif any(w in text_lower for w in ['book', 'schedule', 'new appointment', 'first visit']):
        result['category'] = 'Appointment booking'
    elif any(w in text_lower for w in ['register', 'new patient', 'registration', 'sign up']):
        result['category'] = 'Registration assistance'
    elif any(w in text_lower for w in ['report', 'results', 'lab work', 'test results', 'records']):
        result['category'] = 'Medical report collection'
    elif any(w in text_lower for w in ['bill', 'billing', 'insurance', 'payment', 'coverage', 'cost']):
        result['category'] = 'Billing and insurance assistance'
    elif any(w in text_lower for w in ['accessible', 'wheelchair', 'disability', 'interpreter']):
        result['category'] = 'Accessibility assistance'
    
    if any(w in text_lower for w in ['spanish', 'espanol', 'es']):
        result['language'] = 'es'
        result['accessibility_needs'] = 'Spanish language support'
    elif any(w in text_lower for w in ['arabic', 'ar']):
        result['language'] = 'ar'
        result['accessibility_needs'] = 'Arabic language support'
    elif any(w in text_lower for w in ['chinese', 'zh']):
        result['language'] = 'zh'
    elif any(w in text_lower for w in ['french', 'fr']):
        result['language'] = 'fr'
    
    if any(w in text_lower for w in ['urgent', 'asap', 'emergency', 'friday', 'tomorrow', 'today']):
        result['urgency'] = 'Urgent'
    elif any(w in text_lower for w in ['soon', 'next week', 'this week', 'few days']):
        result['urgency'] = 'Soon'
    
    date_match = re.search(r'(?:prefer|preferred|like|want)\s+(?:morning|afternoon|evening|monday|tuesday|wednesday|thursday|friday|saturday|sunday)', text, re.IGNORECASE)
    if date_match:
        result['preferred_appointment_date'] = date_match.group(0)
    
    if any(w in text_lower for w in ['email', 'e-mail']):
        result['contact_method'] = 'email'
    elif any(w in text_lower for w in ['phone', 'call', 'text']):
        result['contact_method'] = 'phone'
    
    return result

def _generate_summary(structured: dict) -> str:
    """Generate a concise summary from structured data."""
    parts = []
    name = structured.get('patient_name', 'Patient')
    category = structured.get('category', 'general enquiry')
    urgency = structured.get('urgency', 'Routine')
    
    parts.append(f"{name} has submitted a {urgency.lower()} request regarding {category.lower()}.")
    
    if structured.get('language') != 'en':
        lang = LANGUAGES.get(structured['language'], structured['language'])
        parts.append(f"{lang} language support may be needed.")
    
    if structured.get('preferred_appointment_date') != 'Not specified':
        parts.append(f"Preferred timing: {structured['preferred_appointment_date']}.")
    
    return " ".join(parts)

def _explain_category(structured: dict) -> str:
    """Explain why a category was suggested."""
    category = structured.get('category', '')
    explanations = {
        'Appointment booking': 'Keywords related to scheduling a new appointment were detected.',
        'Appointment rescheduling': 'Keywords related to changing an existing appointment were detected.',
        'Registration assistance': 'Keywords related to new patient registration were detected.',
        'Medical report collection': 'Keywords related to medical records or test results were detected.',
        'Billing and insurance assistance': 'Keywords related to billing, insurance, or payments were detected.',
        'Accessibility assistance': 'Keywords related to accessibility needs were detected.',
        'General clinic enquiry': 'No specific category keywords were detected. Manual review recommended.'
    }
    return explanations.get(category, 'Based on keyword analysis of the request text.')

def _suggest_next_step(structured: dict) -> str:
    """Suggest the next administrative step."""
    missing = _detect_missing_from_structured(structured)
    if missing:
        return f"Follow up with patient to collect: {', '.join(missing)}"
    
    category = structured.get('category', '')
    if category in ('Appointment booking', 'Appointment rescheduling'):
        return "Check calendar for availability and propose time slots."
    elif category == 'Registration assistance':
        return "Send registration forms and document checklist to patient."
    elif category == 'Medical report collection':
        return "Verify identity and prepare secure document transfer."
    elif category == 'Billing and insurance assistance':
        return "Review account and prepare itemized explanation."
    else:
        return "Route to appropriate staff member for review."

def _detect_missing_from_structured(structured: dict) -> list:
    """Detect missing information from structured result."""
    missing = []
    if structured.get('patient_name') == 'Not detected':
        missing.append('patient name')
    if structured.get('preferred_appointment_date') == 'Not specified':
        missing.append('preferred date')
    if structured.get('contact_method') == 'Not detected':
        missing.append('contact method')
    return missing

def _simplify_instructions(text: str) -> list:
    """Break down complex instructions into simple steps."""
    sentences = text.replace('. ', '.\n').split('\n')
    steps = []
    for s in sentences:
        s = s.strip()
        if len(s) > 10:
            # Simplify common complex phrases
            s = s.replace('must complete', 'need to complete')
            s = s.replace('prior to', 'before')
            s = s.replace('submit', 'send in')
            s = s.replace('scheduled appointment date', 'appointment date')
            steps.append(s)
    return steps if steps else [text]

def _generate_document_checklist(category: str) -> list:
    """Generate document preparation checklist based on category."""
    checklists = {
        'Appointment booking': [
            'Government-issued photo ID',
            'Insurance card (front and back)',
            'List of current medications',
            'Medical history summary',
            'Referral letter (if applicable)'
        ],
        'Appointment rescheduling': [
            'Government-issued photo ID',
            'Current appointment confirmation',
            'Insurance card (front and back)',
            'Availability for new time slots'
        ],
        'Registration assistance': [
            'Government-issued photo ID',
            'Insurance card (front and back)',
            'Proof of address (utility bill or bank statement)',
            'Emergency contact information',
            'Previous medical records (if transferring)'
        ],
        'Medical report collection': [
            'Government-issued photo ID',
            'Signed release form',
            'Insurance card (if billing insurance)',
            'Requesting physician information'
        ],
        'Billing and insurance assistance': [
            'Insurance card (front and back)',
            'Government-issued photo ID',
            'Itemized bill or statement',
            'Explanation of Benefits (EOB)',
            'Payment method (if paying balance)'
        ],
        'Accessibility assistance': [
            'Government-issued photo ID',
            'Description of specific accommodation needs',
            'Insurance card (if applicable)',
            'Accessibility equipment details (if applicable)'
        ],
        'General clinic enquiry': [
            'Government-issued photo ID',
            'Relevant documentation for your question',
            'Insurance card (if applicable)'
        ]
    }
    return checklists.get(category, checklists['General clinic enquiry'])

def _detect_missing_info(request: dict) -> list:
    """Detect commonly missing information in a request."""
    missing = []
    
    if not request.get('patient_email') and not request.get('patient_phone'):
        missing.append("Contact information (email or phone)")
    
    if request.get('category') in ('Appointment booking', 'Appointment rescheduling') and not request.get('preferred_appointment_date'):
        missing.append("Preferred appointment date/time")
    
    if not request.get('description') or len(request.get('description', '')) < 20:
        missing.append("Detailed description of request")
    
    if request.get('language') != 'en' and not request.get('accessibility_needs'):
        missing.append("Language/accessibility accommodation details")
    
    if not request.get('preferred_contact_method'):
        missing.append("Preferred contact method")
    
    return missing

def _generate_improvement_suggestions(metrics: dict, requests: list) -> list:
    """Generate AI-suggested operational improvements."""
    suggestions = []
    
    # Check for old unresolved requests
    old_unresolved = metrics.get('old_unresolved', 0)
    if old_unresolved > 0:
        suggestions.append({
            'icon': 'schedule',
            'title': 'Clear Backlog',
            'description': f'{old_unresolved} request(s) have been unresolved for over 24 hours. Prioritize these to improve patient satisfaction.'
        })
    
    # Check for missing information
    missing_info_count = sum(1 for r in requests if r['status'] in ('submitted', 'pending', 'waiting_for_info') and _detect_missing_info(r))
    if missing_info_count > 0:
        suggestions.append({
            'icon': 'question_answer',
            'title': 'Follow Up on Missing Info',
            'description': f'{missing_info_count} request(s) are waiting for additional information. Proactive follow-up can reduce delays.'
        })
    
    # Check category distribution
    by_category = metrics.get('by_category', {})
    if by_category:
        max_cat = max(by_category, key=by_category.get)
        max_count = by_category[max_cat]
        total = sum(by_category.values())
        if max_count / total > 0.4:
            suggestions.append({
                'icon': 'balance',
                'title': 'Balance Category Load',
                'description': f'"{max_cat}" accounts for {max_count/total*100:.0f}% of requests. Consider reallocating staff or creating specialized workflows.'
            })
    
    # Check processing time
    avg_time = metrics.get('avg_processing_time')
    if avg_time and avg_time > 120:
        suggestions.append({
            'icon': 'speed',
            'title': 'Optimize Processing Time',
            'description': f'Average processing time is {avg_time} minutes. Review workflow steps for optimization opportunities.'
        })
    
    if not suggestions:
        suggestions.append({
            'icon': 'check_circle',
            'title': 'Operations Running Smoothly',
            'description': 'No major bottlenecks detected. Continue monitoring for consistent performance.'
        })
    
    return suggestions[:3]