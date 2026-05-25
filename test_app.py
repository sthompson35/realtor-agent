from web_server import app
print('Testing Flask app...')
try:
    # Test the app context
    with app.app_context():
        print('App context works')
    print('Flask app test successful')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()