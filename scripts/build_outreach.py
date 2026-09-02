# -*- coding: utf-8 -*-
"""Campaña de validación: 10 prospectos + emails personalizados. NO envía nada."""
import csv, json

P = [
dict(
 company_name="Àrtic Refrigeració - Cámaras frigoríficas y aire acondicionado",
 email="info@articrefrigeracio.es", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://articrefrigeracio.es/", phone="+34 622 50 53 56",
 score=75,
 specific_signal="Su web anuncia «asistencia 24/7, todos los días de la semana» y, al mismo tiempo, horario de oficina de lunes a viernes de 09:00 a 18:00. Venden programas de mantenimiento preventivo desde 99 €/mes. Cartera de cámaras frigoríficas para hostelería, alimentación y panificadoras.",
 likely_pain="Prometen cobertura 24/7 con un horario de oficina de 9 a 18. En cámaras frigoríficas la avería es urgente de verdad (se pierde género), así que el cliente que no encuentra respuesta llama al siguiente número de su lista.",
 sales_angle="La contradicción publicada por ellos mismos: 24/7 frente a 9-18. No hay que convencerles de que el problema existe, ya lo han asumido comercialmente; solo falta preguntarles cómo lo cubren hoy.",
 subject_line="Asistencia 24/7 y horario de 9 a 18",
 email_body="""Hola,

Soy Juan. Estoy montando una herramienta para empresas de climatización y frío que coge las llamadas cuando no puede cogerlas nadie: apunta nombre, teléfono, dirección y qué le pasa al cliente, y os lo pasa como aviso.

He visto que ofrecéis asistencia 24/7 los siete días y que a la vez el horario de oficina es de lunes a viernes de 9 a 18. Con cámaras frigoríficas y clientes de hostelería, me imagino que las llamadas urgentes de verdad no esperan a la mañana siguiente.

Todavía estoy validando si esto es un problema real o me lo estoy inventando.

¿Te puedo hacer una pregunta? Cuando entra un aviso de una cámara un sábado por la tarde, ¿cómo lo gestionáis?

Un saludo,
Juan"""),

dict(
 company_name="Instalaciones Navarro Hermanos S.L.",
 email="contacto@instalacionesnavarrohnos.es", email_status="verified_public_email",
 contact_name="Helios Navarro y Manuel Navarro",
 contact_role="Segunda generación al frente de la empresa (publicado en su propia página «Acerca de»)",
 website="https://instalacionesnavarrohnos.es/", phone="963 663 909 / 686 469 722",
 score=72,
 specific_signal="Fundada en Valencia en 1975 por Pedro y José Navarro; hoy la llevan Helios y Manuel Navarro (segunda generación), según su propia web. Horario partido de 8:00 a 14:00 y de 16:00 a 20:00, sábados de 9:00 a 13:00. Instaladores autorizados por la Conselleria (fontanería, gas categoría A, RITE) y colaboradores de Saunier Duval, Vaillant y Baxi. Blog con instalaciones de suelo radiante y aerotermia.",
 likely_pain="Dos horas cerradas cada día a mediodía, más las noches y los domingos. En suelo radiante y aerotermia la consulta perdida no es una reparación de 80 €, es un proyecto de varios miles.",
 sales_angle="Los únicos del top 10 a los que se puede escribir por su nombre, y publicado por ellos mismos. Ticket alto: el argumento es el valor por lead, no el volumen.",
 subject_line="Una pregunta sobre las llamadas de 2 a 4",
 email_body="""Hola Helios, hola Manuel:

Soy Juan. Estoy desarrollando una herramienta para empresas de instalaciones que atiende las llamadas que entran cuando no hay nadie disponible y recoge los datos del cliente y el motivo, para que el aviso no se pierda.

He visto que lleváis desde 1975 y que el horario es de 8 a 14 y de 16 a 20, con el sábado por la mañana. Entre medias hay dos horas cerradas cada día, y en trabajos como suelo radiante o aerotermia una consulta que no se coge es un presupuesto grande que se va.

Estoy hablando con empresas para entender si esto pasa de verdad.

¿Qué hacéis normalmente con una llamada que entra a las tres de la tarde?

Un saludo,
Juan"""),

dict(
 company_name="Aircoval",
 email="info@aircovalvalencia.es", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://aircovalvalencia.es/", phone="961 133 997 / 679 530 814 / 640 824 607 / 640 016 370",
 score=70,
 specific_signal="Cuatro números de atención publicados entre fijo y móviles. Más de 20 años declarados. Venta, instalación, reparación y mantenimiento de climatización, incluidas torres de refrigeración, y visita inicial de asesoramiento gratuita.",
 likely_pain="Cuatro líneas publicadas es lo que hace una empresa a la que una sola no le basta. Ofrecen además visita de asesoramiento gratuita, que genera consultas entrantes que hay que recoger y filtrar.",
 sales_angle="El dato de los cuatro números es objetivo, verificable y difícil de rebatir. Abre la conversación sin necesidad de afirmar nada sobre sus pérdidas.",
 subject_line="Los cuatro números de Aircoval",
 email_body="""Hola,

Soy Juan. Estoy construyendo una herramienta para empresas de climatización que responde a las llamadas que nadie puede coger, apunta nombre, teléfono, dirección y motivo, y distingue si es una avería, una instalación o un mantenimiento.

He visto que tenéis varios números de atención publicados, cuatro contando fijo y móviles. Eso suele pasar cuando una sola línea no da abasto, y me hace pensar que en temporada alta se os cruzan bastantes llamadas mientras estáis en casa del cliente.

Estoy intentando validar si el problema existe de verdad antes de seguir construyendo.

¿Te puedo hacer una pregunta rápida? De esos números, ¿quién los coge cuando el equipo está instalando?

Un saludo,
Juan"""),

dict(
 company_name="Electricidad Gallardo",
 email="contacto@electricistasvalencia.eu", email_status="verified_public_email",
 contact_name="Jordi Gallardo",
 contact_role="Titular / electricista responsable — SIN VERIFICAR: el nombre aparece en directorios de terceros, no en su propia web. Por eso el email va con saludo neutro.",
 website="https://electricistasvalencia.eu/", phone="655 608 439",
 score=66,
 specific_signal="4,9 sobre 5 con más de 195 reseñas verificadas. Cartera de servicios muy amplia: electricista, contratista de aire acondicionado, calefacción, antenas, iluminación y solar. Ofrecen urgencias. Sábado y domingo cerrado (coinciden todas las fuentes; el horario de diario varía según la fuente).",
 likely_pain="Ofrecen urgencias pero cierran el fin de semana. Y con seis líneas de servicio distintas, el teléfono recibe consultas de tipos muy diferentes que alguien tiene que clasificar antes de mandar a un técnico.",
 sales_angle="Volumen alto y reputación excelente: tienen mucho que perder si una llamada se cae. El ángulo es el fin de semana y el filtrado por tipo de servicio.",
 subject_line="Las llamadas del fin de semana",
 email_body="""Hola,

Soy Juan. Estoy desarrollando una herramienta para empresas como la vuestra que coge las llamadas que no puede coger nadie, recoge los datos del cliente y el motivo, y responde las preguntas típicas que le hayáis configurado antes.

He visto que tenéis un 4,9 en Google con casi 200 reseñas y que cubrís bastante terreno: electricidad, aire acondicionado, calefacción, antenas, solar. También que atendéis urgencias, pero que el fin de semana está cerrado.

Estoy hablando con empresas de Valencia para entender si esto es un problema real o solo una idea mía.

¿Qué pasa con la llamada de un sábado por la mañana? ¿Se pierde, os deja mensaje, os llega de alguna forma?

Un saludo,
Juan"""),

dict(
 company_name="Técnicos Fernando Valencia",
 email="info@tecnicosvalencia.es", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://tecnicosvalencia.es/", phone="643 566 948",
 score=64,
 specific_signal="Su web anuncia «Valencia 24/7» para urgencias, con horario declarado de lunes a viernes de 8:00 a 19:00 y sábados de 9:00 a 14:00. Atienden viviendas y negocios, con instalación y reparación de aire acondicionado, termos, calentadores y electrodomésticos.",
 likely_pain="Segunda empresa del listado que anuncia 24/7 sobre un horario que no lo es. Además, el multiservicio genera muchas llamadas de consulta básica (precios, plazos, marcas) que hoy resuelve personal técnico.",
 sales_angle="Doble ángulo: la promesa 24/7 que no encaja con el horario, y el volumen de preguntas repetitivas que podrían responderse solas.",
 subject_line="24/7 con el equipo en la calle",
 email_body="""Hola,

Soy Juan. Estoy montando una herramienta para servicios técnicos que atiende las llamadas cuando no hay nadie libre: apunta nombre, teléfono, dirección y qué necesita el cliente, y clasifica si es urgencia, reparación o instalación.

He visto que en vuestra web ponéis «Valencia 24/7» para urgencias y que a la vez el horario es de 8 a 19, con el sábado hasta las 14. Trabajando con particulares y con negocios a la vez, imagino que el teléfono suena bastante mientras el técnico está metido en una reparación.

Estoy validando si el problema es real antes de seguir.

¿Te puedo preguntar una cosa? Cuando entra una urgencia y todo el mundo está trabajando, ¿qué hacéis con esa llamada?

Un saludo,
Juan"""),

dict(
 company_name="Climelectric Aire acondicionado Valencia",
 email="climelectricvalencia@gmail.com", email_status="possible_email",
 contact_name="", contact_role="",
 website="https://www.climelectric.com/", phone="963 766 379 / 960 659 140 / 632 194 082",
 score=63,
 specific_signal="596 reseñas, el mayor volumen del dataset entre empresas de servicio. Horario de lunes a viernes de 07:30 a 22:00, sábado y domingo cerrado. Tres números publicados. Ofrecen reparaciones con desplazamiento en menos de 24 horas desde la llamada. Más de 20 años, gama doméstica, comercial e industrial.",
 likely_pain="14 horas y media de atención de lunes a viernes y cero el fin de semana. Han construido su promesa comercial sobre la rapidez de respuesta («menos de 24 horas»), que es justo lo que se rompe el sábado.",
 sales_angle="El mayor volumen de clientes de la lista y una promesa de rapidez publicada. El hueco es el fin de semana, no el día a día.",
 subject_line="De 7:30 a 22:00 y luego el fin de semana",
 email_body="""Hola,

Soy Juan. Estoy desarrollando una herramienta para empresas de climatización que responde las llamadas que no puede coger nadie y recoge nombre, teléfono, dirección y motivo, para que el aviso quede registrado.

He visto que atendéis de 7:30 a 22:00 de lunes a viernes, que tenéis tres números publicados y que ofrecéis reparaciones con desplazamiento en menos de 24 horas. Es mucha disponibilidad. Lo que me pregunto es qué pasa el sábado y el domingo, que aparecéis cerrados, justo cuando a la gente se le estropea el aire.

Estoy hablando con empresas de Valencia para validar si esto es un problema de verdad.

¿Qué hacéis con las llamadas del fin de semana?

Un saludo,
Juan"""),

dict(
 company_name="Aire Clim",
 email="info@aireclim.com", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://aireclim.com/", phone="691 257 547",
 score=63,
 specific_signal="Captación multicanal ya montada: teléfono, formulario web y WhatsApp. Horario de lunes a viernes de 9:00 a 18:00, sábado y domingo cerrado. 4,9 sobre 5 con 128 reseñas. Declaran instalación en un día.",
 likely_pain="El cliente puede escribirles a cualquier hora por WhatsApp o formulario, pero la respuesta solo puede salir en horario de oficina. Cada noche y cada fin de semana se acumula una cola de consultas sin contestar.",
 sales_angle="Ya invierten en captación multicanal, así que no hay que explicarles el valor de un lead. El hueco es la respuesta, no la captación.",
 subject_line="Las consultas que entran después de las 18",
 email_body="""Hola,

Soy Juan. Estoy construyendo una herramienta para empresas de climatización que coge las llamadas cuando no hay nadie para cogerlas, apunta los datos del cliente y el motivo, y os pasa el aviso.

He visto que en la web ofrecéis contacto por teléfono, formulario y WhatsApp, y que el horario es de 9 a 18 de lunes a viernes. O sea, que el cliente os puede escribir a cualquier hora, pero la respuesta solo puede salir en horario de oficina.

Estoy intentando validar si ese hueco importa de verdad o si en la práctica no pasa nada.

¿Te puedo hacer una pregunta? Las consultas que entran por la tarde-noche o el fin de semana, ¿las recuperáis todas al día siguiente?

Un saludo,
Juan"""),

dict(
 company_name="Midasat Clima",
 email="info@midasatclima.com", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://www.midasatclima.com/", phone="963 953 470 / 671 942 415",
 score=62,
 specific_signal="Servicio técnico oficial de Immergas, Viessmann, Bronpi y Lasian, y también trabajan Audax, Cabel y Termat. Horario de lunes a jueves de 9:30 a 18:00 y viernes de 9:30 a 15:00. Segundo email publicado: administracion@midasatclima.com.",
 likely_pain="Los contratos de SAT oficial traen avisos derivados del fabricante con compromiso de respuesta. Ese flujo entra solo, no depende de su marketing, y el viernes a las 15:00 se corta hasta el lunes.",
 sales_angle="Volumen garantizado por contrato con fabricantes: el trabajo de registrar y clasificar avisos es puro coste administrativo. El corte del viernes es el gancho.",
 subject_line="Los avisos que entran el viernes por la tarde",
 email_body="""Hola,

Soy Juan. Estoy desarrollando una herramienta para servicios técnicos que atiende las llamadas que nadie puede coger: recoge nombre, teléfono, dirección y motivo, y separa si es una avería, un mantenimiento o una instalación.

He visto que sois servicio técnico oficial de Immergas, Viessmann, Bronpi y Lasian, entre otras marcas. Imagino que eso significa bastantes avisos entrando cada día. Y que el viernes cerráis a las 15:00, así que la tarde del viernes y el fin de semana quedan fuera.

Estoy hablando con empresas para entender si esto genera un problema real.

¿Qué pasa con un aviso que entra el viernes a las cinco de la tarde?

Un saludo,
Juan"""),

dict(
 company_name="AEROTERMIA y PLACAS SOLARES Flavio Severini (AeroClimaPro)",
 email="flavio@implica-t.com", email_status="possible_email",
 contact_name="Flavio Severini",
 contact_role="Fundador y responsable técnico (perfil propio de LinkedIn a nombre de AEROCLIMAPRO)",
 website="https://aeroclimapro.es/", phone="+34 672 35 34 35",
 score=61,
 specific_signal="Ofrecen estudio gratuito desde la web. Trabajan aerotermia, suelo radiante, aire acondicionado, placas solares, baterías de almacenamiento y cargadores para vehículo eléctrico. 16 años de experiencia declarados. Fundador identificado con LinkedIn activo.",
 likely_pain="El «estudio gratuito» es un imán de consultas, y quien las atiende es el mismo que está instalando. En proyectos de aerotermia cada consulta perdida vale mucho más que una reparación suelta.",
 sales_angle="Ticket alto y persona identificable: el argumento es el valor por lead. Un solo proyecto recuperado paga el servicio muchas veces.",
 subject_line="Los estudios gratuitos que no llegan a llamada",
 email_body="""Hola Flavio,

Soy Juan. Estoy montando una herramienta para instaladores que atiende las llamadas cuando no hay nadie libre: recoge nombre, teléfono, dirección y qué quiere el cliente, y os lo deja registrado como aviso.

He visto que ofrecéis estudio gratuito y que trabajáis aerotermia, suelo radiante, placas y cargadores de coche. Con proyectos de ese tamaño, cada consulta vale mucho más que una reparación suelta, y me imagino que buena parte entra por teléfono mientras estáis instalando.

Estoy validando si el problema existe de verdad antes de seguir construyendo nada.

¿Te puedo hacer una pregunta rápida? Cuando entra una llamada nueva y estás en una instalación, ¿qué sueles hacer con ella?

Un saludo,
Juan"""),

dict(
 company_name="Naper Climatización",
 email="napersc@gmail.com", email_status="verified_public_email",
 contact_name="", contact_role="",
 website="https://naper.pro/", phone="651 564 805",
 score=61,
 specific_signal="Página propia de «climatización para comercios»: tiendas, oficinas, peluquerías, clínicas y restaurantes, además de particulares. Más de 1.000 clientes declarados en su web y 4,8 sobre 5. Horario de lunes a viernes de 8:00 a 19:00, fines de semana cerrado. Cubren Valencia capital, Mislata, Burjassot, Sedaví y Benetússer.",
 likely_pain="Los comercios llaman cuando tienen el local abierto: tardes y sábados. Es justo cuando Naper está cerrada. Y una base de más de 1.000 clientes genera un flujo continuo de mantenimientos y averías que hoy se agenda a mano.",
 sales_angle="Tienen segmentado el cliente comercial en su propia web, así que ya distinguen el valor de un lead de comercio frente a uno residencial. El desajuste de horarios entre ellos y sus clientes es el ángulo.",
 subject_line="Los comercios llaman cuando vosotros habéis cerrado",
 email_body="""Hola,

Soy Juan. Estoy desarrollando una herramienta para empresas de climatización que responde las llamadas que no puede coger nadie, recoge los datos del cliente y el motivo, y os pasa el aviso ya clasificado.

He visto que además de particulares trabajáis climatización para comercios: tiendas, oficinas, peluquerías, clínicas y restaurantes. Ese cliente suele llamar cuando tiene el local abierto, muchas veces por la tarde o en sábado, y vosotros cerráis a las 19 y no abrís el fin de semana.

Estoy hablando con empresas de Valencia para validar si esto es un problema real.

¿Qué hacéis normalmente con la llamada de un comercio que entra fuera de vuestro horario?

Un saludo,
Juan"""),
]

assert len(P) == 10
for p in P:
    w = len(p['email_body'].split())
    assert 90 <= w <= 165, (p['company_name'], w)
    p['_words'] = w

HDR = ['company_name','email','email_status','contact_name','contact_role','website','phone',
       'specific_signal','likely_pain','sales_angle','subject_line','personalized_email']
with open('output/outreach_top10.csv','w',newline='',encoding='utf-8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL); wr.writerow(HDR)
    for p in P:
        wr.writerow([p['company_name'], p['email'], p['email_status'],
                     p['contact_name'] or 'sin persona identificable — usar email general',
                     p['contact_role'] or 'no aplica', p['website'], p['phone'],
                     p['specific_signal'], p['likely_pain'], p['sales_angle'],
                     p['subject_line'], p['email_body']])
json.dump(P, open('output/outreach_top10.json','w'), ensure_ascii=False, indent=1)
print("OK -> output/outreach_top10.csv")
for p in P: print(f"  {p['_words']:3d} palabras  {p['email_status']:22} {p['company_name'][:48]}")
