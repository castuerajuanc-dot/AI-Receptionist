# -*- coding: utf-8 -*-
"""
FASE 1 - Scoring 0-100 de las 251 empresas del CSV de Google Maps.
Solo usa senales OBSERVABLES en el CSV: categoryName, website, title, address, reviewsCount.
El CSV NO trae rating, email ni telefono (columnas vacias) -> no se inventan.
"""
import csv, math, json, re, unicodedata

SRC = 'data/valencia_hvac_raw.csv'

def norm(s):
    s = unicodedata.normalize('NFKD', (s or '')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'\s+', ' ', s).strip()

rows = []
with open(SRC, encoding='utf-8-sig') as f:
    for i, r in enumerate(csv.DictReader(f)):
        r['_i'] = i
        r['rc'] = int(r['reviewsCount']) if (r['reviewsCount'] or '').strip().isdigit() else 0
        w = (r['website'] or '').strip()
        r['domain'] = re.sub(r'^www\.', '', w.replace('https://', '').replace('http://', '').split('/')[0]) if w else ''
        rows.append(r)

# ---------- 1. FILTRO ICP: fuera lo que no es empresa de servicios de climatizacion ----------
EXCLUDE_CAT = {
    'Taller de reparación de automóviles', 'Taller de automóviles', 'Taller mecánico',
    'Taller de chapa y pintura', 'Servicio de lavado de coches', 'Alojamiento',
    'Alquiler de vacaciones', 'Departamento', 'Gimnasio', 'Club de natación',
    'Centro deportivo', 'Polideportivo', 'Tienda de productos para mascotas',
    'Tienda de móviles', 'Tienda de electrónica', 'Tienda de electrodomésticos',
    'Servicio de reparación de televisores', 'Servicio de antenas', 'Cámara',
    'Asociación u organización', 'Empresa de escayolas', 'Proveedor de ventanas PVC',
    'Servicio de instalación de ventanas', 'Carpintería metálica y de aluminio',
    'Empresa de aislamientos', 'Servicio de seguridad', 'Compañía eléctrica',
    'Compañía del gas', 'Proveedor de repuestos de electrodomésticos',
}
# Dominios de portales / franquicias de electrodomesticos / marketplaces -> no son la web de una PYME de servicios
NON_OWN_DOMAIN = {
    'milar.es', 'euronics.es', 'tiendas.mielectro.es', 'g.co', 'facebook.com',
    'es.wallapop.com', 'holidu.de', 'br.bluepillow.com', 'valencia.blue',
    'irpropertymanagement.holidayfuture.com', 'sites.google.com',
}
WEAK_DOMAIN = {'sites.google.com', 'facebook.com', 'g.co', 'es.wallapop.com'}
# Fabricantes, mayoristas, distribuidores de recambio: no encajan en el ICP (no venden servicio con llamadas de cliente final)
EXCLUDE_NAME_PAT = re.compile(
    r'salvador escoda|baxi|trane aire|repuestos aire acondicionado|aacore supply|'
    r'recambios|levantina de suministros|^kide$|romedtec|apartamento|apartup|estudio |loft |'
    r'ruzafa centro|autolavado|taller primado|reparadores de maquinaria hosteleria|'
    r'clival|forza val|sei energia|frio y caliente: tienda', re.I)
# Alojamientos turisticos que Google clasifico raro
TOURISM_PAT = re.compile(r'wifi|balcon|balc|smart tv|apartamento|apartup|deluxe|encantador|luminoso', re.I)

CORE_CAT = {
    'Contratista de aire acondicionado': 20,
    'Empresa de climatización': 20,
    'Servicio de reparación de aire acondicionado': 19,
    'Empresa de calefacción': 17,
    'Proveedor de sistemas de aire acondicionado': 14,
    'Instalador de gas': 13,
    'Tienda de calderas': 12,
    'Tienda aire acondicionado': 11,
    'Fontanero': 11,
    'Electricista': 9,
    'Servicio de instalación eléctrica': 8,
    'Servicio de reparación de electrodomésticos': 8,
    'Contratista': 10,
    'Empresa de suministros industriales': 6,
    'Oficinas de empresa': 10,
    'Reformas': 7,
    '': 8,
}

