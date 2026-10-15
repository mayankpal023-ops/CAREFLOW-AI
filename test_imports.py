import importlib
import sys

pages = [
    'overview',
    'patient_portal', 
    'patient_requests',
    'clinic_operations',
    'accessibility',
    'ai_intelligence',
    'analytics',
    'about',
]

print("Testing page imports:")
print("=" * 50)

for page in pages:
    try:
        mod = importlib.import_module(f'pages.{page}')
        print(f'  OK {page:25s} - imported successfully')
    except Exception as e:
        print(f'  ERROR {page:25s} - {e}')

print("\nAll page imports tested.")