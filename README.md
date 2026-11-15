# Site institucional: Lígia Gervásio, Hipnoterapeuta Clínica

Site de uma página, em um único arquivo, para a Lígia Gervásio (São José do Rio Pardo/SP e online).

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `index.html` | O site pronto. CSS, JavaScript e fotos ficam dentro dele. Publique este arquivo. |
| `og-image.jpg` | Imagem que aparece quando o link é compartilhado no WhatsApp e nas redes (1200×630). |
| `apple-touch-icon.png`, `favicon-32.png` | Ícones do site. |
| `fonte/template.html` | O modelo do site, com os textos e o visual. |
| `fonte/build.py` | Os dados da profissional e o gerador do `index.html`. |
| `fonte/gerar_imagens.py` | Gera a `og-image.jpg` e os ícones. |
| `fonte/fotos/` | Fotos usadas no site. |

Publique na raiz do domínio estes 4 arquivos: `index.html`, `og-image.jpg`, `apple-touch-icon.png` e `favicon-32.png`.

## Como atualizar

Precisa de Python 3 com a biblioteca Pillow (`pip install pillow`).

1. Abra `fonte/build.py` e edite o bloco **DADOS DA PROFISSIONAL**:
   - `DOMINIO`: o endereço final do site, por exemplo `https://www.ligiagervasio.com.br`. Enquanto estiver vazio, o link de compartilhamento não mostra a imagem de prévia no WhatsApp.
   - `RUA`, `BAIRRO`, `CEP`: endereço do consultório. Enquanto `RUA` estiver vazia, o site diz que o endereço é informado no agendamento.
   - `FOTO_CONSULTORIO`: nome do arquivo da foto do consultório, colocado em `fonte/fotos/`.
   - `FORMACAO`: um item por curso, com a instituição. Lista vazia esconde o bloco.
   - `DEPOIMENTOS`: até 3, reais e autorizados. Lista vazia esconde a seção.
   - `WHATSAPP` e `INSTAGRAM_URL`, se mudarem.
2. Para trocar as fotos, substitua `fonte/fotos/hero.jpg` (quadrada) e `fonte/fotos/quem-sou-eu.jpg` (vertical, 4:5) mantendo os nomes.
3. Rode na pasta do projeto:

   ```
   python3 fonte/build.py
   python3 fonte/gerar_imagens.py   # só se mudar a foto da Hero ou os dados da imagem de compartilhamento
   ```

4. Depois de trocar a `og-image.jpg` num site já publicado, aumente o `?v=1` para `?v=2` no `build.py` (procure por `og-image.jpg?v=1`) e gere de novo, para o WhatsApp buscar a imagem nova.

Os textos das seções ficam em `fonte/template.html`. Edite lá e rode o `build.py` de novo.

## Identidade visual

- Fontes: Gloock (títulos) e Onest (texto), do Google Fonts.
- Cores: lavanda #E7E9F1 (fundo), azul royal #0046D5, azul noite #10163A, lilás #B4B0E0, ardósia #3A4060.
- Assinatura: títulos em duas camadas (uma cópia lilás deslocada que se junta ao texto) e círculos concêntricos finos.
