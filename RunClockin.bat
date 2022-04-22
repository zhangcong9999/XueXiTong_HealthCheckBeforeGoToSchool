@echo off
set CurrentDir=%~dp0
pushd %CurrentDir%
python clockin.py
popd