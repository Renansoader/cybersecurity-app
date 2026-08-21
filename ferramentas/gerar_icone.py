"""Gera o app.ico da raiz do projeto — escudo com fechadura, na paleta do app.

Só precisa rodar de novo se você quiser mudar o desenho. O .ico fica versionado,
então o app e o atalho funcionam sem isso aqui.

Precisa do Pillow, que NÃO é dependência do app:

    pip install pillow
    python ferramentas/gerar_icone.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "app.ico"

FUNDO = (26, 27, 38, 255)        # BG_PRIMARY do theme.py
ESCUDO = (122, 162, 247, 255)    # ACCENT
INTERNO = (31, 35, 53, 255)      # BG_CARD
BRILHO = (158, 206, 106, 255)    # SUCCESS

LADO = 1024  # desenha grande e reduz: borda sai limpa
TAMANHOS = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]


def escudo(desenho, cx, topo, largura, altura, cor):
    """Escudo: ombros retos no topo, laterais retas e ponta arredondada embaixo."""
    meia = largura / 2
    ombro = topo + altura * 0.62
    desenho.polygon(
        [(cx - meia, topo), (cx + meia, topo), (cx + meia, ombro),
         (cx, topo + altura), (cx - meia, ombro)],
        fill=cor)
    desenho.ellipse([cx - meia, topo - meia * 0.35, cx + meia, topo + meia * 0.35], fill=cor)


def main():
    imagem = Image.new("RGBA", (LADO, LADO), (0, 0, 0, 0))
    desenho = ImageDraw.Draw(imagem)

    margem = LADO * 0.06
    desenho.rounded_rectangle([margem, margem, LADO - margem, LADO - margem],
                              radius=LADO * 0.18, fill=FUNDO)

    centro = LADO / 2
    escudo(desenho, centro, LADO * 0.24, LADO * 0.52, LADO * 0.56, ESCUDO)
    escudo(desenho, centro, LADO * 0.30, LADO * 0.38, LADO * 0.42, INTERNO)

    # fechadura: círculo com haste, o símbolo mais legível a 16 px
    raio = LADO * 0.075
    desenho.ellipse([centro - raio, centro - raio * 1.4, centro + raio, centro + raio * 0.6],
                    fill=BRILHO)
    desenho.polygon([(centro - raio * 0.45, centro + raio * 0.2),
                     (centro + raio * 0.45, centro + raio * 0.2),
                     (centro + raio * 0.30, centro + raio * 2.2),
                     (centro - raio * 0.30, centro + raio * 2.2)], fill=BRILHO)

    imagem.save(SAIDA, format="ICO", sizes=TAMANHOS)
    print(f"gerado: {SAIDA}  ({SAIDA.stat().st_size} bytes, {len(TAMANHOS)} resoluções)")


if __name__ == "__main__":
    main()
