import re
import json

# Leer cookies del archivo
try:
    with open("cookies.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Limpiar el contenido (quitar possible BOM o espacios)
    content = content.strip()
    
    # Parsear el JSON
    cookies_list = json.loads(content)
except FileNotFoundError:
    print("Error: No se encontró el archivo cookies.txt")
    print("Crea un archivo llamado 'cookies.txt' y pega el JSON de Cookie-Editor")
    input("Presiona Enter para salir...")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: JSON inválido - {e}")
    print("Asegúrate de pegar el JSON completo de Cookie-Editor en cookies.txt")
    input("Presiona Enter para salir...")
    exit()

# Extraer solo las cookies necesarias
cookie_session = ""
cookie_xsrf = ""

for cookie in cookies_list:
    if cookie.get("name") == "shalomempresas_session":
        cookie_session = cookie.get("value", "")
    elif cookie.get("name") == "XSRF-TOKEN":
        cookie_xsrf = cookie.get("value", "")

if not cookie_session or not cookie_xsrf:
    print("Error: No se encontraron las cookies necesarias")
    print("Asegúrate de estar logueado en cliente.shalom.pe")
    input("Presiona Enter para salir...")
    exit()

print(f"Cookies extraidas correctamente")
print(f"  Session: {cookie_session[:30]}...")
print(f"  XSRF: {cookie_xsrf[:30]}...")

# Leer main.py
with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar cookies
content = re.sub(
    r'session\.cookies\.set\("shalomempresas_session", "[^"]*"',
    f'session.cookies.set("shalomempresas_session", "{cookie_session}"',
    content
)

content = re.sub(
    r'session\.cookies\.set\("XSRF-TOKEN", "[^"]*"',
    f'session.cookies.set("XSRF-TOKEN", "{cookie_xsrf}"',
    content
)

# Guardar main.py actualizado
with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\nCookies actualizadas en main.py")
print("Ejecutando script...\n")

# Ejecutar main.py
import subprocess
result = subprocess.run(
    ["venv\\Scripts\\python.exe", "main.py"], 
    capture_output=True, 
    text=True, 
    encoding='utf-8', 
    errors='replace'
)
print(result.stdout)
if result.stderr:
    print("Errores:", result.stderr)
