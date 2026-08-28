import os
import time
import random
import re
import requests
import pandas as pd
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ========================================
# 1. CONFIGURACIÓN DE REGISTROS (LOGS)
# ========================================
# Esto creará un archivo "scraper.log" para monitorear el script cuando esté en el servidor
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ========================================
# 2. CONFIGURACIÓN SEGURA
# ========================================
load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not API_KEY:
    logging.error("No se encontró la API Key en el archivo .env. Revisa el nombre de la variable.")
    exit()

CIUDAD = "Monterrey"
NICHO = "dentistas"
LIMITE_EMAILS = 15  # Aumentamos la extracción de correos para esta prueba

# ========================================
# 3. BÚSQUEDA PRIMARIA (CON PAGINACIÓN)
# ========================================
logging.info(f"Buscando {NICHO} en {CIUDAD}...")
places = []
search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={NICHO}+en+{CIUDAD}&key={API_KEY}"

# Bucle para recolectar todas las páginas posibles (Google da máximo 60 resultados por término)
while True:
    response = requests.get(search_url).json()
    resultados_pagina = response.get("results", [])
    places.extend(resultados_pagina)
    
    logging.info(f"Se obtuvieron {len(resultados_pagina)} lugares. Total acumulado: {len(places)}")
    
    next_page_token = response.get("next_page_token")
    if not next_page_token:
        break  # Si ya no hay más páginas, salimos del bucle
    
    # Mecanismo de reintento progresivo
    exito_paginacion = False
    for intento in range(3):
        tiempo_espera = 2 * (intento + 1)
        logging.info(f"Esperando {tiempo_espera}s para validar token (Intento {intento+1}/3)...")
        time.sleep(tiempo_espera)
        
        search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={API_KEY}"
        prueba_response = requests.get(search_url).json()
        
        # Si la respuesta trae resultados nuevos, el token ya es válido
        if prueba_response.get("results"):
            exito_paginacion = True
            break
            
    if not exito_paginacion:
        logging.warning("El token caducó o falló tras 3 intentos. Deteniendo búsqueda.")
        break

if not places:
    logging.warning("No se encontraron lugares. Verifica tus términos de búsqueda.")
    exit()

# ========================================
# 4. OBTENER DETALLES Y FILTRAR WEB
# ========================================
logging.info("Consultando detalles para verificar sitios web...")
data = []

for i, place in enumerate(places):
    place_id = place["place_id"]
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website,rating,formatted_address&key={API_KEY}"
    
    detail = requests.get(details_url).json().get("result", {})
    
    if detail.get("website"):
        registro = {
            "nombre": detail.get("name", ""),
            "telefono": detail.get("formatted_phone_number", ""),
            "website": detail.get("website", ""),
            "calificacion": detail.get("rating", ""),
            "direccion": detail.get("formatted_address", ""),
            "email": "" 
        }
        data.append(registro)
        logging.info(f"[+] Web encontrada: {registro['nombre']}")
    
    time.sleep(0.5)  # Respetar rate limits de Google

logging.info(f"Extracción de detalles completada. {len(data)} registros con sitio web.")

if not data:
    logging.warning("Ninguno de los lugares encontrados tiene un sitio web. Terminando proceso.")
    exit()

# ========================================
# 5. EXTRACCIÓN DE EMAILS (CORRECCIÓN DE TEXTO)
# ========================================
logging.info(f"Extrayendo emails de los primeros {LIMITE_EMAILS} sitios web...")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]

def extraer_email_de_sitio(url):
    try:
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        time.sleep(random.uniform(3, 7))
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # CORRECCIÓN: Obligamos a insertar un espacio entre cada elemento HTML
        texto = soup.get_text(separator=' ')
        
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', texto)
        emails_filtrados = [e for e in emails if not any(x in e.lower() for x in ["noreply", "no-reply", "info@"])]
        
        return emails_filtrados[0] if emails_filtrados else ""
    except Exception as e:
        logging.warning(f"No se pudo escanear {url}. Motivo: {e}")
        return ""

for i, registro in enumerate(data[:LIMITE_EMAILS]):
    if registro["website"]:
        email = extraer_email_de_sitio(registro["website"])
        registro["email"] = email
        logging.info(f"[{i+1}/{min(LIMITE_EMAILS, len(data))}] {registro['nombre']} -> {email if email else 'No encontrado'}")

# ========================================
# 6. CREAR CSV FREEMIUM
# ========================================
df = pd.DataFrame(data)

def mask_phone(phone):
    if not phone or len(phone) < 4: return phone
    digits = re.sub(r'\D', '', phone)
    if len(digits) >= 4: return digits[:2] + '-' + 'X' * (len(digits) - 2)
    return phone

def mask_email(email):
    if not email or '@' not in email: return email
    local, domain = email.split('@', 1)
    if len(local) >= 2: return local[:2] + '****' + '@' + domain
    return local + '@' + domain

df['telefono'] = df['telefono'].apply(mask_phone)
df['email'] = df['email'].apply(mask_email)

df.to_csv("base_freemium_paginada.csv", index=False, encoding='utf-8-sig')
logging.info("Proceso finalizado. CSV generado: base_freemium_paginada.csv")