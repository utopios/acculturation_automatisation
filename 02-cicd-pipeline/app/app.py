#!/usr/bin/env python3
"""
API de Provisionnement Telco - Demo CI/CD
Formation Automatisation Telco
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
import os
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
ENV = os.getenv('ENV', 'development')
APP_NAME = os.getenv('APP_NAME', 'telco-provisioning')
VERSION = os.getenv('APP_VERSION', '1.0.0')

# Simulation de base de données en mémoire
services_db = {}
provisioning_queue = []

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template('index.html',
                         env=ENV,
                         version=VERSION,
                         app_name=APP_NAME)

@app.route('/health')
def health():
    """Health check pour le pipeline CI/CD"""
    return jsonify({
        'status': 'healthy',
        'environment': ENV,
        'version': VERSION,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/info')
def info():
    """Informations sur l'application"""
    return jsonify({
        'app_name': APP_NAME,
        'version': VERSION,
        'environment': ENV,
        'features': [
            'VoIP Provisioning',
            'SIP Trunk Management',
            'Number Allocation',
            'QoS Configuration'
        ],
        'uptime': 'demo-mode'
    })

@app.route('/api/provision', methods=['POST'])
def provision_service():
    """
    Provisionnement d'un nouveau service VoIP

    Body JSON attendu:
    {
        "customer_id": "CUST-123",
        "service_type": "SIP_TRUNK",
        "channels": 30,
        "did_range_start": "+33155550000",
        "did_count": 30
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validation
    required_fields = ['customer_id', 'service_type']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # Création du service
    service_id = f"SVC-{uuid.uuid4().hex[:8].upper()}"
    service = {
        'service_id': service_id,
        'customer_id': data['customer_id'],
        'service_type': data['service_type'],
        'channels': data.get('channels', 10),
        'did_range_start': data.get('did_range_start', '+33100000000'),
        'did_count': data.get('did_count', 10),
        'status': 'provisioning',
        'created_at': datetime.now().isoformat(),
        'environment': ENV
    }

    services_db[service_id] = service
    provisioning_queue.append(service_id)

    # Simulation du provisionnement
    service['status'] = 'active'
    service['provisioned_at'] = datetime.now().isoformat()

    return jsonify({
        'message': 'Service provisioned successfully',
        'service': service
    }), 201

@app.route('/api/services')
def list_services():
    """Liste tous les services provisionnés"""
    return jsonify({
        'count': len(services_db),
        'services': list(services_db.values())
    })

@app.route('/api/services/<service_id>')
def get_service(service_id):
    """Récupère un service par son ID"""
    if service_id not in services_db:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify(services_db[service_id])

@app.route('/api/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Supprime (déprovisionne) un service"""
    if service_id not in services_db:
        return jsonify({'error': 'Service not found'}), 404

    service = services_db.pop(service_id)
    return jsonify({
        'message': 'Service deprovisioned',
        'service_id': service_id
    })

@app.route('/api/test')
def test_endpoint():
    """Endpoint de test pour les tests d'intégration"""
    return jsonify({
        'test': 'passed',
        'environment': ENV,
        'timestamp': datetime.now().isoformat()
    })

# Endpoint spécifique pour démontrer le canary deployment
@app.route('/api/version')
def get_version():
    """Retourne la version pour le canary deployment"""
    return jsonify({
        'version': VERSION,
        'environment': ENV,
        'canary': os.getenv('CANARY', 'false')
    })

if __name__ == '__main__':
    print(f"""
    ╔════════════════════════════════════════════╗
    ║  🚀 Telco Provisioning API                 ║
    ╠════════════════════════════════════════════╣
    ║  Environment: {ENV:<28} ║
    ║  Version: {VERSION:<32} ║
    ╚════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=8080, debug=(ENV == 'development'))
