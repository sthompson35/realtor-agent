import os
from flask import Flask, render_template

app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), 'web', 'templates'),
            static_folder=os.path.join(os.getcwd(), 'web', 'static'))

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

if __name__ == '__main__':
    print('Starting simple analytics test server...')
    app.run(port=5002, debug=False)