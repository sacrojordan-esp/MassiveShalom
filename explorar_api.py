import requests
from urllib.parse import unquote
import re

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# Login
login_page = session.get("https://cliente.shalom.pe/login#/")
csrf_token = re.search(r'name="csrf-token" content="(.*?)"', login_page.text).group(1)
session.post("https://pro.shalom.pe/login", data={"email": "20612606103", "password": "!+/BFy9H+_xj}se8"})

xsrf_token = unquote(session.cookies.get("XSRF-TOKEN"))
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "X-XSRF-TOKEN": xsrf_token
}

# Más endpoints
endpoints = [
    "/api/user",
    "/api/destinos",
    "/api/origenes",
    "/envia_ya/origen",
    "/envia_ya/destino",
    "/envia_ya/ubigeo",
    "/envia_ya/zonas",
    "/envia_ya/service_order/origenes",
]

print("=== Explorando API ===")
for ep in endpoints:
    try:
        r = session.get(f"https://pro.shalom.pe{ep}", headers=headers)
        print(f"{ep}: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  → {data}")
            except:
                print(f"  → {r.text[:100]}")
    except Exception as e:
        print(f"{ep}: Error - {e}")

# Buscar en el HTML del login los endpoints
print("\n=== Buscando en HTML ===")
html = login_page.text
# Buscar URLs o APIs en el JS
import re
urls = re.findall(r'["\'](/api[^"\']*)["\']', html)
urls += re.findall(r'["\'](/envia_ya[^"\']*)["\']', html)
print("URLs encontradas:", set(urls))
