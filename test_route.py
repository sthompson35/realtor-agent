import requests

try:
    response = requests.get('http://localhost:5001/toolkit-dashboard')
    print(f'Status: {response.status_code}')
    print(f'Content length: {len(response.text)}')
    print('First 200 chars:', response.text[:200])
except Exception as e:
    print(f'Error: {e}')