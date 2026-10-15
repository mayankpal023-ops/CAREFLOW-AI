"""Accessibility Assistant Page"""
import streamlit as st
from utils.database import get_all_patient_requests

ACCESSIBILITY_FEATURES = [
    "Wheelchair accessible facility",
    "Sign language interpreter",
    "Large print materials",
    "Audio/Screen reader compatible",
    "Extended appointment time",
    "Transportation assistance",
    "Visual impairment support",
    "Cognitive accessibility support"
]

LANGUAGE_TRANSLATIONS = {
    "en": "English",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Chinese",
    "fr": "French"
}

def render_accessibility_assistant():
    """Render the accessibility assistant page."""
    st.markdown('<p class="section-title">Accessibility Assistant</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        This tool helps identify patients with accessibility needs and provides
        guidance for accommodation. Review pending requests for accessibility flags.
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Accessibility Needs Review", "Language Support", "Guidelines"])
    
    # Tab 1: Review accessibility needs
    with tab1:
        st.markdown("### Pending Requests with Accessibility Needs")
        
        all_requests = get_all_patient_requests()
        flagged = [r for r in all_requests if r.get('accessibility_needs')]
        
        if not flagged:
            st.markdown("""
            <div class="empty-state">
                <h3>No flagged requests</h3>
                <p>No pending requests have accessibility requirements.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for req in flagged:
                with st.expander(f"{req['patient_name']} — {req['accessibility_needs']}"):
                    st.markdown(f"**Category:** {req['category']}")
                    st.markdown(f"**Request:** {req['description']}")
                    st.markdown(f"**Status:** {req['status']}")
                    st.markdown("**Recommended Actions:**")
                    if "wheelchair" in req['accessibility_needs'].lower():
                        st.markdown("- Ensure ground-floor or elevator-accessible room")
                        st.markdown("- Verify wheelchair-accessible examination table")
                    if "interpreter" in req['accessibility_needs'].lower():
                        st.markdown("- Schedule certified interpreter for appointment")
                    if "large print" in req['accessibility_needs'].lower():
                        st.markdown("- Prepare large print versions of all documents")
                    if "screen reader" in req['accessibility_needs'].lower():
                        st.markdown("- Ensure digital forms are screen reader compatible")
                    if "spanish" in req['accessibility_needs'].lower() or "arabic" in req['accessibility_needs'].lower():
                        st.markdown(f"- Arrange {req['language']} interpreter or bilingual staff")
    
    # Tab 2: Language Support
    with tab2:
        st.markdown("### Language Support Dashboard")
        
        all_requests = get_all_patient_requests()
        
        # Count by language
        lang_counts = {}
        for r in all_requests:
            lang = r.get('language', 'en')
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        if lang_counts:
            for lang, count in sorted(lang_counts.items()):
                lang_name = LANGUAGE_TRANSLATIONS.get(lang, lang)
                st.markdown(f"**{lang_name}:** {count} request(s)")
        else:
            st.info("No language data available.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Quick Translation Guide")
        
        translations = {
            "Appointment Scheduling": {
                "es": "Programación de citas",
                "ar": "جدولة المواعيد",
                "zh": "预约安排"
            },
            "Prescription Refill": {
                "es": "Receta de recarga",
                "ar": "إعادة تعبئة الوصفة الطبية",
                "zh": "处方续药"
            },
            "Emergency": {
                "es": "Emergencia",
                "ar": "طوارئ",
                "zh": "紧急情况"
            }
        }
        
        for phrase, langs in translations.items():
            st.markdown(f"**{phrase}:**")
            for lang, translation in langs.items():
                st.markdown(f"- {LANGUAGE_TRANSLATIONS.get(lang, lang)}: {translation}")
    
    # Tab 3: Guidelines
    with tab3:
        st.markdown("### Accessibility Best Practices")
        
        st.markdown("#### Physical Accessibility")
        st.markdown("- Ensure all entrances are wheelchair accessible")
        st.markdown("- Maintain clear pathways free of obstacles")
        st.markdown("- Provide accessible restrooms on every floor")
        st.markdown("- Install proper signage with braille and high contrast")
        
        st.markdown("#### Communication Access")
        st.markdown("- Offer materials in multiple formats (print, digital, audio)")
        st.markdown("- Use plain language (6th-8th grade reading level)")
        st.markdown("- Provide qualified interpreters when requested")
        st.markdown("- Ensure digital tools meet WCAG 2.1 AA standards")
        
        st.markdown("#### Cognitive Accessibility")
        st.markdown("- Offer extended appointment times when needed")
        st.markdown("- Provide written summaries of verbal instructions")
        st.markdown("- Use visual schedules and reminders")
        st.markdown("- Allow support persons to accompany patients")