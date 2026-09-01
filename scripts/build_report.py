# -*- coding: utf-8 -*-
import json, csv
T = json.load(open('output/top30_enriched.json'))
FUERA = json.load(open('output/casi_dentro.json'))
raw = list(csv.DictReader(open('data/valencia_hvac_raw.csv', encoding='utf-8-sig')))
ph1 = json.load(open('output/phase1_scores.json'))
n_all, n_exc = len(ph1), sum(1 for o in ph1 if o['excluded'])

ev = [r for r in T if r['email_status']=='verified_public_email']
ep = [r for r in T if r['email_status']=='possible_email']
ne = [r for r in T if r['email_status']=='no_email_found']
ph = [r for r in T if r['phone']]; wa=[r for r in T if r['whatsapp']]; nm=[r for r in T if r['contact_name']]
pct = lambda x: f"{len(x)}/30 ({len(x)/30*100:.0f} %)"

def tabla(rs, cols):
    out = ["| " + " | ".join(c[0] for c in cols) + " |",
           "|" + "|".join("---" for _ in cols) + "|"]
    for r in rs:
        out.append("| " + " | ".join(str(c[1](r)).replace("|","/") for c in cols) + " |")
    return "\n".join(out)

L = []
W = L.append
W("# Top 30 empresas de climatización de Valencia — informe de prospección\n")
W("**Producto a vender:** AI Receptionist para empresas de climatización (atiende llamadas entrantes, "
  "captura y califica leads, responde preguntas básicas, recupera oportunidades perdidas y agenda citas).\n")
W(f"**Fuente:** `data/valencia_hvac_raw.csv` — {n_all} fichas de Google Maps (Valencia), copia íntegra e "
  "inalterada del CSV original.\n")
W(f"**Entregables:** `output/valencia_hvac_top30_enriched.csv` (30 empresas, 19 columnas) y este informe.\n")
W("---\n")

W("## 0. Limitaciones a tener en cuenta antes de leer nada más\n")
W("Tres avisos que condicionan cómo hay que interpretar los datos:\n")
W("1. **El CSV no trae `rating`, ni `emails`, ni `phones`.** Las columnas `emails` y `phones` existen pero están "
  "vacías en las 251 filas, y no hay columna de valoración. Por tanto el scoring de Fase 1 **no usa rating** "
  "(no se ha inventado ninguno) y el 100 % de los emails y teléfonos del entregable procede de la Fase 3.\n")
W("2. **No he podido abrir las webs directamente.** La política de red de este entorno bloquea el acceso "
  "saliente a dominios externos (`EGRESS_BLOCKED`). El enriquecimiento se ha hecho con el buscador web, que sí "
  "recupera el contenido de las páginas de contacto oficiales. Es decir: los datos vienen de esas páginas, "
  "pero **no los he verificado abriendo la web yo mismo**. La columna `contact_source` guarda siempre la URL.\n")
W("3. **`email_status` codifica exactamente ese nivel de confianza:**\n")
W("   - `verified_public_email` — publicado en el dominio propio de la empresa (página de contacto).\n")
W("   - `possible_email` — localizado en un directorio de terceros, o en un dominio distinto al que figura "
  "en su ficha de Google Maps. **Confirmar antes de escribir.**\n")
W("   - `no_email_found` — no existe email público localizable; solo formulario y/o teléfono.\n")
W("\n---\n")

W("## 1. Cómo se hizo el scoring\n")
W("### Fase 1 — puntuación base 0–100 sobre las 251 fichas\n")
W("Solo con señales observables en el CSV (`categoryName`, `website`, `title`, `address`, `reviewsCount`). "
  "Cinco componentes:\n")
