#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.3 – MP10 – Evolução das concentrações médias anuais – RMSP
================================================================================

Este script gera um gráfico interativo em HTML com DOIS EIXOS Y, mostrando:
1. Eixo Y esquerdo: Concentração de MP₁₀ (µg/m³) - Média e faixa de percentis 10/90
2. Eixo Y direito: Número de dias desfavoráveis (ano todo)

O gráfico permite visualizar simultaneamente a qualidade do ar e a frequência
de dias com condições desfavoráveis de dispersão de poluentes.

Autor: Leonardo Rocha
Data: 2026-09-10
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos
from plotly.subplots import make_subplots  # Para criar gráficos com eixos duplos (Y secundário)


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
# O arquivo deve estar na mesma pasta do script
CSV = Path("Grafico5_3.csv")

# Lê o arquivo CSV com configurações específicas:
# - sep=None: detecta automaticamente o separador (vírgula, ponto-e-vírgula, etc.)
# - engine="python": usa o parser Python para maior flexibilidade
# - encoding="utf-8-sig": lida com arquivos UTF-8 com BOM (comum em Excel)
df = pd.read_csv(CSV, sep=None, engine="python", encoding="utf-8-sig")

# =============================================================================
# LIMPEZA E PREPARAÇÃO DOS DADOS
# =============================================================================

# --- Colunas de percentis (Per_90 e Per_10) ---
# Essas colunas podem conter valores com vírgula como separador decimal (padrão brasileiro)
# Exemplo: "45,2" em vez de "45.2"
# O código abaixo:
#   1. Converte para string
#   2. Substitui vírgulas por pontos (padrão internacional)
#   3. Converte para numérico, transformando erros em NaN
for c in ["Per_90", "Per_10"]:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"
    )

# --- Coluna de Ano ---
# Converte para numérico e depois para inteiro (anos não têm casas decimais)
df["Ano"] = pd.to_numeric(df["Ano"], errors="coerce").astype(int)

# --- Coluna de média (med_int) ---
# Converte para numérico, transformando valores inválidos em NaN
df["med_int"] = pd.to_numeric(df["med_int"], errors="coerce")

# --- Coluna de dias desfavoráveis (ndias_desf) ---
# Converte para numérico, transformando valores inválidos em NaN
df["ndias_desf"] = pd.to_numeric(df["ndias_desf"], errors="coerce")


# =============================================================================
# CRIAÇÃO DA FIGURA COM EIXO Y SECUNDÁRIO
# =============================================================================

# Cria uma figura com um subplot que possui um eixo Y secundário
# specs=[[{"secondary_y": True}]] permite ter dois eixos Y no mesmo gráfico
fig = make_subplots(specs=[[{"secondary_y": True}]])


# =============================================================================
# TRAÇO 1: PERCENTIL 90 (BASE PARA PREENCHIMENTO)
# =============================================================================

# Este traço é adicionado primeiro para servir como base para o preenchimento
# da área entre os percentis. Ele não é visível (width=0) e não aparece na legenda.
fig.add_trace(
    go.Scatter(
        x=df["Ano"],                          # Eixo X: anos
        y=df["Per_90"],                       # Eixo Y: valores do percentil 90
        mode="lines",                         # Modo: apenas linhas
        line=dict(width=0, color="rgba(0,0,0,0)"),  # Linha invisível (transparente)
        showlegend=False,                     # Não mostra na legenda
        # Template do tooltip ao passar o mouse
        
        hovertemplate="P90: %{y:.0f} µg/m³<extra></extra>"  
    ),
    secondary_y=False                         # Usa o eixo Y principal (esquerdo)
)


# =============================================================================
# TRAÇO 2: PERCENTIL 10 (ÁREA SOMBREADA)
# =============================================================================

# Este traço cria a área sombreada entre P10 e P90 usando fill="tonexty"
# Isso preenche a área entre este traço e o anterior (Per_90)
fig.add_trace(
    go.Scatter(
        x=df["Ano"],                          # Eixo X: anos
        y=df["Per_10"],                       # Eixo Y: valores do percentil 10
        mode="lines",                         # Modo: apenas linhas
        line=dict(width=0, color="rgba(0,0,0,0)"),  # Linha invisível
        fill="tonexty",                       # Preenche entre este traço e o anterior
        fillcolor="#dce6f2",                  # Azul claro
        name="Percentis 10/90",               # Nome na legenda
        
        # Tooltip exibindo o Percentil 10
        hovertemplate="<b>Percentis 10/90</b><br>"          # Título em negrito
        "P10: %{y:.0f} µg/m³<extra></extra>"
    ),
    secondary_y=False                         # Usa o eixo Y principal (esquerdo)
)

# =============================================================================
# TRAÇO 3: MÉDIA DE MP₁₀ (LINHA PRINCIPAL)
# =============================================================================

# Este traço mostra a média de MP₁₀ com linha preta, marcadores e rótulos de texto
fig.add_trace(
    go.Scatter(
        x=df["Ano"],                          # Eixo X: anos
        y=df["med_int"],                      # Eixo Y: valores da média
        mode="lines+markers+text",            # Modo: linha + marcadores + texto
        name="Média",                         # Nome na legenda
        
        # Configuração da linha
        line=dict(
            color="#111111",                  # Cor preta
            width=2                           # Espessura da linha
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color="#111111",                  # Cor preta (mesma da linha)
            size=8,                           # Tamanho do marcador
            symbol="circle",                  # Forma: círculo
            line=dict(
                color="#1D6FA5",              # Borda azul
                width=2                       # Espessura da borda
            )
        ),
        
        # Rótulos de texto nos pontos (valores arredondados)
        text=df["med_int"].round(0).astype(int).astype(str),
        textposition="top center",            # Posição: acima do ponto
        
        # Template do tooltip ao passar o mouse
        hovertemplate="<b>Média</b><br>%{y:.0f} µg/m³<extra></extra>"
    ),
    secondary_y=False                         # Usa o eixo Y principal (esquerdo)
)


