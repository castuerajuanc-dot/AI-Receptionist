# Top 30 empresas de climatización de Valencia — informe de prospección

**Producto a vender:** AI Receptionist para empresas de climatización (atiende llamadas entrantes, captura y califica leads, responde preguntas básicas, recupera oportunidades perdidas y agenda citas).

**Fuente:** `data/valencia_hvac_raw.csv` — 251 fichas de Google Maps (Valencia), copia íntegra e inalterada del CSV original.

**Entregables:** `output/valencia_hvac_top30_enriched.csv` (30 empresas, 19 columnas) y este informe.

---

## 0. Limitaciones a tener en cuenta antes de leer nada más

Tres avisos que condicionan cómo hay que interpretar los datos:

1. **El CSV no trae `rating`, ni `emails`, ni `phones`.** Las columnas `emails` y `phones` existen pero están vacías en las 251 filas, y no hay columna de valoración. Por tanto el scoring de Fase 1 **no usa rating** (no se ha inventado ninguno) y el 100 % de los emails y teléfonos del entregable procede de la Fase 3.

2. **No he podido abrir las webs directamente.** La política de red de este entorno bloquea el acceso saliente a dominios externos (`EGRESS_BLOCKED`). El enriquecimiento se ha hecho con el buscador web, que sí recupera el contenido de las páginas de contacto oficiales. Es decir: los datos vienen de esas páginas, pero **no los he verificado abriendo la web yo mismo**. La columna `contact_source` guarda siempre la URL.

3. **`email_status` codifica exactamente ese nivel de confianza:**

   - `verified_public_email` — publicado en el dominio propio de la empresa (página de contacto).

   - `possible_email` — localizado en un directorio de terceros, o en un dominio distinto al que figura en su ficha de Google Maps. **Confirmar antes de escribir.**

   - `no_email_found` — no existe email público localizable; solo formulario y/o teléfono.


---

## 1. Cómo se hizo el scoring

### Fase 1 — puntuación base 0–100 sobre las 251 fichas

Solo con señales observables en el CSV (`categoryName`, `website`, `title`, `address`, `reviewsCount`). Cinco componentes:

| Componente | Peso | Qué mide y por qué |
|---|---|---|
| A. Volumen de reseñas | 0–35 | Único proxy disponible del volumen real de clientes, y por tanto de llamadas. Escala logarítmica: la diferencia entre 5 y 50 reseñas importa mucho más que entre 500 y 550 |
| B. Web propia | 0–20 | Dominio propio = 20. Perfil gratuito (Google Sites, Facebook, `g.co`, Wallapop) = 6. Sin web = 0. Una web propia indica inversión en captación y presupuesto |
| C. Encaje de categoría ICP | 0–20 | Contratista de A/A y empresa de climatización = 20; reparación de A/A = 19; calefacción = 17; tienda de A/A = 11; electricista/fontanero = 9–11 |
| D. Amplitud de servicios | 0–15 | Detección por palabras clave de seis líneas (instalación, reparación/SAT, calefacción, refrigeración comercial, renovables, ventilación). 4 puntos por línea |
| E. Señales de estructura | 0–10 | Forma jurídica en el nombre (S.L., S.A., «Grupo», «Hermanos», «Ingeniería»), tramo de reseñas y dirección física con código postal |

**Filtro ICP previo:** se descartaron **115 de 251 fichas** (46 %) antes de puntuar, quedando **136 candidatas** reales. Motivos de descarte:

- **Talleres de automoción** (~55 fichas): «aire acondicionado del coche» contaminó la búsqueda. Fuera del ICP.

- **Apartamentos turísticos** (~12): listados con «aire acondicionado» en el título como reclamo.

- **Cadenas y franquicias de electrodomésticos** (Milar, Euronics, Mi Electro): venden producto, no prestan servicio; además la web es la del grupo, no de la tienda.

- **Fabricantes y mayoristas** (Salvador Escoda, delegación comercial de BAXI, Trane, Kide, Levantina de Suministros, AACORE, tiendas de recambios): no reciben llamadas de cliente final que agendar.

- **Ruido puro:** gimnasios, piscinas, tienda de mascotas, tienda de móviles, servicio de antenas.


