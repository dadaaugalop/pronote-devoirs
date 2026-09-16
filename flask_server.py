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
        # Utilise le chemin relatif pour Render
        script_path = os.path.join(os.path.dirname(__file__), 'pronote_devoirs_all.py')
        
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return {
                'message': 'Devoirs envoyés avec succès',
                'status': 'success',
                'timestamp': datetime.now().isoformat()
            }, 200
        else:
            return {
                'message': f'Erreur : {result.stderr}',
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }, 500
    
    except subprocess.TimeoutExpired:
        return {
            'message': 'Timeout : le script a pris trop de temps',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }, 500
    
    except Exception as e:
        return {
            'message': f'Erreur : {str(e)}',
            'status': 'error',
            'timestamp': datetime.now().isoformat()
        }, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