def excluded(r):
    n = norm(r['title'])
    if r['categoryName'] in EXCLUDE_CAT: return 'categoria fuera de ICP'
    if EXCLUDE_NAME_PAT.search(n): return 'fabricante/mayorista/recambios/no-ICP'
    if TOURISM_PAT.search(r['title']) and 'clima' not in n: return 'alojamiento turistico'
    if r['domain'] in NON_OWN_DOMAIN and r['domain'] not in WEAK_DOMAIN: return 'cadena/franquicia o portal, no PYME de servicios'
    if r['categoryName'] not in CORE_CAT: return 'categoria no relevante'
    # fuera de la provincia de Valencia
    if 'Valencia' not in (r['address'] or '') and (r['address'] or '').strip(): return 'fuera de Valencia'
    return None

# ---------- 2. SCORING ----------
SERV_PAT = {
    'instalacion': re.compile(r'instalac|instalador|climatizacion|aire acondicionado|aerotermia|clima', re.I),
    'reparacion': re.compile(r'reparac|servicio tecnico|sat |mantenimiento|averia|urgencia|24h|24 horas', re.I),
    'calefaccion': re.compile(r'calefac|caldera|calentador|gas|ferroli|junkers|cointra|baxi', re.I),
    'refrigeracion_comercial': re.compile(r'refrigerac|frigorific|camara|frio|hosteleria|industrial', re.I),
    'renovables': re.compile(r'aerotermia|solar|energia|fotovoltaic|eficiencia', re.I),
    'ventilacion': re.compile(r'ventilac|extracc|humifred|humedad', re.I),
}
STRUCT_PAT = re.compile(r'\bs\.?\s?l\.?\b|\bs\.?\s?a\.?\b|\bsl\b|\bsa\b|\bs\.?c\.?\b|\bsal\b|grupo|showroom|hermanos|hnos|ingenieria|soluciones|integral|servicios', re.I)

def score(r):
    br = {}
    # A) Volumen de resenas (proxy de volumen de clientes/llamadas) 0-35, log-escalado
    rc = r['rc']
    br['A_resenas'] = round(min(35.0, 35.0 * math.log10(1 + rc) / math.log10(1 + 300)), 1) if rc else 0.0
    # B) Web propia 0-20
    d = r['domain']
    if not d: b = 0.0
    elif d in WEAK_DOMAIN: b = 6.0                       # perfil gratuito, no web propia
    elif re.search(r'\.(es|com|net|eu|pro)$', d): b = 20.0 if not d.endswith('.app') else 12.0
    else: b = 14.0
    # dominio que contiene la marca/servicio = web propia identificable
    br['B_web'] = b
    # C) Encaje de categoria ICP 0-20
    br['C_categoria'] = float(CORE_CAT.get(r['categoryName'], 5))
    # D) Amplitud de servicios detectable en nombre + dominio 0-15
    text = r['title'] + ' ' + d + ' ' + r['categoryName']
    hits = [k for k, p in SERV_PAT.items() if p.search(text)]
    br['D_servicios'] = round(min(15.0, 4.0 * len(hits)), 1)
    br['_servicios_detectados'] = hits
    # E) Senales de empresa estructurada 0-10
    e = 0.0
    if STRUCT_PAT.search(r['title']): e += 5
    if rc >= 100: e += 3
    elif rc >= 40: e += 2
    elif rc >= 15: e += 1
    if re.search(r'\b46\d{3}\b', r['address'] or ''): e += 2   # direccion fisica con CP = local real
    br['E_estructura'] = round(min(10.0, e), 1)
    total = sum(v for k, v in br.items() if not k.startswith('_'))
    return round(min(100.0, total), 1), br

out = []
for r in rows:
    ex = excluded(r)
    s, br = (0.0, {}) if ex else score(r)
    out.append(dict(idx=r['_i'], title=r['title'], category=r['categoryName'], website=r['website'],
                    domain=r['domain'], address=r['address'], reviews=r['rc'],
                    excluded=ex, score=s, breakdown=br))

json.dump(out, open('output/phase1_scores.json', 'w'), ensure_ascii=False, indent=1)
kept = [o for o in out if not o['excluded']]
kept.sort(key=lambda o: -o['score'])
print(f"Total filas: {len(out)} | Excluidas: {len(out)-len(kept)} | Candidatas ICP: {len(kept)}\n")
print(f"{'#':>3} {'score':>5} {'rev':>5}  {'empresa':46} {'dominio':34} servicios")
for n, o in enumerate(kept[:60], 1):
    print(f"{n:3d} {o['score']:5.1f} {o['reviews']:5d}  {o['title'][:46]:46} {(o['domain'] or '-')[:34]:34} {','.join(o['breakdown']['_servicios_detectados'])}")