### Fase 3 — ajuste por enriquecimiento (±, reglas fijas)

La puntuación final es `base + ajuste`. El ajuste **no es discrecional**: son reglas aplicadas por igual a todas, y cada señal está respaldada por la fuente citada en `contact_source`.

| Señal verificada | Ajuste |
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

**Prioridad de contacto**, por tramos de puntuación final: **A** ≥ 84 · **B** 77–83,9 · **C** < 77.


---

## 2. Las 10 empresas de mayor prioridad

| # | Empresa | Score | Reseñas | Email | Estado | Teléfono |
|---|---|---|---|---|---|---|
| 1 | Grupo Aplus | 95.0 | 507 | — | no_email_found | 865 603 008 / 600 692 689 |
| 2 | Climelectric Aire acondicionado Valencia | 87.0 | 596 | climelectricvalencia@gmail.com | possible_email | 963 766 379 / 960 659 140 / 632 194 082 |
| 3 | Aire Clim | 86.1 | 186 | info@aireclim.com | verified_public_email | 691 257 547 |
| 4 | Electricidad Gallardo | 86.1 | 258 | contacto@electricistasvalencia.eu | verified_public_email | 655 608 439 |
| 5 | Layre | 85.9 | 212 | — | no_email_found | 688 91 93 23 |
| 6 | Climargas | 85.7 | 125 | info@climargas.es | verified_public_email | 961 939 219 |
| 7 | Técnicos Fernando Valencia | 85.6 | 123 | info@tecnicosvalencia.es | verified_public_email | 643 566 948 |
| 8 | AEROTERMIA y PLACAS SOLARES Flavio Severini | 85.3 | 194 | flavio@implica-t.com | possible_email | +34 672 35 34 35 |
| 9 | Viventia / Servicios Integrales | 84.7 | 90 | viventia@viventia.eu | verified_public_email | 963 680 491 |
| 10 | Climelgas Servicio Técnico de Valencia | 84.0 | 95 | — | no_email_found | 961 338 306 / 677 629 065 (urgencias) |

### 3. Qué señal concreta metió a cada una en el top 10

**1. Grupo Aplus** (95.0 pts) — 507 reseñas —el mayor volumen del dataset entre empresas de servicio puro— y delegaciones verificadas en Valencia, Alicante, Elche y Murcia. Estructura multi-provincia con equipo de ingenieros propio.

**2. Climelectric Aire acondicionado Valencia** (87.0 pts) — 596 reseñas, el volumen absoluto más alto. Publica **tres teléfonos distintos**: síntoma claro de canal telefónico saturado. Más de 20 años, gama doméstica e industrial.

**3. Aire Clim** (86.1 pts) — 186 reseñas y captación ya multicanal (formulario + teléfono + WhatsApp) con web propia bien estructurada, pero cierra a las 18:00 y no abre fines de semana.

**4. Electricidad Gallardo** (86.1 pts) — 258 reseñas y horario declarado 08:00–20:00 (12 h) con estructura pequeña. Titular identificado por nombre. Combina electricidad y climatización: más motivos de llamada.

**5. Layre** (85.9 pts) — 212 reseñas, S.L. con 20+ años y valoración pública 4,8. Horario partido 9–14 / 16–18: dos huecos diarios en plena temporada de averías.

**6. Climargas** (85.7 pts) — 125 reseñas, instaladora autorizada por la Conselleria de Industria y colaboradora de Gas Natural, con cinco líneas de servicio (gas, calefacción, fontanería, clima, aerotermia).

**7. Técnicos Fernando Valencia** (85.6 pts) — 123 reseñas y el horario más amplio del top: L–V 08:00–19:00, sábados 09:00–14:00 y urgencias declaradas, con plantilla pequeña.

**8. AEROTERMIA y PLACAS SOLARES Flavio Severini** (85.3 pts) — 194 reseñas en el nicho de mayor ticket (aerotermia + fotovoltaica). Fundador identificado con LinkedIn activo: entrada comercial personal, no genérica.

**9. Viventia | Servicios Integrales** (84.7 pts) — 90 reseñas y la única del top que declara abiertamente cartera de **oficinas, empresas y edificios de pública concurrencia** además de vivienda.

