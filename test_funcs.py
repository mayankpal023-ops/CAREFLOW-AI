import pages.overview as ov
import pages.patient_portal as pp
import pages.patient_requests as pr
import pages.clinic_operations as co
import pages.accessibility as ac
import pages.ai_intelligence as ai
import pages.analytics as an
import pages.about as ab

print("Page render function check:")
all_ok = True
functions = [
    ('overview', hasattr(ov, 'render_overview')),
    ('patient_portal', hasattr(pp, 'render_patient_portal')),
    ('patient_requests', hasattr(pr, 'render_patient_requests')),
    ('clinic_operations', hasattr(co, 'render_clinic_operations')),
    ('accessibility', hasattr(ac, 'render_accessibility_assistant')),
    ('ai_intelligence', hasattr(ai, 'render_ai_intelligence')),
    ('analytics', hasattr(an, 'render_analytics')),
    ('about', hasattr(ab, 'render_about')),
]

for name, ok in functions:
    status = "OK" if ok else "MISSING"
    if not ok:
        all_ok = False
    print(f"  {name:25s} - {status}")

print(f"\nAll functions present: {all_ok}")