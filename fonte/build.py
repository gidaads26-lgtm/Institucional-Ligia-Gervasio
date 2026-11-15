#!/usr/bin/env python3
"""Gera o index.html do site da Lígia Gervásio a partir do template.html.

Como usar:
  1. Edite os dados abaixo (endereço, formação, depoimentos, domínio...).
  2. Troque as fotos na pasta fonte/fotos/ mantendo os mesmos nomes.
  3. Rode:  python3 fonte/build.py
O arquivo index.html é gerado na pasta acima de fonte/.
"""
import base64, html, io, json, os, urllib.parse
from PIL import Image

# =====================================================================
# DADOS DA PROFISSIONAL (edite aqui)
# =====================================================================
NOME_COMPLETO = "Lígia Maria Magalhães Gervásio"
NOME_SITE     = "Lígia Gervásio"          # como aparece no cabeçalho e no título
PRIMEIRO_NOME = "Lígia"
ARTIGO_DE     = "da"                       # "da" para profissional mulher, "do" para homem
PROFISSAO     = "Hipnoterapeuta Clínica"
CIDADE        = "São José do Rio Pardo"
UF            = "SP"
WHATSAPP      = "5519981810682"            # DDI + DDD + número, só números
INSTAGRAM_URL = "https://www.instagram.com/ligia_hipnoterapia/"

# Domínio final, com https e sem barra no fim. Ex.: "https://www.ligiagervasio.com.br"
# Enquanto estiver vazio, as tags de URL absoluta (canonical, og:url) ficam de fora.
DOMINIO = ""

# Endereço do consultório. Deixe RUA vazia enquanto não estiver confirmado.
RUA    = ""        # Ex.: "Rua Exemplo, 123, sala 4"
BAIRRO = ""        # Ex.: "Centro"
CEP    = ""        # Ex.: "13720-000"

# Foto do consultório: coloque o arquivo em fonte/fotos/ e escreva o nome aqui.
# Vazio = a seção Local mostra um bloco visual no lugar da foto.
FOTO_CONSULTORIO = ""   # Ex.: "consultorio.jpg"

# Formação: um item por curso, com a instituição. Lista vazia = bloco escondido.
FORMACAO = [
    # "Formação em Hipnose Clínica, Nome da Instituição",
]

# Depoimentos reais e autorizados (até 3). Lista vazia = seção escondida.
# foto: nome do arquivo em fonte/fotos/ (só se autorizada) ou "" para usar a inicial.
DEPOIMENTOS = [
    # {"nome": "Maria S.", "tema": "Pânico", "texto": "Texto do depoimento.", "foto": ""},
]

DESCRICAO = (f"{PROFISSAO} em {CIDADE}/{UF} e online. Hipnose clínica para ansiedade, "
             "pânico, fobias e TOC. Agende sua consulta de avaliação pelo WhatsApp.")
# =====================================================================

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
FOTOS = os.path.join(AQUI, "fotos")
CIDADE_UF = f"{CIDADE}/{UF}"
esc = lambda s: html.escape(s, quote=True)

ICO_WA = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5 0 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3Z"/></svg>')
ICO_IG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/></svg>')
ICO_PIN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>')
ANEIS = ('<svg class="aneis" viewBox="0 0 400 400" aria-hidden="true"><circle cx="200" cy="200" r="50"/>'
         '<circle cx="200" cy="200" r="90"/><circle cx="200" cy="200" r="130"/><circle cx="200" cy="200" r="170"/></svg>')


