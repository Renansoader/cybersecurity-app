"""Frequência de EventID no log System, últimas 24h — somente leitura.

Conta quantas vezes cada EventID aparece no log System nas últimas 24 horas.
Serve para o artefato de 4.5.q23: mostrar, com número real desta máquina, que
um EventID de alto volume (aqui, 10016 — erro de permissão DCOM, amplamente
citado como ruído de plataforma) não é sinal de ataque só por ser frequente.
"""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")


def contagem_por_eventid(log, horas=24, top=8):
    ps = (
        f"$since = (Get-Date).AddHours(-{horas}); "
        f"Get-WinEvent -FilterHashtable @{{LogName='{log}'; StartTime=$since}} "
        f"-ErrorAction SilentlyContinue | Group-Object Id | "
        f"Sort-Object Count -Descending | Select-Object -First {top} | "
        f"ForEach-Object {{ \"$($_.Name)|$($_.Count)\" }}"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                        capture_output=True, text=True)
    linhas = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    return [tuple(l.split("|")) for l in linhas]


if __name__ == "__main__":
    print("=== EventID mais frequentes no log System, últimas 24h ===")
    for event_id, contagem in contagem_por_eventid("System"):
        print(f"  EventID {event_id:<6}: {contagem} ocorrências")
