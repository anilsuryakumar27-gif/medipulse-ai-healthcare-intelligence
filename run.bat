@echo off
title MediPulse AI - Australian GP Intelligence & Growth Platform
echo ======================================================================
echo  MediPulse AI - Australian GP Healthcare Intelligence Platform
echo  Starting local server...
echo ======================================================================

start "" http://localhost:5000
python app.py
pause
