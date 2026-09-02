# -*- coding: utf-8 -*-
import json
P = json.load(open('output/outreach_top10.json'))
T = json.load(open('output/top30_enriched.json'))
sin_email = [r for r in T if r['email_status']=='no_email_found']

L=[]; W=L.append
W("# Campaña de validación — 10 primeros prospectos\n")
W("**Objetivo:** conseguir el primer cliente piloto. El objetivo de este primer email **no es vender ni cerrar**: "
  "es conseguir una conversación de 10 minutos y validar que el problema existe.\n")
W("**Propuesta:** «Te ayudamos a no perder clientes cuando nadie puede atender el teléfono.» "
  "En ningún email se menciona la palabra IA ni se vende tecnología.\n")
W("**Estado:** preparado para revisión humana. **No se ha enviado nada.**\n")
W("---\n")

W("## Qué se promete y qué no\n")
W("""Los emails solo mencionan lo que el producto hace hoy:

- Atender la llamada cuando no puede cogerla nadie
- Recoger nombre, teléfono, dirección y motivo
- Distinguir el tipo de aviso (avería, instalación, mantenimiento, urgencia)
- Responder preguntas básicas previamente configuradas
- Registrar el aviso
""")
W("\n**Deliberadamente NO se menciona la agenda de citas** ni la derivación a persona, porque la agenda "
  "figura como «potencialmente» en el alcance. Prometerla en el primer contacto sería vender algo que "
  "todavía no está validado. Todos los emails se presentan explícitamente como una fase de validación "
  "(«estoy validando», «estoy intentando entender si esto pasa de verdad»), lo que además baja la guardia "
  "del receptor: no le están vendiendo, le están preguntando.\n")
W("\nTampoco se afirma en ningún momento que pierdan llamadas. Se formula como hipótesis "
  "(«me imagino que…», «lo que me pregunto es…») y se cierra con una pregunta abierta.\n")
W("---\n")

W("## Cómo se eligieron estos 10\n")
W("El ranking del informe anterior medía *encaje de producto y tamaño*. Para una **campaña de email** hay "
  "dos criterios que pesan mucho más y que allí eran secundarios: poder escribir a alguien, y tener una "
  "señal concreta que citar. Por eso el orden cambia.\n")
W("""| Criterio | Peso | Cómo se midió |
|---|---|---|
| Dolor potencial por llamadas perdidas | 20 | Contradicción entre lo que prometen y su horario, o promesa de rapidez publicada |
| Volumen aparente de clientes | 20 | Reseñas de Google (escala log) |
| Horarios limitados | 12 | Horario real publicado: cierres a mediodía, fines de semana, viernes cortos |
| Urgencias / servicio 24 h | 12 | Que lo anuncien explícitamente en su web |
| Múltiples teléfonos | 8 | Números distintos publicados |
| Servicios de alto ticket | 10 | Aerotermia, suelo radiante, cámaras frigoríficas, obra |
| Tamaño / estructura | 8 | Forma jurídica, antigüedad, multisede, acreditaciones |
| Persona concreta contactable | 10 | Nombre y cargo publicados en fuente propia |
| Email público verificable | 10 | Verificado en dominio propio = 10 · por confirmar = 5 |
""")
W("**Se excluyeron de la campaña las 7 empresas sin email localizable**, por muy alta que fuera su "
  "puntuación general. Sin email no hay campaña de email:\n")
W("\n".join(f"- **{r['title']}** (nº {r['rank']} del top 30, {r['reviews']} reseñas) — {r['phone']}" for r in sin_email))
W("\nEntre ellas está **Grupo Aplus**, la nº 1 del ranking general. Es un prospecto excelente, pero solo "
  "publica formulario web: hay que trabajarla por teléfono, no por email. Merece su propia lista aparte.\n")
W("---\n")