W("""| Componente | Peso | Qué mide y por qué |
|---|---|---|
| A. Volumen de reseñas | 0–35 | Único proxy disponible del volumen real de clientes, y por tanto de llamadas. Escala logarítmica: la diferencia entre 5 y 50 reseñas importa mucho más que entre 500 y 550 |
| B. Web propia | 0–20 | Dominio propio = 20. Perfil gratuito (Google Sites, Facebook, `g.co`, Wallapop) = 6. Sin web = 0. Una web propia indica inversión en captación y presupuesto |
| C. Encaje de categoría ICP | 0–20 | Contratista de A/A y empresa de climatización = 20; reparación de A/A = 19; calefacción = 17; tienda de A/A = 11; electricista/fontanero = 9–11 |
| D. Amplitud de servicios | 0–15 | Detección por palabras clave de seis líneas (instalación, reparación/SAT, calefacción, refrigeración comercial, renovables, ventilación). 4 puntos por línea |
| E. Señales de estructura | 0–10 | Forma jurídica en el nombre (S.L., S.A., «Grupo», «Hermanos», «Ingeniería»), tramo de reseñas y dirección física con código postal |
""")
W(f"**Filtro ICP previo:** se descartaron **{n_exc} de {n_all} fichas** ({n_exc/n_all*100:.0f} %) antes de puntuar, "
  f"quedando **{n_all-n_exc} candidatas** reales. Motivos de descarte:\n")
W("- **Talleres de automoción** (~55 fichas): «aire acondicionado del coche» contaminó la búsqueda. Fuera del ICP.\n")
W("- **Apartamentos turísticos** (~12): listados con «aire acondicionado» en el título como reclamo.\n")
W("- **Cadenas y franquicias de electrodomésticos** (Milar, Euronics, Mi Electro): venden producto, no prestan servicio; "
  "además la web es la del grupo, no de la tienda.\n")
W("- **Fabricantes y mayoristas** (Salvador Escoda, delegación comercial de BAXI, Trane, Kide, Levantina de Suministros, "
  "AACORE, tiendas de recambios): no reciben llamadas de cliente final que agendar.\n")
W("- **Ruido puro:** gimnasios, piscinas, tienda de mascotas, tienda de móviles, servicio de antenas.\n")

W("\n### Fase 3 — ajuste por enriquecimiento (±, reglas fijas)\n")
W("La puntuación final es `base + ajuste`. El ajuste **no es discrecional**: son reglas aplicadas por igual a "
  "todas, y cada señal está respaldada por la fuente citada en `contact_source`.\n")
W("""| Señal verificada | Ajuste |
|---|---|
| Email público verificado en dominio propio | +2 |
| Email localizado pero pendiente de confirmar | +1 |
| Ningún email público localizable | −1 |
| Opera desde varias sedes o provincias | +2 |
| Cartera comercial/industrial explícita (no solo residencial) | +2 |
| Señal directa de alto volumen telefónico (24 h declarado, 3+ líneas, base de clientes grande) | +2 |
| SAT oficial de fabricante, instaladora autorizada o asociación sectorial | +1 |
| Sociedad anónima (estructura mayor que la media del sector) | +1 |
| Interlocutor identificado con nombre y cargo públicos | +1 |
| Dominio o dirección que no coinciden con la ficha de Google Maps | −2 |
""")
W("**Prioridad de contacto**, por tramos de puntuación final: **A** ≥ 84 · **B** 77–83,9 · **C** < 77.\n")
W("\n---\n")

W("## 2. Las 10 empresas de mayor prioridad\n")
W(tabla(T[:10], [("#", lambda r: r['rank']), ("Empresa", lambda r: r['title']),
                 ("Score", lambda r: r['final']), ("Reseñas", lambda r: r['reviews']),
                 ("Email", lambda r: r['email'] or "—"), ("Estado", lambda r: r['email_status']),
                 ("Teléfono", lambda r: r['phone'])]))
W("")
W("### 3. Qué señal concreta metió a cada una en el top 10\n")
SIG = {
 1:"507 reseñas —el mayor volumen del dataset entre empresas de servicio puro— y delegaciones verificadas en Valencia, Alicante, Elche y Murcia. Estructura multi-provincia con equipo de ingenieros propio.",
 2:"596 reseñas, el volumen absoluto más alto. Publica **tres teléfonos distintos**: síntoma claro de canal telefónico saturado. Más de 20 años, gama doméstica e industrial.",
 3:"186 reseñas y captación ya multicanal (formulario + teléfono + WhatsApp) con web propia bien estructurada, pero cierra a las 18:00 y no abre fines de semana.",
 4:"258 reseñas y horario declarado 08:00–20:00 (12 h) con estructura pequeña. Titular identificado por nombre. Combina electricidad y climatización: más motivos de llamada.",
 5:"212 reseñas, S.L. con 20+ años y valoración pública 4,8. Horario partido 9–14 / 16–18: dos huecos diarios en plena temporada de averías.",
 6:"125 reseñas, instaladora autorizada por la Conselleria de Industria y colaboradora de Gas Natural, con cinco líneas de servicio (gas, calefacción, fontanería, clima, aerotermia).",
 7:"123 reseñas y el horario más amplio del top: L–V 08:00–19:00, sábados 09:00–14:00 y urgencias declaradas, con plantilla pequeña.",
 8:"194 reseñas en el nicho de mayor ticket (aerotermia + fotovoltaica). Fundador identificado con LinkedIn activo: entrada comercial personal, no genérica.",
 9:"90 reseñas y la única del top que declara abiertamente cartera de **oficinas, empresas y edificios de pública concurrencia** además de vivienda.",
 10:"95 reseñas y posicionamiento explícito de **urgencias 24 h** con línea dedicada. El coste de una llamada no atendida es aquí máximo y fácil de cuantificar.",
}
for r in T[:10]:
    W(f"**{r['rank']}. {r['title']}** ({r['final']} pts) — {SIG[r['rank']]}\n")

