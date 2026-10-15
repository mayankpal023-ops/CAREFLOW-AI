import urllib.request
import re

try:
    r = urllib.request.urlopen('http://localhost:8501')
    html = r.read().decode('utf-8', errors='ignore')
    # Check for navigation-related elements
    if 'data-testid' in html:
        # Find all data-testid elements
        elements = re.findall(r'data-testid="([^"]+)"', html)
        print('data-testid elements in page:', elements)
    else:
        print('No data-testid attributes found')
    
    # Check for specific navigation text
    if 'app' in html.lower():
        print('Found "app" text in page')
    else:
        print('"app" text NOT found in page')
    
    if 'about' in html.lower():
        print('Found "about" text in page')
    else:
        print('"about" text NOT found in page')
        
except Exception as e:
    print(f'Error: {e}')