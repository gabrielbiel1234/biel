
@echo off
title ULTRA AI
cd /d "%~dp0"
echo Iniciando ULTRA AI...
echo Mantenha esta janela aberta enquanto usar o robo.
start "" http://localhost:8000
py server.py
pause
