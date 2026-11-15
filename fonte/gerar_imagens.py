#!/usr/bin/env python3
"""Gera og-image.jpg (1200x630), apple-touch-icon.png (180) e favicon-32.png.

Rode:  python3 fonte/gerar_imagens.py
Precisa das fontes Gloock e Inter (ou Onest) instaladas, ou ajuste os caminhos abaixo.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)

NOME = "Lígia Gervásio"
PROFISSAO = "Hipnoterapeuta Clínica"
FRASE = ["Hipnose clínica para", "ansiedade, pânico,", "fobias e TOC"]
CIDADE = "São José do Rio Pardo/SP e online"
SELO = "Agende pelo WhatsApp"

FONTE_TITULO = os.environ.get("FONTE_TITULO", os.path.expanduser("~/.fonts/Gloock-Regular.ttf"))
FONTE_TEXTO = os.environ.get("FONTE_TEXTO", "/usr/share/fonts/opentype/inter/Inter-Medium.otf")
FONTE_TEXTO_B = os.environ.get("FONTE_TEXTO_B", "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf")

BG = (231, 233, 241)
AZUL = (0, 70, 213)
NOITE = (16, 22, 58)
LILAS = (180, 176, 224)
TEXTO = (58, 64, 96)


def fonte(caminho, tam):
    try:
        return ImageFont.truetype(caminho, tam)
    except OSError:
        return ImageFont.load_default(tam)


def foto_circular(diam):
    im = Image.open(os.path.join(AQUI, "fotos", "hero.jpg")).convert("RGB").resize((diam, diam), Image.LANCZOS)
    m = Image.new("L", (diam * 4, diam * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, diam * 4 - 1, diam * 4 - 1), fill=255)
    return im, m.resize((diam, diam), Image.LANCZOS)


def aneis(draw, cx, cy, raios, cor, largura=2):
    for r in raios:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=cor, width=largura)


def og():
    W, H, S = 1200, 630, 2
    im = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(im)
    cx, cy = W * S // 2, 315 * S
    aneis(d, cx, cy, [r * S for r in (190, 240, 295, 355, 420)], (178, 190, 230), 2)
    diam = 300 * S
    foto, mask = foto_circular(diam)
    d.ellipse((cx - diam // 2 - 14 * S, cy - diam // 2 - 14 * S, cx + diam // 2 + 14 * S, cy + diam // 2 + 14 * S), fill=BG, outline=(200, 204, 222), width=2)
    im.paste(foto, (cx - diam // 2, cy - diam // 2), mask)

    # esquerda: nome com camada "fantasma"
    fn = fonte(FONTE_TITULO, 62 * S)
    x0, y0 = 64 * S, 222 * S
    ghost = Image.new("RGBA", im.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost)
    for i, linha in enumerate(NOME.split(" ")):
        gd.text((x0 + 7 * S, y0 - 5 * S + i * 70 * S), linha, font=fn, fill=LILAS + (160,))
    ghost = ghost.filter(ImageFilter.GaussianBlur(2 * S))
    im.paste(ghost, (0, 0), ghost)
    d = ImageDraw.Draw(im)
    for i, linha in enumerate(NOME.split(" ")):
        d.text((x0, y0 + i * 70 * S), linha, font=fn, fill=NOITE)
    d.text((x0, y0 + 158 * S), PROFISSAO, font=fonte(FONTE_TEXTO, 24 * S), fill=TEXTO)

    # direita: frase, cidade e selo
    ft = fonte(FONTE_TITULO, 30 * S)
    xr = 838 * S
    for i, l in enumerate(FRASE):
        d.text((xr, 207 * S + i * 38 * S), l, font=ft, fill=NOITE)
    d.text((xr, 332 * S), CIDADE, font=fonte(FONTE_TEXTO, 17 * S), fill=TEXTO)

    # selo
    fs = fonte(FONTE_TEXTO_B, 22 * S)
    tw = d.textlength(SELO, font=fs)
    px, py, ph = xr, 377 * S, 54 * S
    pw = int(tw + 56 * S)
    d.rounded_rectangle((px + 6 * S, py + 6 * S, px + pw + 6 * S, py + ph + 6 * S), radius=ph // 2, outline=AZUL, width=3)
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=ph // 2, fill=AZUL)
    d.text((px + 28 * S, py + ph // 2), SELO, font=fs, fill=(255, 255, 255), anchor="lm")

    im.resize((W, H), Image.LANCZOS).save(os.path.join(RAIZ, "og-image.jpg"), quality=86, optimize=True, progressive=True)


def icone(tam, destino):
    S = 8
    T = tam * S
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    raio = T // 2 if tam <= 32 else int(T * 0.22)
    d.rounded_rectangle((0, 0, T - 1, T - 1), radius=raio, fill=NOITE)
    f = fonte(FONTE_TITULO, int(T * (0.62 if tam <= 32 else 0.46)))
    txt = "L" if tam <= 32 else "LG"
    off = int(T * 0.035)
    d.text((T // 2 + off, T // 2 - off + int(T * .02)), txt, font=f, fill=LILAS + (200,), anchor="mm")
    d.text((T // 2, T // 2 + int(T * .02)), txt, font=f, fill=(255, 255, 255), anchor="mm")
    im = im.resize((tam, tam), Image.LANCZOS)
    if tam == 180:  # iOS não usa transparência
        fundo = Image.new("RGB", (tam, tam), NOITE)
        fundo.paste(im, (0, 0), im)
        im = fundo
    im.save(os.path.join(RAIZ, destino), optimize=True)


if __name__ == "__main__":
    og()
    icone(180, "apple-touch-icon.png")
    icone(32, "favicon-32.png")
    print("og-image.jpg, apple-touch-icon.png e favicon-32.png gerados")
