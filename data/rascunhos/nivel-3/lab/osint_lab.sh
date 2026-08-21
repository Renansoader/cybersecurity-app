#!/bin/sh
# Laboratorio passivo — SO contra nomes reservados para documentacao (RFC 2606).
# example.com e reservado pela IANA; .invalid nunca resolve. Nenhuma varredura.
echo "=== 1. consulta DNS por tipo (example.com, dominio reservado RFC 2606) ==="
for tipo in A MX TXT NS; do
  echo "--- $tipo"
  nslookup -type=$tipo example.com 8.8.8.8 2>/dev/null | sed -n '4,12p'
done
echo
echo "=== 2. nome que nao existe (.invalid, reservado RFC 2606) ==="
nslookup -type=A intranet.nao-existe.invalid 8.8.8.8 2>/dev/null | sed -n '3,8p'
echo
echo "=== 3. whois do dominio reservado ==="
whois example.com 2>/dev/null | grep -iE "^(domain name|registrar|creation date|updated date|name server|registrant organization):" | head -10
