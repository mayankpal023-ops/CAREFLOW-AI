"""Accessibility Assistant Page"""
import streamlit as st
from utils.database import get_all_patient_requests

LANGUAGE_TRANSLATIONS = {
    "en": "English",
    "es": "Spanish",
    "ar": "Arabic",
    "zh": "Chinese",
    "fr": "French"
}

def render_accessibility_assistant():
    """Render the accessibility assistant page."""
    st.header("Accessibility Assistant")
    
    st.info("This tool helps identify patients with accessibility needs and provides guidance for accommodation. Review pending requests for accessibility flags.")
    
    tab1, tab2, tab3 = st.tabs(["Accessibility Needs Review", "Language Support", "Guidelines"])
    
    # Tab 1: Review accessibility needs
    with tab1:
        st.subheader("Pending Requests with Accessibility Needs")
        
        all_requests = get_all_patient_requests()
        flagged = [r for r in all_requests if r.get('accessibility_needs')]
        
        if not flagged:
            st.info("No flagged requests. No pending requests have accessibility requirements.")
        else:
            for req in flagged:
                with st.expander(f"{req['patient_name']} — {req['accessibility_needs']}"):
                    st.write(f"**Category:** {req['category']}")
                    st.write(f"**Request:** {req['description']}")
                    st.write(f"**Status:** {req['status'].replace('_', ' ').title()}")
                    st.write("**Recommended Actions:**")
                    if "wheelchair" in req['accessibility_needs'].lower():
                        st.write("- Ensure ground-floor or elevator-accessible room")
                        st.write("- Verify wheelchair-accessible examination table")
                    if "interpreter" in req['accessibility_needs'].lower() or "language support" in req['accessibility_needs'].lower():
                        st.write("- Schedule certified interpreter for appointment")
                        st.write("- Prepare translated materials")
                    if "large print" in req['accessibility_needs'].lower():
                        st.write("- Prepare large print versions of all documents")
                    if "screen reader" in req['accessibility_needs'].lower():
                        st.write("- Ensure digital forms are screen reader compatible")
                    if "spanish" in req['accessibility_needs'].lower() or req.get('language') == 'es':
                        st.write("- Arrange Spanish interpreter or bilingual staff")
                    if "arabic" in req['accessibility_needs'].lower() or req.get('language') == 'ar':
                        st.write("- Arrange Arabic interpreter or bilingual staff")
                    if "visual" in req['accessibility_needs'].lower() or "audio" in req['accessibility_needs'].lower():
                        st.write("- Provide audio instructions and visual aids")
    
    # Tab 2: Language Support
    with tab2:
        st.subheader("Language Support Dashboard")
        
        all_requests = get_all_patient_requests()
        
        # Count by language
        lang_counts = {}
        for r in all_requests:
            lang = r.get('language', 'en')
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        if lang_counts:
            cols = st.columns(len(lang_counts))
            for i, (lang, count) in enumerate(sorted(lang_counts.items())):
                with cols[i]:
                    lang_name = LANGUAGE_TRANSLATIONS.get(lang, lang)
                    st.metric(lang_name, count)
        else:
            st.info("No language data available.")
        
        st.write("")
        st.subheader("Quick Translation Guide")
        
        translations = {
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
            }
        }
        
        for phrase, langs in translations.items():
            with st.container(border=True):
                st.write(f"**{phrase}**")
                cols = st.columns(len(langs))
                for i, (lang, translation) in enumerate(langs.items()):
                    with cols[i]:
                        st.caption(f"**{LANGUAGE_TRANSLATIONS.get(lang, lang)}:** {translation}")
    
    # Tab 3: Guidelines
    with tab3:
        st.subheader("Accessibility Best Practices")
        
        st.write("**Physical Accessibility**")
        st.write("- Ensure all entrances are wheelchair accessible")
        st.write("- Maintain clear pathways free of obstacles")
        st.write("- Provide accessible restrooms on every floor")
        st.write("- Install proper signage with braille and high contrast")
        
        st.write("**Communication Access**")
        st.write("- Offer materials in multiple formats (print, digital, audio)")
        st.write("- Use plain language (6th-8th grade reading level)")
        st.write("- Provide qualified interpreters when requested")
        st.write("- Ensure digital tools meet WCAG 2.1 AA standards")
        
        st.write("**Cognitive Accessibility**")
        st.write("- Offer extended appointment times when needed")
        st.write("- Provide written summaries of verbal instructions")
        st.write("- Use visual schedules and reminders")
        st.write("- Allow support persons to accompany patients")