# =============================================================================
# TRAÇO 4: DIAS DESFAVORÁVEIS (EIXO SECUNDÁRIO)
# =============================================================================

# Este traço mostra o número de dias desfavoráveis usando o eixo Y secundário (direito)
fig.add_trace(
    go.Scatter(
        x=df["Ano"],                          # Eixo X: anos
        y=df["ndias_desf"],                   # Eixo Y: número de dias desfavoráveis
        mode="lines+markers+text",            # Modo: linha + marcadores + texto
        name="NDias desfavoráveis (ano todo)", # Nome na legenda
        
        # Configuração da linha
        line=dict(
            color="#C84A43",                  # Cor vermelha
            width=2                           # Espessura da linha
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color="#C84A43",                  # Cor vermelha (mesma da linha)
            size=8,                           # Tamanho do marcador
            symbol="x"                        # Forma: X
        ),
        
        # Rótulos de texto nos pontos (valores arredondados)
        text=df["ndias_desf"].round(0).astype(int).astype(str),
        textposition="bottom center",         # Posição: abaixo do ponto
        
        # Template do tooltip ao passar o mouse
        hovertemplate="<b>Dias desfavoráveis</b><br>%{y:.0f} dias<extra></extra>"
    ),
    secondary_y=True                          # Usa o eixo Y secundário (direito)
)


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT GERAL
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco e linhas suaves
    template="plotly_white",
    
    # Altura da figura em pixels
    height=720,
    
    # Margens ao redor do gráfico
    # Margem direita maior (80px) para acomodar o eixo Y secundário
    # Margem inferior (100px) para a legenda horizontal e rótulos rotacionados
    margin=dict(l=90, r=80, t=25, b=100),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#FFFFFF",                  # Branco
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#FFFFFF",                   # Branco
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#555555"                       # Cinza escuro
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal
        yanchor="top",                        # Âncora no topo
        y=-0.105,                             # Posicionada abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X
        font=dict(size=12)                    # Tamanho da fonte da legenda
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        tickmode="linear",                    # Ticks em intervalos regulares
        dtick=1,                              # Intervalo de 1 em 1 ano
        range=[2000, 2025],                   # Limites: 2000 a 2025
        tickangle=-90,                        # Rotação de -90° (vertical)
        showgrid=False,                        # Sem linhas de grade verticais
        showticklabels=True,                   # Mostra os rótulos
        ticks="inside",                        # Marcadores  do eixo
        showline=True,                         # Mostra a linha do eixo
        linecolor="#B8B8B8",
    )
)


# =============================================================================
# CONFIGURAÇÃO DO EIXO Y PRINCIPAL (ESQUERDO) - MP₁₀
# =============================================================================

fig.update_yaxes(
    title_text="MP₁₀ (µg/m³)",                # Título do eixo
    range=[0, 80],                            # Limites: 0 a 80 µg/m³
    dtick=10,                                 # Intervalo de 10 em 10
    showgrid=False,                           # Mostra linhas de grade
    gridcolor="rgba(130,130,130,0.35)",       # Cinza com 35% opacidade
    griddash="dash",                          # Linhas tracejadas
    secondary_y=False,                         # Eixo Y principal (esquerdo)
    showticklabels=True,      # Mostra os rótulos
    ticks="outside",          # Marcadores fora do eixo
    showline=True,                         # Mostra a linha do eixo
    linecolor="#B8B8B8",
)


# =============================================================================
# CONFIGURAÇÃO DO EIXO Y SECUNDÁRIO (DIREITO) - DIAS DESFAVORÁVEIS
# =============================================================================

fig.update_yaxes(
    title_text="Número de dias desfavoráveis", # Título do eixo
    range=[0, 100],                           # Limites: 0 a 100 dias
    dtick=20,                                 # Intervalo de 20 em 20
    showgrid=False,                           # Sem linhas de grade (evita poluição visual)
    secondary_y=True,                          # Eixo Y secundário (direito)
    showticklabels=True,      # Mostra os rótulos
    ticks="outside",          # Marcadores fora do eixo
    showline=True,                         # Mostra a linha do eixo
    linecolor="#B8B8B8",
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (funciona offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta ao tamanho da tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                   # Permite zoom com scroll do mouse
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO COMBINADO GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Anos: {min(df['Ano'])} a {max(df['Ano'])}")
print(f"📉 Média MP₁₀: {df['med_int'].min():.1f} a {df['med_int'].max():.1f} µg/m³")
print(f"📆 Dias desfavoráveis: {df['ndias_desf'].min():.0f} a {df['ndias_desf'].max():.0f} dias")
print("=" * 70)
print("🌐 Abra o arquivo no navegador para visualizar o gráfico interativo.")
print("💡 Dica: Passe o mouse sobre as linhas para ver os valores detalhados.")
print("🔍 Use o scroll para zoom e arraste para navegar.")
print("=" * 70)