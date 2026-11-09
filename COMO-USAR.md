# Site portfólio — como usar

## Ver no computador

```bash
cd "/Users/alanveloso/Documents/Portifolio Alan" && python3 -m http.server 4173 --directory site
```

Depois abra http://localhost:4173.

## Estrutura

- `site/`: o site pronto. **Só esta pasta vai para o GitHub Pages.**
  - `index.html`: a home (versão Índice suíço).
  - `planos.html`: planos mensais, comparativo e serviços avulsos (valores em `PLANS` e `SINGLES` no `content.py`).
  - `trabalhos/`: uma página por case.
  - `assets/`: imagens (AVIF + WebP), vídeos comprimidos, fontes, CSS e JS.
- `tools/content.py`: **todos os textos (PT/EN), os cases e as imagens de cada um.** Edite aqui.
- `tools/assets.py`: gera as imagens otimizadas a partir de "Meus Trabalhos separados por cliente".
- `tools/build.py`: gera as páginas HTML a partir do `content.py`.
- `tools/avatar.py`: separa as pupilas do autorretrato (`Icon Alan.JPG`) para o avatar piscar e olhar. Rode de novo só se trocar o desenho.

## Mudar um texto ou adicionar um trabalho

1. Edite `tools/content.py`.
2. Se adicionou imagens, gere as versões otimizadas:

```bash
python3 tools/assets.py
```

3. Gere as páginas de novo:

```bash
python3 tools/build.py
```

## Antes de publicar

- Preencher `SITE_URL` e `GA_ID` (Google Analytics) no topo de `tools/build.py`.
- O formulário de briefing não usa servidor: ele abre o WhatsApp ou o e-mail do visitante com a mensagem pronta. Por isso funciona no GitHub Pages sem nenhum custo.
