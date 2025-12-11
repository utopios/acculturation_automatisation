#!/bin/bash
# Script de simulation de commandes router

case "$1" in
    show-config)
        echo "=== Configuration actuelle ==="
        for f in /etc/router/*/*.conf; do
            echo "--- $f ---"
            cat "$f"
            echo ""
        done
        ;;
    show-vlans)
        cat /etc/router/vlans/config.conf
        ;;
    show-interfaces)
        cat /etc/router/interfaces/config.conf
        ;;
    show-qos)
        cat /etc/router/qos/config.conf
        ;;
    show-routing)
        cat /etc/router/routing/config.conf
        ;;
    *)
        echo "Usage: router-config.sh {show-config|show-vlans|show-interfaces|show-qos|show-routing}"
        exit 1
        ;;
esac
