"""Mapear comportamento real para técnica — artefato antes do nome.

Somente leitura: lista autostart (Win32_StartupCommand) e tarefas agendadas
ativas desta máquina, via WMI/CIM nativo do Windows. Nenhum programa é
iniciado, parado ou alterado.

O ponto do módulo: um binário rodando de %LocalAppData% via chave de
execução automática, com um "Update.exe" genérico no nome, tem a MESMA forma
de superfície que um padrão de persistência conhecido (T1547.001 no
vocabulário do MITRE ATT&CK) — mas nesta máquina real, pelo menos uma
entrada assim é o atualizador legítimo de um aplicativo de uso diário.
Decidir o nome da técnica exige olhar o procedimento (que binário, assinado
por quem, chamado como), não só a forma do artefato.
"""
import getpass
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")


def autostart():
    ps = (
        "Get-CimInstance Win32_StartupCommand | "
        "Select-Object Name, Command, Location | "
        "ForEach-Object { \"$($_.Name)|$($_.Command)|$($_.Location)\" }"
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                        capture_output=True, text=True)
    return [l.strip() for l in r.stdout.splitlines() if l.strip()]


def anonimizar(linha, usuario_real):
    return linha.replace(usuario_real, "ana.silva")


if __name__ == "__main__":
    usuario_real = getpass.getuser()
    print("=== autostart real desta máquina (Win32_StartupCommand) ===")
    for linha in autostart():
        nome, comando, local = linha.split("|", 2)
        comando = anonimizar(comando, usuario_real)
        origem_appdata = "AppData\\Local" in comando or "AppData\\Roaming" in comando
        marca = "  [binário roda de dentro do perfil do usuário]" if origem_appdata else ""
        print(f"  {nome:<45} {comando}{marca}")
