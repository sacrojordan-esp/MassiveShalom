import requests, re, json
import pandas as pd
from urllib.parse import unquote
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Session setup
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://cliente.shalom.pe",
    "Referer": "https://cliente.shalom.pe/",
    "X-Requested-With": "XMLHttpRequest"
})

# Cookies - se actualizan desde cookies.txt
session.cookies.set("shalomempresas_session", "COOKIE_SESSION", domain="cliente.shalom.pe")
session.cookies.set("XSRF-TOKEN", "COOKIE_XSRF", domain="cliente.shalom.pe")

# Login page para CSRF
login_page = session.get("https://cliente.shalom.pe/")
csrf_token = re.search(r'name="csrf-token" content="(.*?)"', login_page.text)
csrf_token = csrf_token.group(1) if csrf_token else ""

# Headers
xsrf_token = unquote(session.cookies.get("XSRF-TOKEN", "") or "")
headers = {"X-Requested-With": "XMLHttpRequest", "X-XSRF-TOKEN": xsrf_token}

# Cargar destinos
print("Cargando destinos...")
r_destinos = session.get("https://cliente.shalom.pe/envia_ya/service_order/restricciones-categorias?origen=426", headers=headers)
destinos = {v["nombre_terminal"]: int(k) for k, v in r_destinos.json()["data"].items()}
print(f"Destinos: {len(destinos)}")

# Buscar destinatario por DNI
def buscar_destinatario(dni):
    r = session.post("https://cliente.shalom.pe/envia_ya/person/search", data={"_token": csrf_token, "documento": str(dni)}, headers=headers)
    data = r.json()
    return data.get("data", {}).get("id") if data.get("success") else None

# Excel setup
df = pd.read_excel("MassiveShalom.xlsx")
if "ESTADO" not in df.columns:
    df["ESTADO"] = ""
wb = load_workbook("MassiveShalom.xlsx")
ws = wb.active

verde = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
naranja = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
rojo = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

# Constantes
ORIGEN = 426
COSTO_FIJO = 5

# Procesar cada fila
for idx, fila in df.iterrows():
    excel_row = idx + 2
    dni = str(fila["DNI"])
    agencia = fila["AGENCIA SHALOM"]
    clave = str(fila["CLAVE"])
    
    print(f"Fila {idx + 1}: {fila['CLIENTE']}")
    
    # Buscar destino
    destino_id = destinos.get(agencia)
    if not destino_id:
        ws.cell(excel_row, 12, "NO PROCEDIO").fill = rojo
        continue
    
    # Buscar destinatario
    destinatario_id = buscar_destinatario(dni)
    if not destinatario_id:
        ws.cell(excel_row, 12, "NO PROCEDIO POR ID").fill = naranja
        continue
    
    # Enviar pedido
    payload = {
        "origen": ORIGEN, "destino": destino_id, "tipo_pago": "REMITENTE", "tipo_producto": 1090,
        "aereo": 0, "alto": "", "ancho": "", "cantidad": 1, "clave": clave, "contacto_doc": "",
        "costo": "5.00", "declaracion_jurada": "", "destinatario": dni, "destinatario_id": destinatario_id,
        "garantia": 0, "garantia_costo": 0, "garantia_monto": "0.00", "grrs": "[]", "largo": "", "peso": "",
        "remitente": "20612606103", "remitente_id": 1074, "servicio_cobranza": 0, "servicio_cobranza_costo": 0,
        "servicio_cobranza_datos": "{}", "tipo_producto_json": {"value": "5.00", "name": "Caja Paquete XS", "detalle": "15 x 20 x 12 cm"}
    }
    
    response = session.post("https://cliente.shalom.pe/envia_ya/service_order/save", json=payload, headers=headers)
    
    try:
        resp_json = response.json()
        if resp_json.get("success"):
            print(f"  [OK] PROCEDIO - Guia: {resp_json['data'].get('guia')}")
            ws.cell(excel_row, 12, "PROCEDIO").fill = verde
        else:
            msg = resp_json.get("message", "Error")
            print(f"  [ERROR] {msg}")
            ws.cell(excel_row, 12, f"NO PROCEDIO: {msg}").fill = rojo
    except:
        print("  [ERROR] Respuesta invalida")
        ws.cell(excel_row, 12, "NO PROCEDIO").fill = rojo

wb.save("MassiveShalom.xlsx")
print("\nExcel guardado")
