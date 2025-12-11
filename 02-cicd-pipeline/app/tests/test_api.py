"""
Tests unitaires pour l'API Telco Provisioning
Formation Automatisation Telco
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestHealthEndpoint:
    """Tests pour l'endpoint /health"""

    def test_health_returns_200(self, client):
        """Le health check doit retourner 200"""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_status_healthy(self, client):
        """Le health check doit retourner status: healthy"""
        response = client.get('/health')
        data = response.get_json()
        assert data['status'] == 'healthy'

    def test_health_contains_version(self, client):
        """Le health check doit contenir la version"""
        response = client.get('/health')
        data = response.get_json()
        assert 'version' in data


class TestProvisioningEndpoint:
    """Tests pour l'endpoint /api/provision"""

    def test_provision_voip_success(self, client):
        """Le provisioning VoIP doit réussir"""
        payload = {
            "service_type": "voip",
            "customer_id": "TEST001",
            "parameters": {
                "codec": "G.711",
                "max_channels": 10
            }
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'provisioned'
        assert data['service_type'] == 'voip'

    def test_provision_internet_success(self, client):
        """Le provisioning Internet doit réussir"""
        payload = {
            "service_type": "internet",
            "customer_id": "TEST002",
            "parameters": {
                "bandwidth": "100Mbps",
                "ip_type": "dynamic"
            }
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'provisioned'

    def test_provision_mobile_success(self, client):
        """Le provisioning Mobile doit réussir"""
        payload = {
            "service_type": "mobile",
            "customer_id": "TEST003",
            "parameters": {
                "plan": "5G_unlimited",
                "sim_type": "esim"
            }
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 200

    def test_provision_missing_service_type(self, client):
        """Doit échouer si service_type manquant"""
        payload = {
            "customer_id": "TEST004"
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_provision_missing_customer_id(self, client):
        """Doit échouer si customer_id manquant"""
        payload = {
            "service_type": "voip"
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 400

    def test_provision_invalid_service_type(self, client):
        """Doit échouer si service_type invalide"""
        payload = {
            "service_type": "invalid_service",
            "customer_id": "TEST005"
        }
        response = client.post('/api/provision', json=payload)
        assert response.status_code == 400


class TestServicesEndpoint:
    """Tests pour l'endpoint /api/services"""

    def test_get_services_returns_list(self, client):
        """Doit retourner une liste de services"""
        response = client.get('/api/services')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    def test_get_services_contains_voip(self, client):
        """La liste doit contenir le service VoIP"""
        response = client.get('/api/services')
        data = response.get_json()
        service_types = [s['type'] for s in data]
        assert 'voip' in service_types


class TestCustomerEndpoint:
    """Tests pour les endpoints customer"""

    def test_get_customer_services(self, client):
        """Doit retourner les services d'un client"""
        # D'abord provisionner un service
        payload = {
            "service_type": "voip",
            "customer_id": "CUST001"
        }
        client.post('/api/provision', json=payload)

        # Puis récupérer les services du client
        response = client.get('/api/customer/CUST001/services')
        assert response.status_code == 200

    def test_get_unknown_customer(self, client):
        """Doit retourner 404 pour un client inconnu"""
        response = client.get('/api/customer/UNKNOWN/services')
        assert response.status_code == 404


class TestMetricsEndpoint:
    """Tests pour l'endpoint /metrics"""

    def test_metrics_returns_200(self, client):
        """Les métriques doivent être accessibles"""
        response = client.get('/metrics')
        assert response.status_code == 200

    def test_metrics_contains_requests_total(self, client):
        """Les métriques doivent contenir requests_total"""
        response = client.get('/metrics')
        data = response.get_json()
        assert 'requests_total' in data


# Fixtures pytest
@pytest.fixture
def app():
    """Créer l'application de test"""
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    """Créer le client de test"""
    return app.test_client()
