#!/bin/sh
# Gera o site e publica no GitHub Pages (https://lirukkkkk.github.io/portfolio/)
set -e
cd "$(dirname "$0")/.."
python3 tools/build.py
git add -A
git commit -m "${1:-Atualiza site}" || echo "Nada novo para salvar."
git push origin main
git push origin "$(git subtree split --prefix site main)":gh-pages --force
echo "Publicado. Em 1 a 2 minutos: https://lirukkkkk.github.io/portfolio/"
