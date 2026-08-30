"""Volume de eventos e custo de retenção, a partir da máquina real.

Somente leitura. Conta eventos das últimas 24h em dois logs nativos do Windows
(System e Application — Security exige elevação, e o script não pede) e mede o
tamanho médio de um evento pela representação XML. Dali projeta o volume diário
de um parque de máquinas e o efeito de reter 90 dias contra 1 ano.

Não usa preço de nenhum fornecedor: o objetivo é mostrar que retenção multiplica
armazenamento de forma linear, não estimar uma fatura real.
"""
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")  # console do Windows usa cp850/cp1252 por padrao

LOGS = ["System", "Application"]
AMOSTRA = 300  # eventos mais recentes usados para medir o tamanho médio


def contagem_24h(log):
    """Quantidade de eventos no log nas ultimas 24h, via wevtutil (so contagem)."""
    query = "*[System[TimeCreated[timediff(@SystemTime) <= 86400000]]]"
    saida = subprocess.run(
        ["wevtutil", "qe", log, f"/q:{query}", "/c:1", "/rd:true", "/f:text"],
        capture_output=True, text=True,
    )
    # wevtutil nao tem "so contar": conta via powershell, que e mais direto e exato.
    ps = (
        f"(Get-WinEvent -FilterHashtable @{{LogName='{log}'; "
        f"StartTime=(Get-Date).AddHours(-24)}} -ErrorAction SilentlyContinue "
        f"| Measure-Object).Count"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                        capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def bytes_medio_por_evento(log):
    """Tamanho medio, em bytes, da representacao XML dos eventos mais recentes."""
    ps = (
        f"$s = Get-WinEvent -LogName '{log}' -MaxEvents {AMOSTRA}; "
        f"($s | ForEach-Object {{ $_.ToXml().Length }} | Measure-Object -Average).Average"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                        capture_output=True, text=True)
    valor = r.stdout.strip().replace(",", ".") or "0"  # locale pt-BR usa vírgula decimal
    return float(valor)


def projetar(eventos_dia_uma_maquina, bytes_por_evento, n_maquinas):
    bytes_dia = eventos_dia_uma_maquina * bytes_por_evento * n_maquinas
    gb_dia = bytes_dia / (1024 ** 3)
    return gb_dia


if __name__ == "__main__":
    total_eventos_dia = 0
    soma_bytes = 0.0
    print("=== medido nesta máquina, últimas 24h ===")
    for log in LOGS:
        n = contagem_24h(log)
        media = bytes_medio_por_evento(log)
        print(f"  {log:<12} eventos/24h={n:<6} bytes_medio/evento={media:.0f}")
        total_eventos_dia += n
        soma_bytes += n * media

    bytes_medio_geral = soma_bytes / total_eventos_dia if total_eventos_dia else 0
    print(f"\n  total: {total_eventos_dia} eventos/24h, {bytes_medio_geral:.0f} bytes/evento em média")
    print("  (Security ficou de fora: exige elevação. Costuma pesar mais que os dois somados.)")

    print("\n=== projeção para um parque de máquinas, com este perfil ===")
    for n_maquinas in (1, 100, 500, 2000):
        gb_dia = projetar(total_eventos_dia, bytes_medio_geral, n_maquinas)
        gb_90 = gb_dia * 90
        gb_365 = gb_dia * 365
        print(f"  {n_maquinas:>5} máquina(s): {gb_dia:9.3f} GB/dia · "
              f"90 dias = {gb_90:9.1f} GB · 1 ano = {gb_365:9.1f} GB "
              f"(razão {gb_365/gb_90:.2f}×)")

    print("\n  A razão 1 ano / 90 dias é sempre ~4,06× — é aritmética de calendário,")
    print("  não depende de fornecedor. O que muda de fornecedor para fornecedor é")
    print("  o preço por GB, não essa proporção.")