def foto_b64(nome, largura_max=1000, qualidade=80):
    im = Image.open(os.path.join(FOTOS, nome)).convert("RGB")
    if im.width > largura_max:
        im = im.resize((largura_max, round(im.height * largura_max / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=qualidade, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def wa(msg):
    return f"https://wa.me/{WHATSAPP}?text=" + urllib.parse.quote(msg)


def bloco_local():
    if FOTO_CONSULTORIO:
        return (f'<div class="local-visual rv"><img src="{foto_b64(FOTO_CONSULTORIO)}" '
                f'alt="Consultório de {esc(NOME_SITE)} em {esc(CIDADE_UF)}" loading="lazy"></div>')
    return f'<div class="local-visual rv">{ANEIS}<p>{esc(CIDADE)}, {UF}</p></div>'


def bloco_endereco():
    if RUA:
        linhas = [RUA, ", ".join(x for x in [BAIRRO, CIDADE_UF] if x)]
        if CEP:
            linhas.append(f"CEP {CEP}")
        return '<address class="endereco"><p>' + "<br>".join(esc(l) for l in linhas) + "</p></address>"
    return (f"<p>Atendimento presencial em {esc(CIDADE_UF)}. "
            "O endereço completo é informado no agendamento pelo WhatsApp.</p>")


def bloco_formacao():
    if not FORMACAO:
        return ""
    itens = "".join(f"<li>{esc(f)}</li>" for f in FORMACAO)
    return f'<div class="formacao rv"><h3>Formação</h3><ul>{itens}</ul></div>'


def bloco_depoimentos():
    if not DEPOIMENTOS:
        return ""
    cartoes = []
    for i, d in enumerate(DEPOIMENTOS[:3]):
        if d.get("foto"):
            avatar = f'<img src="{foto_b64(d["foto"], 160)}" alt="">'
        else:
            avatar = esc(d["nome"].strip()[0].upper())
        cartoes.append(
            f'<figure class="cartao depo rv" style="--i:{i}"><blockquote>“{esc(d["texto"])}”</blockquote>'
            f'<figcaption><span class="avatar" aria-hidden="true">{avatar}</span>'
            f'<span><b>{esc(d["nome"])}</b><small>{esc(d["tema"])}</small></span></figcaption></figure>')
    n = len(cartoes)
    return (f'<!-- 8. Depoimentos -->\n<section class="secao" id="depoimentos" aria-labelledby="titulo-depo" style="padding-top:0">'
            f'<div class="wrap"><h2 class="dupla" id="titulo-depo">O que dizem as pessoas que passaram por aqui</h2>'
            f'<div class="depo-grade n{n}">{"".join(cartoes)}</div></div></section>')


def jsonld():
    endereco = {"@type": "PostalAddress", "addressLocality": CIDADE, "addressRegion": UF, "addressCountry": "BR"}
    if RUA:
        endereco["streetAddress"] = RUA
    if CEP:
        endereco["postalCode"] = CEP
    dados = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"{NOME_SITE} | {PROFISSAO}",
        "description": DESCRICAO,
        "address": endereco,
        "telephone": "+" + WHATSAPP,
        "areaServed": [CIDADE_UF, "Online"],
        "sameAs": [INSTAGRAM_URL],
        "founder": {"@type": "Person", "name": NOME_COMPLETO, "jobTitle": PROFISSAO},
    }
    if DOMINIO:
        dados["url"] = DOMINIO + "/"
        dados["image"] = DOMINIO + "/og-image.jpg"
    return json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")


def meta_url():
    if not DOMINIO:
        return "<!-- Preencha DOMINIO no build.py para gerar canonical e og:url -->"
    return (f'<link rel="canonical" href="{DOMINIO}/">\n'
            f'<meta property="og:url" content="{DOMINIO}/">')


def main():
    tpl = open(os.path.join(AQUI, "template.html"), encoding="utf-8").read()
    og = (DOMINIO + "/og-image.jpg?v=1") if DOMINIO else "og-image.jpg?v=1"
    trocas = {
        "{{NOME_SITE}}": esc(NOME_SITE),
        "{{NOME_COMPLETO}}": esc(NOME_COMPLETO),
        "{{PRIMEIRO_NOME}}": PRIMEIRO_NOME,
        "{{ARTIGO_DE}}": ARTIGO_DE,
        "{{PROFISSAO}}": esc(PROFISSAO),
        "{{PROFISSAO_MINUSCULA}}": esc(PROFISSAO[0].lower() + PROFISSAO[1:].lower()),
        "{{CIDADE_UF}}": esc(CIDADE_UF),
        "{{DESCRICAO}}": esc(DESCRICAO),
        "{{WHATSAPP}}": WHATSAPP,
        "{{WA_AGENDAR}}": esc(wa(f"Olá, {PRIMEIRO_NOME}! Vim pelo site e gostaria de agendar uma consulta de avaliação.")),
        "{{WA_DUVIDA}}": esc(wa(f"Olá, {PRIMEIRO_NOME}! Vim pelo site e tenho uma dúvida sobre a hipnoterapia.")),
        "{{INSTAGRAM_URL}}": esc(INSTAGRAM_URL),
        "{{OG_IMAGE}}": og,
        "{{META_URL}}": meta_url(),
        "{{JSONLD}}": jsonld(),
        "{{FOTO_HERO}}": foto_b64("hero.jpg"),
        "{{FOTO_SOBRE}}": foto_b64("quem-sou-eu.jpg", 800),
        "{{LOCAL_VISUAL}}": bloco_local(),
        "{{ENDERECO_BLOCO}}": bloco_endereco(),
        "{{FORMACAO}}": bloco_formacao(),
        "{{DEPOIMENTOS}}": bloco_depoimentos(),
        "{{ICO_WA}}": ICO_WA,
        "{{ICO_IG}}": ICO_IG,
        "{{ICO_PIN}}": ICO_PIN,
    }
    for k, v in trocas.items():
        tpl = tpl.replace(k, v)
    sobra = [p for p in tpl.split("{{")[1:]]
    if sobra:
        raise SystemExit("Marcadores sem valor: " + ", ".join("{{" + s.split("}}")[0] + "}}" for s in sobra))
    destino = os.path.join(RAIZ, "index.html")
    open(destino, "w", encoding="utf-8").write(tpl)
    print(f"index.html gerado ({os.path.getsize(destino) // 1024} KB)")


if __name__ == "__main__":
    main()
