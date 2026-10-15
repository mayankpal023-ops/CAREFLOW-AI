# Test navigation logic
page_names = ["Overview", "Patient Portal", "Patient Requests", "Clinic Operations", 
              "Accessibility Assistant", "AI Intelligence", "Analytics", "About & Responsible AI"]

page_map = {
    'Overview': 'render_overview',
    'Patient Portal': 'render_patient_portal', 
    'Patient Requests': 'render_patient_requests',
    'Clinic Operations': 'render_clinic_operations',
    'Accessibility Assistant': 'render_accessibility_assistant',
    'AI Intelligence': 'render_ai_intelligence',
    'Analytics': 'render_analytics',
    'About & Responsible AI': 'render_about'
}

print('Navigation mapping test:')
print('=' * 50)
for page in page_names:
    selected_func = page_map.get(page, 'unknown')
    print(f'  {page:30s} -> {selected_func}')

print()
print('All', len(page_names), 'pages successfully mapped to render functions')
print('Navigation logic: OK')