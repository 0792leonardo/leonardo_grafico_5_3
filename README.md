# Gráfico 5.3 — MP10 e dias desfavoráveis

Gráfico interativo em Python + Plotly baseado diretamente no CSV fornecido.

## Dados

Arquivo fonte: `Grafico5_3.csv`

Campos utilizados:

- `Ano`
- `med_int` — média de MP10
- `ndias_desf` — número de dias desfavoráveis
- `Per_90` — percentil 90
- `Per_10` — percentil 10

Os campos `Per_90` e `Per_10` são convertidos de vírgula decimal para número.

## Configuração visual

- MP10 no eixo esquerdo: 0–80 µg/m³.
- Dias desfavoráveis no eixo direito: 0–100.
- Faixa entre os percentis 10 e 90.
- Linha preta para a média.
- Linha vermelha para os dias desfavoráveis.
- Rótulos numéricos nos pontos.
- Fundo `#DDE9F4`.
- Eixo temporal de 2000 a 2025.
- HTML autocontido.

## Arquivos

- `index.html`
- `Grafico5_3.csv`
- `gerar_grafico.py`
- `publicar_github.bat`
- `.github/workflows/pages.yml`
- `.nojekyll`
- `README.md`

## Instalação

```bash
pip install pandas plotly
```

## Gerar

```bash
python gerar_grafico.py
```

## Publicar

```bash
git init
git add .
git commit -m "Adicionar grafico 5.3 MP10"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

URL:

```text
https://SEU_USUARIO.github.io/SEU_REPOSITORIO/
```
