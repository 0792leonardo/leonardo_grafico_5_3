@echo off
echo ============================================
echo Grafico 5.3 - MP10 + Dias desfavoraveis
echo Plotly + GitHub Pages
echo ============================================
echo.
set /p REPO=URL do repositorio GitHub:
git init
git add .
git commit -m "Adicionar grafico 5.3 MP10"
git branch -M main
git remote add origin %REPO%
git push -u origin main
echo.
echo Configure no GitHub:
echo Settings ^> Pages ^> Build and deployment ^> Source: GitHub Actions
pause
