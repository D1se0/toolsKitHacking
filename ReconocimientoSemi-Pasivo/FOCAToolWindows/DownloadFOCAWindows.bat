@echo off
setlocal

:: Definir el enlace
set LINK=https://github.com/ElevenPaths/FOCA/releases/download/v3.4.7.1/FOCA-v3.4.7.1.zip

:: Función para verificar si Firefox está instalado
:check_chrome
where chrome >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Google Chrome no está instalado en la ubicación estándar.
    echo [!] Por favor, instala Chrome primero.
    goto :end
) else (
    echo [+] Google Chrome está instalado.
)

:: Función para cerrar Firefox si está abierto
:close_firefox
tasklist /FI "IMAGENAME eq firefox.exe" 2>NUL | find /I "firefox.exe" >NUL
if %ERRORLEVEL% EQU 0 (
    echo [+] Firefox está abierto. Cerrándolo...
    taskkill /F /IM firefox.exe
    timeout /t 2 >nul
) else (
    echo [+] Firefox no está abierto.
)
goto :skip_firefox

:: Abrir el enlace en Google Chrome
:open_chrome
echo [+] Abriendo el enlace en Google Chrome...
start chrome %LINK%

:: Finalizar
:end
endlocal
exit
