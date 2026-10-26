@echo off
REM ============================================================
REM  Portafolio-QA - Script de inicializacion
REM  Crea el entorno virtual e instala las dependencias
REM  (requests y pytest) para correr las suites.
REM ============================================================
cd /d "%~dp0"

REM Detectar el comando de Python real (el alias "python" de la
REM Microsoft Store existe en el PATH pero no ejecuta nada)
set "PYTHON="
py --version >nul 2>nul
if not errorlevel 1 set "PYTHON=py"
if not defined PYTHON (
    python --version >nul 2>nul
    if not errorlevel 1 set "PYTHON=python"
)
if not defined PYTHON (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Descargalo desde https://www.python.org/downloads/
    pause
    exit /b 1
)

REM El entorno virtual vive dentro de la carpeta API, junto a las suites
if not exist API\venv (
    echo Creando entorno virtual en API\venv...
    %PYTHON% -m venv API\venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        pause
        exit /b 1
    )
)

echo Instalando dependencias...
call API\venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install requests pytest
if errorlevel 1 (
    echo [ERROR] No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Listo. Para activar el entorno en una nueva terminal:
echo      API\venv\Scripts\activate
echo  Para correr las pruebas de una API, desde su carpeta:
echo      cd API\Petstore\PRUEBAS
echo      pytest -v
echo  (igual con API\RestfulBooker\PRUEBAS y API\Toolshop\PRUEBAS)
echo ============================================================
pause
