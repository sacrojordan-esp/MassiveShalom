@echo off
chcp 65001 >nul

echo ========================================
echo   EJECUTAR SCRIPT SHALOM
echo ========================================
echo.
echo INSTRUCCIONES:
echo 1. Ve a cliente.shalom.pe (logueado)
echo 2. Con Cookie-Editor, haz click en "Export" (todas las cookies)
echo 3. Copia el JSON
echo 4. Abre el archivo cookies.txt con el bloc de notas y pega el JSON
echo 5. Guarda y cierra el archivo
echo 6. Ejecuta este BAT
echo.
echo ----------------------------------------------------------
echo.

if not exist "cookies.txt" (
    echo ERROR: No existe el archivo cookies.txt
    echo Crea ese archivo y pega el JSON de Cookie-Editor
    pause
    exit
)

echo Archivo cookies.txt encontrado
echo Extrayendo cookies y ejecutando script...
echo.

call venv\Scripts\python.exe actualiza_y_ejecuta.py

echo.
echo ========================================
echo Script terminado
echo ========================================
pause