**10. Climelgas Servicio Técnico de Valencia** (84.0 pts) — 95 reseñas y posicionamiento explícito de **urgencias 24 h** con línea dedicada. El coste de una llamada no atendida es aquí máximo y fácil de cuantificar.

---

## 4. Cobertura de datos de contacto (sobre las 30)

| Dato | Cobertura |
|---|---|
| **Email (verificado o posible)** | **23/30 (77 %)** |
| — de los cuales verificados en dominio propio | 18/30 (60 %) |
| — localizados pero pendientes de confirmar | 5/30 (17 %) |
| — sin email público localizable | 7/30 (23 %) |
| **Teléfono** | **30/30 (100 %)** |
| WhatsApp público | 5/30 (17 %) |
| **Nombre de persona identificable** | **4/30 (13 %)** |

El teléfono está al 100 % porque en este sector es el canal principal y aparece en todas partes. El nombre propio es el dato escaso: solo 4 de 30 publican quién dirige la empresa.

**Personas identificadas:**

- **Jordi Gallardo** — Titular / electricista responsable (25+ anos de experiencia, segun fichas publicas) · Electricidad Gallardo
- **Flavio Severini** — Fundador / responsable tecnico (perfil LinkedIn propio de AEROCLIMAPRO) · AEROTERMIA y PLACAS SOLARES Flavio Severini
- **Helios Navarro y Manuel Navarro** — Segunda generacion al frente de la empresa (fundada por Pedro y Jose Navarro en 1975), segun la pagina 'Nosotros' de su web · Instalaciones Navarro Hermanos S.L.
- **Sergio Gasso Mota** — Posible administrador (inferido del registro empresarial; SIN VERIFICAR) · CLIMA SOLUCIONES VALENCIA S.L

---

## 5. Los mejores primeros prospectos

Aquí hay **dos capas distintas** y conviene no confundirlas. La columna `contact_priority` (A/B/C) es mecánica: sale del tramo de puntuación, que mide *encaje y tamaño*. Esta lista de cinco es un juicio comercial que además pondera **la intensidad del dolor**: por eso aparecen aquí empresas marcadas como B y C. Si se prefiere una regla única y automática, úsese la columna A/B/C; si se va a llamar personalmente esta semana, úsese esta lista.

En este orden:

1. **Àrtic Refrigeració** (#14, 83,0) — *el mejor primer prospecto pese a no ser el de mayor score.* Es el
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

---

## 6. Patrones del mercado de climatización de Valencia

**a) El teléfono es el canal, y está desbordado.** 30 de 30 tienen teléfono público; solo 18 tienen email
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

---

## 7. Control de calidad

### Duplicados y relaciones detectadas

- **`Clima Solution` (140 reseñas) y `Tu Servicio Técnico` (56)** comparten domicilio exacto: Gran Via del
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

### Descartes deliberados pese a puntuación alta

- **Pascual Martí** (1.438 reseñas, la ficha con más reseñas de todo el CSV) — es una **cadena de tiendas de
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

### Discrepancias marcadas (no resueltas, señaladas en el CSV)

