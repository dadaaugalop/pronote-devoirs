#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur Flask pour lancer le script pronote_devoirs_all.py depuis l'iPhone
"""

from flask import Flask, jsonify
import subprocess
from datetime import datetime

app = Flask(__name__)

@app.route('/devoirs', methods=['GET'])
def lancer_devoirs():
    """Lance le script pronote_devoirs_all.py"""
    try:
        print(f"[{datetime.now()}] Lancement du script depuis l'iPhone...")
        result = subprocess.run(
            ['/usr/bin/python3', '/Users/user/Pronote_Devoirs/pronote_devoirs_all.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return jsonify({
                "status": "success",
                "message": "Devoirs envoyés avec succès !",
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Erreur : {result.stderr}",
                "timestamp": datetime.now().isoformat()
            }), 500
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur critique : {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Vérifie que le serveur est actif"""
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
