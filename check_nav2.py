import urllib.request
import re

try:
    r = urllib.request.urlopen('http://localhost:8501')
    html = r.read().decode('utf-8', errors='ignore')
    
    # Find all occurrences of "app" with context
    matches = re.findall(r'.{0,50}app.{0,50}', html, re.IGNORECASE)
    print('Occurrences of "app" in page (with context):')
    for m in matches[:10]:
        print(f'  ...{m}...')
    
    print()
    
except Exception as e:
    print(f'Error: {e}')