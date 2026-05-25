try:
    from web_server import app
    print('Flask app imported successfully')
    print('App routes:', len(list(app.url_map.iter_rules())))
except Exception as e:
    print(f'Import error: {e}')
    import traceback
    traceback.print_exc()