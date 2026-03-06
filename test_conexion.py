import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

print("Probando conexión a Shalom...")

try:
    response = session.get("https://cliente.shalom.pe/login#/")
    print(f"Status: {response.status_code}")
    print(f"URL final: {response.url}")
    print("¡Conexión exitosa!" if response.status_code == 200 else "Algo falló")
except Exception as e:
    print(f"Error: {e}")
