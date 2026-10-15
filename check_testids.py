import re

with open('app.py', 'r') as f:
    content = f.read()
    elements = re.findall(r'data-testid="([^"]+)"', content)
    print('data-testid elements in app.py:', elements)