W("## Los 10 prospectos\n")
W("| # | Empresa | Contacto | Email | Estado | Señal que se cita |")
W("|---|---|---|---|---|---|")
for i,p in enumerate(P,1):
    est = {'verified_public_email':'✅ verificado','possible_email':'⚠️ por confirmar'}[p['email_status']]
    per = p['contact_name'] or '—'
    if 'SIN VERIFICAR' in p['contact_role']: per += ' *(sin verificar)*'
    sig = p['specific_signal'].split('.')[0]
    W(f"| {i} | {p['company_name'][:44]} | {per} | `{p['email']}` | {est} | {sig} |")
W("")
W("---\n")
W("## Por qué contactaríamos a cada una\n")
for i,p in enumerate(P,1):
    W(f"### {i}. {p['company_name']}\n")
    W(f"**Señal concreta:** {p['specific_signal']}\n")
    W(f"**Dolor probable:** {p['likely_pain']}\n")
    W(f"**Ángulo de venta:** {p['sales_angle']}\n")
    W(f"**Asunto:** {p['subject_line']}\n")
    W("```")
    W(p['email_body'])
    W("```\n")
W("---\n")

W("## Antes de enviar — comprobaciones\n")
W("""1. **Confirmar los dos emails marcados «por confirmar»:**
   - `climelectricvalencia@gmail.com` (Climelectric) — localizado en el directorio Cylex, no en su web. En
     climelectric.com solo se ve formulario. Merece la pena mirar su página de contacto antes de escribir.
   - `flavio@implica-t.com` (AeroClimaPro) — el dominio no coincide con aeroclimapro.es. Puede ser correcto
     (otra sociedad del mismo grupo), pero conviene verificarlo.
2. **Electricidad Gallardo:** el nombre «Jordi Gallardo» viene de un directorio de terceros, no de su web.
   Por eso el email va con saludo neutro. Si se confirma el nombre, cambiar «Hola,» por «Hola Jordi,» sube
   bastante la tasa de respuesta.
3. **Aircoval:** el cuarto número (679 530 814) aparece en una sola fuente. El email dice «cuatro contando
   fijo y móviles»; si se prefiere ir sobre seguro, cambiar por «varios números».
4. **Revisar los horarios el día del envío.** Son el eje de casi todos los emails y cambian con la
   temporada. Citar un horario desactualizado destruye la credibilidad del email entero.
5. **Enviar desde un dominio propio** con SPF/DKIM configurados, y **espaciar los envíos** (3-4 al día, no
   los 10 de golpe).
6. **Sin adjuntos y sin enlaces** en el primer email: el objetivo es una respuesta, no un clic.
""")
W("## Orden de envío sugerido\n")
W("""**Día 1 — los tres de contradicción publicada.** Son los que menos hay que convencer, porque el problema
ya lo han asumido ellos en su propia web: Àrtic Refrigeració, Técnicos Fernando y Climelectric.

**Día 2 — los de persona identificable.** Un email dirigido a alguien por su nombre se responde más:
Instalaciones Navarro Hnos. (Helios y Manuel) y AeroClimaPro (Flavio).

**Día 3 — el resto:** Aircoval, Electricidad Gallardo, Aire Clim, Midasat y Naper.

Si a los 4-5 días no hay respuesta, un único seguimiento de dos líneas sobre el mismo hilo. Nada más:
son 10 empresas, no una campaña de volumen, y la reputación del dominio importa más que la insistencia.
""")
W("## Nota sobre el objetivo real\n")
W("""Estos 10 emails no son una campaña de ventas, son 10 entrevistas de descubrimiento disfrazadas de email
frío. La pregunta final de cada uno («¿qué hacéis con esa llamada?») está diseñada para que responder cueste
menos que ignorarlo, y para que la respuesta —sea la que sea— sirva para decidir si el producto merece
seguir construyéndose. Una respuesta del tipo «pues no nos pasa, tenemos a alguien en oficina» es tan
valiosa como un «sí, nos pasa cada semana».
""")
open('output/outreach_top10.md','w',encoding='utf-8').write("\n".join(L))
print("OK -> output/outreach_top10.md")
