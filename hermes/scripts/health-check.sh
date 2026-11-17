#!/bin/bash
# Health check - BRANDON AI services
# À lancer pour vérifier l'état de santé du système

echo "=== SANTÉ BRANDON AI ==="
echo "Date: $(date)"
echo ""

echo "--- Services système ---"
for svc in postgresql@16-main fail2ban crowdsec cron; do
    status=$(systemctl is-active "$svc" 2>/dev/null)
    echo "  $svc: $status"
done

echo ""
echo "--- Ports critiques ---"
for port in 5678 4000 9119 8080 5679; do
    if ss -tlnp | grep -q ":$port "; then
        echo "  Port $port: ✅ ÉCOUTE"
    else
        echo "  Port $port: ❌ FERMÉ"
    fi
done

echo ""
echo "--- RAM ---"
free -h | grep Mem | awk '{print "  Utilisée: "$3" / "$2}'

echo ""
echo "--- Disque ---"
df -h / /srv/data 2>/dev/null | grep -v tmpfs | tail -2 | awk '{print "  "$1": "$5" plein ("$4" libres)"}'

echo ""
echo "--- Uptime ---"
uptime | awk '{print "  "$3" "$4" "$5}'