W("---\n")
W("## 4. Cobertura de datos de contacto (sobre las 30)\n")
W(f"""| Dato | Cobertura |
|---|---|
| **Email (verificado o posible)** | **{pct(ev+ep)}** |
| — de los cuales verificados en dominio propio | {pct(ev)} |
| — localizados pero pendientes de confirmar | {pct(ep)} |
| — sin email público localizable | {pct(ne)} |
| **Teléfono** | **{pct(ph)}** |
| WhatsApp público | {pct(wa)} |
| **Nombre de persona identificable** | **{pct(nm)}** |
""")
W("El teléfono está al 100 % porque en este sector es el canal principal y aparece en todas partes. "
  "El nombre propio es el dato escaso: solo 4 de 30 publican quién dirige la empresa.\n")
W("**Personas identificadas:**\n")
for r in T:
    if r['contact_name']:
        W(f"- **{r['contact_name']}** — {r['contact_role']} · {r['title']}")
W("")
W("---\n")

W("## 5. Los mejores primeros prospectos\n")
W("Aquí hay **dos capas distintas** y conviene no confundirlas. La columna `contact_priority` (A/B/C) es "
  "mecánica: sale del tramo de puntuación, que mide *encaje y tamaño*. Esta lista de cinco es un juicio "
  "comercial que además pondera **la intensidad del dolor**: por eso aparecen aquí empresas marcadas como B "
  "y C. Si se prefiere una regla única y automática, úsese la columna A/B/C; si se va a llamar personalmente "
  "esta semana, úsese esta lista.\n")
W("En este orden:\n")
W("""1. **Àrtic Refrigeració** (#14, 83,0) — *el mejor primer prospecto pese a no ser el de mayor score.* Es el
   único perfil 100 % B2B del listado: cámaras frigoríficas para hostelería, panificadoras y alimentación. Ahí
   una avería no es una incomodidad, es **pérdida de mercancía**, así que el cliente llama con urgencia y, si no
   responden, llama al siguiente. Y cierran a las 18:00 y los fines de semana, justo cuando la hostelería opera.
   El ROI se calcula solo. Además publican ofertas de empleo (equipo creciendo) y email corporativo verificado.
2. **Grupo Aplus** (#1, 95,0) — el de mayor puntuación y mayor estructura: 507 reseñas y cuatro delegaciones.
   Atienden «con cita previa» y no publican email: todo entra por teléfono. Contacto telefónico, no por email.
3. **Climelectric** (#2, 87,0) — 596 reseñas y **tres números publicados**. Ese detalle por sí solo abre la
   conversación: tres líneas es lo que hace una empresa que no da abasto con una.
4. **Instalaciones Navarro Hnos.** (#13, 83,2) — dos responsables identificados por nombre (Helios y Manuel
   Navarro, segunda generación desde 1975), email corporativo verificado y ticket alto (aerotermia, suelo
   radiante). La mejor combinación de *puedo escribir a una persona concreta* + *le duele perder un lead*.
5. **Arimax Climatización** (#28, 73,6) — baja en el ranking, pero anuncia **servicio 24 horas** con un único
   móvil y ningún email. Es la contradicción más fácil de señalar en una llamada: «¿cómo cubrís las 24 h que
   prometéis con un solo número?».
""")
W("---\n")

