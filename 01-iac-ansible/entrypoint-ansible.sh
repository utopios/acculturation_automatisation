#!/bin/bash
# Entrypoint pour le contrôleur Ansible

echo "============================================"
echo "  🎮 DEMO ANSIBLE - Formation Telco"
echo "============================================"
echo ""
echo "Attente du démarrage des routeurs..."
sleep 5

# Test de connectivité
echo "Test de connectivité vers les routeurs..."
for host in router-01 router-02 router-03; do
    until nc -z $host 22 2>/dev/null; do
        echo "  Attente de $host..."
        sleep 2
    done
    echo "  ✅ $host accessible"
done

echo ""
echo "============================================"
echo "  Commandes disponibles :"
echo "============================================"
echo ""
echo "  1. Voir l'inventaire :"
echo "     ansible-inventory --list -i /ansible/inventory/"
echo ""
echo "  2. Ping tous les routeurs :"
echo "     ansible all -m ping -i /ansible/inventory/"
echo ""
echo "  3. Configurer les VLANs VoIP :"
echo "     ansible-playbook /ansible/playbooks/01-configure-vlans.yml"
echo ""
echo "  4. Configurer la QoS Telco :"
echo "     ansible-playbook /ansible/playbooks/02-configure-qos.yml"
echo ""
echo "  5. Déployer config complète :"
echo "     ansible-playbook /ansible/playbooks/03-full-config.yml"
echo ""
echo "  6. Vérifier les configs :"
echo "     ansible-playbook /ansible/playbooks/04-verify-config.yml"
echo ""
echo "============================================"

exec "$@"
