# Demo 03 - Kubernetes CNF (Cloud Native Functions)

## Description

Cette démo présente le déploiement de CNF (Cloud Native Functions) Telco sur Kubernetes avec K3s:

- **CNF VoIP** : SIP Proxy, Media Gateway, SBC
- **5G Core** : AMF, SMF, UPF (simulés)
- **Concepts K8s** : HPA, Network Policies, PDB

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cluster K3s                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Namespace: telco-cnf                    │   │
│  │                                                      │   │
│  │   ┌─────────┐    ┌─────────────┐    ┌───────────┐  │   │
│  │   │   SBC   │───▶│  SIP Proxy  │───▶│ Media GW  │  │   │
│  │   │ (2 pods)│    │  (2 pods)   │    │ (2 pods)  │  │   │
│  │   └─────────┘    └─────────────┘    └───────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Namespace: telco-5g-core                  │   │
│  │                                                      │   │
│  │   ┌─────────┐    ┌─────────┐    ┌─────────┐        │   │
│  │   │   AMF   │    │   SMF   │    │   UPF   │        │   │
│  │   │ (2 pods)│    │ (2 pods)│    │ (2 pods)│        │   │
│  │   └─────────┘    └─────────┘    └─────────┘        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────┐              ┌─────────────┐              │
│  │ k3s-server  │              │  k3s-agent  │              │
│  │ (control)   │              │  (worker)   │              │
│  └─────────────┘              └─────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Démarrage rapide

```bash
# Démarrer le cluster K3s
docker-compose up -d

# Attendre que le cluster soit prêt (~30s)
sleep 30

# Accéder à kubectl
docker exec -it k8s-kubectl bash

# Vérifier les nodes
kubectl get nodes
```

## Accès aux services

| Service | URL/Port | Description |
|---------|----------|-------------|
| Dashboard | http://localhost:8083 | Interface de la démo |
| K8s API | https://localhost:6443 | API Kubernetes |
| Ingress HTTP | http://localhost:80 | Ingress Controller |
| Ingress HTTPS | https://localhost:443 | Ingress Controller |

## CNF déployés

### Namespace `telco-cnf`

| CNF | Description | Ports |
|-----|-------------|-------|
| cnf-sip-proxy | Proxy SIP (Kamailio) | 5060/UDP, 5061/TCP |
| cnf-media-gateway | Media Gateway (RTPEngine) | 2000/UDP |
| cnf-sbc | Session Border Controller | 5060/UDP, 5080/UDP |

### Namespace `telco-5g-core`

| NF | Description | Ports |
|----|-------------|-------|
| open5gs-amf | Access & Mobility Management | 38412/SCTP |
| open5gs-smf | Session Management | 8805/UDP |
| open5gs-upf | User Plane | 2152/UDP |

## Commandes utiles

```bash
# Accéder au container kubectl
sed -i '' 's|https://127.0.0.1:6443|https://k3s-server:6443|g' kubeconfig/kubeconfig.yaml
docker exec -it k8s-kubectl bash

# Voir tous les pods
kubectl get pods -A

# Déployer les manifests
kubectl apply -f /manifests/

# Voir les CNF
kubectl get pods -n telco-cnf -o wide

# Voir le 5G Core
kubectl get pods -n telco-5g-core

# Vérifier les HPA
kubectl get hpa -n telco-cnf

# Voir les Network Policies
kubectl get networkpolicy -n telco-cnf

# Scaler un deployment
kubectl scale deployment cnf-sip-proxy -n telco-cnf --replicas=5

# Voir les logs d'un pod
kubectl logs -n telco-cnf -l app=sip-proxy

# Rolling update
kubectl set image deployment/cnf-sbc sbc=nginx:latest -n telco-cnf
kubectl rollout status deployment/cnf-sbc -n telco-cnf

# Rollback
kubectl rollout undo deployment/cnf-sbc -n telco-cnf
```

## Concepts Kubernetes démontrés

### 1. HorizontalPodAutoscaler (HPA)
```yaml
minReplicas: 2
maxReplicas: 10
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        averageUtilization: 70
```

### 2. Network Policies
- Isolation par défaut
- Autorisation explicite du trafic SIP
- Autorisation du monitoring

### 3. PodDisruptionBudget
```yaml
minAvailable: 1  # Au moins 1 pod toujours disponible
```

### 4. Rolling Updates
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

### 5. Anti-Affinity
```yaml
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchLabels:
            app: session-border-controller
        topologyKey: kubernetes.io/hostname
```

## Fichiers manifests

- `01-namespace.yaml` - Création des namespaces
- `02-cnf-sip-proxy.yaml` - Déploiement SIP Proxy + HPA
- `03-cnf-media-gateway.yaml` - Déploiement Media Gateway + PDB
- `04-cnf-session-border.yaml` - Déploiement SBC + ConfigMap
- `05-5g-core-amf.yaml` - AMF 5G Core
- `06-5g-core-smf-upf.yaml` - SMF et UPF 5G Core
- `07-network-policies.yaml` - Politiques réseau

## Kubeconfig

Le fichier kubeconfig est généré automatiquement dans `./kubeconfig/kubeconfig.yaml`.

Pour l'utiliser depuis l'hôte:
```bash
export KUBECONFIG=$(pwd)/kubeconfig/kubeconfig.yaml
kubectl get nodes
```

## Nettoyage

```bash
docker-compose down -v
rm -rf kubeconfig/
```
