# -*- coding: utf-8 -*-
"""Laboratorio 3.9 -- o nome da rede nao e prova de identidade.

Nao captura trafego nenhum, nao ataca rede de terceiro, nao usa ferramenta
de rede sem fio: e uma simulacao local, em memoria, de duas coisas que
QUALQUER equipamento pode transmitir de graca (o nome/SSID e o endereco
MAC) contra uma coisa que so quem conhece o segredo consegue produzir (uma
resposta de desafio calculada com HMAC). Objetivo: mostrar que copiar a
identidade visivel de uma rede e trivial, e que so uma prova criptografica
mutua fecha essa lacuna -- nao "desconfiar do nome".

Roda com: python identidade_de_rede_e_copiavel.py
"""

import hmac
import hashlib
import secrets


class PontoDeAcesso:
    def __init__(self, nome_visivel, segredo=None):
        self.nome_visivel = nome_visivel
        self.segredo = segredo  # None = impostor, nao conhece o segredo real

    def transmitir_beacon(self):
        # Qualquer equipamento pode transmitir qualquer nome. Isso e dado
        # publico, nao prova nada sobre quem esta do outro lado.
        return {"nome": self.nome_visivel}

    def responder_desafio(self, desafio):
        if self.segredo is None:
            # Impostor: nao tem o segredo, so pode responder algo aleatorio
            return secrets.token_hex(32)
        return hmac.new(self.segredo, desafio, hashlib.sha256).hexdigest()


def cliente_confia_so_no_nome(rede_conhecida_nome, candidatos):
    """Comportamento ingenuo: conecta na primeira rede com o nome certo,
    sem checar mais nada."""
    for ap in candidatos:
        if ap.transmitir_beacon()["nome"] == rede_conhecida_nome:
            return ap
    return None


def cliente_exige_prova_mutua(segredo_esperado, candidatos):
    """Comportamento correto: desafia cada candidato e so aceita quem
    produz a resposta certa para o segredo que o cliente tambem conhece."""
    desafio = secrets.token_bytes(16)
    resposta_certa = hmac.new(segredo_esperado, desafio, hashlib.sha256).hexdigest()
    for ap in candidatos:
        if ap.transmitir_beacon()["nome"] != "CafeCentral-WiFi":
            continue
        resposta = ap.responder_desafio(desafio)
        if hmac.compare_digest(resposta, resposta_certa):
            return ap
    return None


def main():
    segredo_real = b"segredo-de-exemplo-da-rede-legitima"

    real = PontoDeAcesso("CafeCentral-WiFi", segredo=segredo_real)
    impostor = PontoDeAcesso("CafeCentral-WiFi")  # mesmo nome, sem o segredo

    print("=== os dois transmitem exatamente o mesmo nome ===")
    print("  real:     ", real.transmitir_beacon())
    print("  impostor: ", impostor.transmitir_beacon())

    print("\n=== cliente que confia so no nome ===")
    escolhido = cliente_confia_so_no_nome("CafeCentral-WiFi", [impostor, real])
    print(f"  conectou em: {'IMPOSTOR' if escolhido is impostor else 'rede real'}")
    print("  (a ordem da lista decidiu -- o nome nao desempata nada)")

    print("\n=== cliente que exige prova mutua (desafio-resposta) ===")
    escolhido = cliente_exige_prova_mutua(segredo_real, [impostor, real])
    print(f"  conectou em: {'IMPOSTOR' if escolhido is impostor else 'rede real'}")
    print("  (o impostor tem o nome certo, mas nao tem o segredo -- falha)")

    print("\n=== leitura ===")
    print("  nome de rede e endereco de equipamento sao dados PUBLICOS,")
    print("  copiaveis por qualquer um que esteja no alcance. Nenhum dos")
    print("  dois prova que quem esta do outro lado conhece o segredo.")
    print("  so uma prova criptografica -- calculada, nao transmitida --")
    print("  distingue a rede real da copia com o mesmo nome.")


if __name__ == "__main__":
    main()
