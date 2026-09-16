#!/usr/bin/env python3
import subprocess
import os
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}, 200

@app.route('/devoirs', methods=['GET'])
def devoirs():
    try:
        script_path = os.path.join(os.path.dirname(__file__), 'pronote_devoirs_all.py')
        
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Capture TOUT (stdout + stderr)
        output = result.stdout + result.stderr
        
        if result.returncode == 0:
            return {
                'message': 'Devoirs envoyés avec succès',
                'output': output,
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }, 200
        else:
            return {
                'message': f'Erreur (code {result.returncode})',
                'output': output,
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }, 500
    
    except Exception as e:
        import traceback
        return {
            'message': f'Exception : {str(e)}',
            'traceback': traceback.format_exc(),
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