- **Climatron** (#30): Google Maps la sitúa en C/ Ciscar 16 (Valencia); su web y los directorios, en
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

### Qué no se ha hecho

- **No se ha modificado el CSV original.** Se trabajó sobre la copia `data/valencia_hvac_raw.csv`, en modo
  solo lectura (permisos 444).
- **No se ha inventado ningún dato.** No hay facturación, número de empleados, número de llamadas ni tamaño de
  plantilla en ninguna columna, porque nada de eso es observable ni verificable.
- **No se ha generado ningún email por patrón.** Ni un solo `nombre@empresa.com` deducido: todos los emails del
  entregable aparecen publicados en alguna fuente, y la fuente está en `contact_source`.
- **No se ha contactado con ninguna empresa** ni se ha escrito ningún mensaje de venta.
- **Rating de Google:** solo se ha rellenado en las tres empresas donde una fuente lo publicaba explícitamente
  (Layre 4,8 · Àrtic 4,9 · Naper 4,8), con la fuente indicada. En las 27 restantes figura «no disponible».


### Investigadas pero fuera del top 30 por puntuación

Se enriquecieron 33 candidatas y se conservaron las 30 de mayor puntuación final. Quedaron fuera por poco y sirven como reserva inmediata:

- **Humifred Santacreu, S.L** — 72.4 pts, 16 reseñas
- **Airfutur** — 70.9 pts, 48 reseñas
- **RefriValencia** — 70.6 pts, 46 reseñas

---

## 8. Ranking completo (30)

| # | Empresa | Score | Base | Ajuste | Reseñas | Email | Prioridad |
|---|---|---|---|---|---|---|---|
| 1 | Grupo Aplus | 95.0 | 92.0 | +3 | 507 | — | A |
| 2 | Climelectric Aire acondicionado Valencia | 87.0 | 84.0 | +3 | 596 | por confirmar | A |
| 3 | Aire Clim | 86.1 | 84.1 | +2 | 186 | verificado | A |
| 4 | Electricidad Gallardo | 86.1 | 83.1 | +3 | 258 | verificado | A |
| 5 | Layre | 85.9 | 84.9 | +1 | 212 | — | A |
| 6 | Climargas | 85.7 | 82.7 | +3 | 125 | verificado | A |
| 7 | Técnicos Fernando Valencia | 85.6 | 81.6 | +4 | 123 | verificado | A |
| 8 | AEROTERMIA y PLACAS SOLARES Flavio Severini | 85.3 | 85.3 | +0 | 194 | por confirmar | A |
| 9 | Viventia / Servicios Integrales | 84.7 | 80.7 | +4 | 90 | verificado | A |
| 10 | Climelgas Servicio Técnico de Valencia | 84.0 | 83.0 | +1 | 95 | — | A |
| 11 | Clima Solution | 83.3 | 82.3 | +1 | 140 | por confirmar | B |
| 12 | Estracfrigus S L | 83.3 | 80.3 | +3 | 52 | verificado | B |
| 13 | Instalaciones Navarro Hermanos S.L. | 83.2 | 78.2 | +5 | 51 | verificado | B |
| 14 | Artic Refrigeració - Cámaras frigoríficas y aire acondicionado | 83.0 | 79.0 | +4 | 81 | verificado | B |
| 15 | stA+ Servicio Técnico de Electrodomésticos y Aire Acondicionado | 82.6 | 81.6 | +1 | 124 | — | B |
| 16 | Reparacion de Aire Acondicionado Valencia-DAVOFRIO | 82.5 | 78.5 | +4 | 45 | verificado | B |
| 17 | Naper Climatización | 81.6 | 77.6 | +4 | 105 | verificado | B |
| 18 | Mairo Valenciana de Climatización | 80.8 | 77.8 | +3 | 109 | verificado | B |
| 19 | Aircoval | 79.2 | 75.2 | +4 | 84 | verificado | B |
| 20 | Midasat Clima. | 78.7 | 75.7 | +3 | 55 | verificado | B |
| 21 | ElectroClima Valencia | 77.4 | 78.4 | -1 | 120 | — | B |
| 22 | Antonio Grimaldos S.L. | 75.9 | 75.9 | +0 | 41 | por confirmar | C |
| 23 | Servicio Técnico Mitsubishi Valencia - G&E | 75.6 | 75.6 | +0 | 54 | — | C |
| 24 | Novofrio SL | 75.2 | 70.2 | +5 | 11 | verificado | C |
| 25 | CLIMA SOLUCIONES VALENCIA S.L | 74.8 | 73.8 | +1 | 34 | por confirmar | C |
| 26 | CLIMAVITA - Soluciones de climatización | 74.4 | 72.4 | +2 | 27 | verificado | C |
| 27 | Climalem | 74.3 | 72.3 | +2 | 52 | verificado | C |
| 28 | Arimax Climatización | 73.6 | 72.6 | +1 | 54 | — | C |
| 29 | Pertegás Ventilación | 73.2 | 69.2 | +4 | 11 | verificado | C |
| 30 | Climatron - Aire Acondicionado Valencia | 72.9 | 70.9 | +2 | 41 | verificado | C |
