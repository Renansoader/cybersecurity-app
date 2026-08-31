"""Caça sem hipótese acha padrão à toa — demonstração real, não simulada.

Somente leitura. Conta eventos reais do log System desta máquina, agrupados
por hora, nas últimas 48h. Mostra que SEMPRE existe uma "hora mais
movimentada" em qualquer recorte de dado — isso é aritmética (pombos e
casas), não descoberta. Quem caça sem hipótese declarada antes tende a
apontar essa hora como "suspeita" só porque ela existe, e ela sempre existe.
"""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")


def contagem_por_hora(log, horas=48):
    ps = (
        f"$since = (Get-Date).AddHours(-{horas}); "
        f"Get-WinEvent -FilterHashtable @{{LogName='{log}'; StartTime=$since}} "
        f"-ErrorAction SilentlyContinue | "
        f"Group-Object {{ $_.TimeCreated.ToString('yyyy-MM-dd HH:00') }} | "
        f"Sort-Object Name | ForEach-Object {{ \"$($_.Name)|$($_.Count)\" }}"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                        capture_output=True, text=True)
    linhas = [l.strip() for l in r.stdout.splitlines() if l.strip()]
    return [(h, int(c)) for h, c in (l.split("|", 1) for l in linhas)]


if __name__ == "__main__":
    dados = contagem_por_hora("System")
    if not dados:
        print("sem eventos suficientes na janela de 48h")
        sys.exit(0)

    media = sum(c for _, c in dados) / len(dados)
    pico_hora, pico_n = max(dados, key=lambda x: x[1])

    print(f"=== eventos do log System por hora, últimas 48h ({len(dados)} horas com dado) ===")
    for hora, n in dados:
        marca = "  <-- a mais movimentada" if hora == pico_hora else ""
        print(f"  {hora}  {n:>4} eventos{marca}")

    print(f"\nmédia por hora: {media:.1f}")
    print(f"hora mais movimentada: {pico_hora}, com {pico_n} eventos ({pico_n/media:.1f}x a média)")
    print("\nEssa hora seria 'a mais movimentada' MESMO que todo o tráfego fosse")
    print("inteiramente normal: em qualquer lista de números, um deles é o maior.")
    print("Apontar para ela sem uma hipótese declarada antes não é achado — é o")
    print("resultado garantido de perguntar 'qual é o pico?' depois de já ter os dados.")
