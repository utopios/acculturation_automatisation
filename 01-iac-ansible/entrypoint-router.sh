#!/bin/bash
# Entrypoint pour le routeur simulé

# Création de la config initiale
cat > /etc/router/system.conf << EOF
# Configuration système du routeur
HOSTNAME=${HOSTNAME}
ROUTER_ID=${ROUTER_ID:-00}
ROUTER_TYPE=${ROUTER_TYPE:-unknown}
MANAGEMENT_IP=$(hostname -i)
CREATED_AT=$(date -Iseconds)
CONFIG_VERSION=1.0
EOF

# Config réseau initiale (vide - à remplir par Ansible)
echo "# Interfaces - À configurer" > /etc/router/interfaces/config.conf
echo "# VLANs - À configurer" > /etc/router/vlans/config.conf
echo "# ACL - À configurer" > /etc/router/acl/config.conf
echo "# QoS - À configurer" > /etc/router/qos/config.conf
echo "# Routing - À configurer" > /etc/router/routing/config.conf

echo "Router ${HOSTNAME} (${ROUTER_TYPE}) démarré - IP: $(hostname -i)"

exec "$@"