W("## 6. Patrones del mercado de climatización de Valencia\n")
W("""**a) El teléfono es el canal, y está desbordado.** 30 de 30 tienen teléfono público; solo 18 tienen email
verificado. Siete empresas del top 30 publican dos o tres números distintos. Nadie multiplica líneas si una
basta.

**b) Casi nadie cubre el horario en el que llama su cliente.** El patrón dominante es horario partido de
oficina (9–14 y 16–18/19), con el viernes por la tarde y el fin de semana cerrados. El particular descubre que
su aire no enfría al llegar a casa por la tarde o el fin de semana. Humifred atiende **solo de 9:00 a 14:00**;
stA+ atiende en Valencia hasta las 14:00 mientras en Madrid y Mallorca llega hasta las 20:00, dentro de la
misma empresa.

**c) Prometen 24 h con un móvil.** Varias (Arimax, Climelgas, Técnicos Fernando) anuncian urgencias 24 h o
servicio permanente sosteniéndose en un único número. Es una promesa comercial sin infraestructura detrás:
el hueco más señalable del mercado.

**d) La densidad de SAT oficiales es alta.** Midasat es SAT oficial de cuatro marcas a la vez (Immergas,
Viessmann, Bronpi, Lasian); Estracfrigus está en la red oficial Daikin; Grimaldos es SAT de Saivod. Estas
empresas reciben avisos derivados del fabricante con SLA de respuesta: volumen que entra solo y que hay que
registrar, agendar y confirmar. Es trabajo administrativo puro, el más automatizable del sector.

**e) El mercado se está desplazando a la aerotermia.** Aeroclimapro, Climavita, Climargas, Navarro Hnos.,
Clima Jover y Tecnoair la ofrecen explícitamente. Sube el ticket medio de cientos a miles de euros, y con él
el coste de perder un solo lead: el argumento de ROI deja de ser volumen y pasa a ser valor por lead.

**f) Mucha empresa antigua con web moderna y captación anticuada.** Hay S.L. y S.A. de 20–50 años (Mairo es
S.A. desde hace décadas, Navarro Hnos. desde 1975, Pertegás desde 2003) con web propia decente pero cuyo único
canal es un formulario que nadie contesta fuera de horario. Tienen presupuesto y estructura; les falta la capa
de atención.

**g) El «ruido» del dataset es enorme.** El 46 % de las fichas no eran del sector: talleres de coches,
apartamentos turísticos y tiendas de electrodomésticos. Cualquier campaña lanzada sobre el CSV en bruto habría
desperdiciado casi la mitad del esfuerzo.
""")
W("---\n")

W("## 7. Control de calidad\n")
W("### Duplicados y relaciones detectadas\n")
W("""- **`Clima Solution` (140 reseñas) y `Tu Servicio Técnico` (56)** comparten domicilio exacto: Gran Via del
  Marqués del Túria 49, 1º-1ª. Dos marcas del mismo operador con teléfonos y dominios distintos. **Se ha
  conservado solo Clima Solution** (la de mayor volumen) para no gastar dos huecos en el mismo comprador.
- **`Estracfrigus S.L.` (52) y `Frigus Air S.L.` (7)** comparten domicilio exacto: Camí Cases de Bàrcena 43.
  Conservada solo Estracfrigus.
- **`Reparacion Calderas Valencia` y `Reparación Caldera Valencia`** comparten el dominio
  `reparacioncalderasvalencia.eu`: dos fichas del mismo sitio. **Ambas descartadas** — la búsqueda no devolvió
  ningún dato de contacto ni rastro de empresa real; tiene toda la pinta de página SEO de captación.
- **`Servicio técnico Baxi Samsung…`** aparece dos veces en Sant Vicent Màrtir 85. Ambas descartadas (0 y 9
  reseñas, sin web).
- Fichas de cadena repetidas (Milar ×3, Euronics ×2, apartamentos de Holidu ×7) descartadas en el filtro ICP.
- **No hay `placeId` duplicados**: no hay duplicados exactos de ficha en el CSV.
""")
W("### Descartes deliberados pese a puntuación alta\n")
W("""- **Pascual Martí** (1.438 reseñas, la ficha con más reseñas de todo el CSV) — es una **cadena de tiendas de
  electrodomésticos** con cinco sucursales en la provincia; el email localizado es `administración@pascualmarti.es`.
  Vende e instala, pero el ICP pide empresa de servicios, no tienda. Fuera.
- **Saneamientos Orts** (290 reseñas) — **mayorista** de fontanería, calefacción y climatización con showroom.
  No presta el servicio técnico que genera las llamadas que resuelve el producto. Fuera.
- **«Servicio Técnico Oficial Ferroli–Cointra»** (`cointravalencia.com`, 75 reseñas) — **descartada por dudas de
  identidad**: la búsqueda indica que el SAT oficial de Cointra para Valencia y Castellón es COINSAT, en
  Paiporta, y no se pudo confirmar ningún dato de contacto en la dirección de la ficha (Av. General Avilés 23).
  Se prefiere excluirla antes que entregar un contacto no verificable.
- **Servicio Junkers Valencia** — descartada por el mismo motivo: los resultados devuelven media docena de
  teléfonos y emails contradictorios de agregadores SEO, ninguno atribuible con seguridad a la ficha.
""")
W("### Discrepancias marcadas (no resueltas, señaladas en el CSV)\n")
W("""- **Climatron** (#30): Google Maps la sitúa en C/ Ciscar 16 (Valencia); su web y los directorios, en
  **Burjassot**. Confirmar antes de visitar.
- **Clima Solution** (#11): la ficha enlaza `climasolution.net`, pero la web activa localizada es
  `climasolution.es` (misma marca y domicilio). Email marcado como `possible_email`.
- **Antonio Grimaldos** (#22): ficha con dominio `.es`, web localizada en `.com`, y **dos emails distintos**
  (`info@grimaldosclimatizacion.com` y `agv@metha.es`). Marcado `possible_email`.
- **Aeroclimapro** (#8): el email publicado está en el dominio `implica-t.com`, no en `aeroclimapro.es`.
  Marcado `possible_email`.
- **Electricidad Gallardo** (#4): Maps indica C/ del Navili 5; un directorio indica Padre Ferris 38. El
  teléfono y el email sí son consistentes entre fuentes.
- **Clima Soluciones Valencia** (#25): el nombre «Sergio Gassó Mota» procede de un registro empresarial y
  **no está verificado** como interlocutor; el email es una cuenta personal de Gmail. Confirmar antes de usar.
""")
W("### Qué no se ha hecho\n")
W("""- **No se ha modificado el CSV original.** Se trabajó sobre la copia `data/valencia_hvac_raw.csv`, en modo
  solo lectura (permisos 444).
- **No se ha inventado ningún dato.** No hay facturación, número de empleados, número de llamadas ni tamaño de
  plantilla en ninguna columna, porque nada de eso es observable ni verificable.
- **No se ha generado ningún email por patrón.** Ni un solo `nombre@empresa.com` deducido: todos los emails del
  entregable aparecen publicados en alguna fuente, y la fuente está en `contact_source`.
- **No se ha contactado con ninguna empresa** ni se ha escrito ningún mensaje de venta.
- **Rating de Google:** solo se ha rellenado en las tres empresas donde una fuente lo publicaba explícitamente
  (Layre 4,8 · Àrtic 4,9 · Naper 4,8), con la fuente indicada. En las 27 restantes figura «no disponible».
""")
W(f"\n### Investigadas pero fuera del top 30 por puntuación\n")
W("Se enriquecieron 33 candidatas y se conservaron las 30 de mayor puntuación final. Quedaron fuera por poco "
  "y sirven como reserva inmediata:\n")
for r in FUERA:
    W(f"- **{r['title']}** — {r['final']} pts, {r['reviews']} reseñas")
W("")
W("---\n")
W("## 8. Ranking completo (30)\n")
W(tabla(T, [("#", lambda r: r['rank']), ("Empresa", lambda r: r['title']),
            ("Score", lambda r: r['final']), ("Base", lambda r: r['base']),
            ("Ajuste", lambda r: f"{r['adj']:+d}"), ("Reseñas", lambda r: r['reviews']),
            ("Email", lambda r: {'verified_public_email':'verificado','possible_email':'por confirmar','no_email_found':'—'}[r['email_status']]),
            ("Prioridad", lambda r: r['prio'])]))
W("")
open('output/valencia_hvac_top30_report.md','w',encoding='utf-8').write("\n".join(L))
print("OK -> output/valencia_hvac_top30_report.md")
