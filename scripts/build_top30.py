# -*- coding: utf-8 -*-
"""
FASE 2-4: ranking final de 30 empresas + enriquecimiento de contacto.
Todos los datos de contacto provienen de busqueda web publica (ver contact_source).
Nada esta inventado: lo no encontrado se marca explicitamente.
"""
import csv, json, sys
sys.path.insert(0,'scripts')
from fix_accents import fix

base = {o['idx']: o for o in json.load(open('output/phase1_scores.json'))}

def B(idx): return base[idx]

# (idx_csv, ajuste_enriquecimiento, motivo_ajuste, campos de contacto...)
R = [
dict(idx=5, adj=+4, adj_why="grupo multi-delegacion (Valencia/Alicante/Elche/Murcia) verificado; solo formulario, sin email publico",
 email="", email_status="no_email_found", phone="865 603 008 / 600 692 689", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.grupoaplus.es/contacto/ ; https://www.cylex.es/valencia/grupo-aplus-aire-acondicionado-valencia-13782714.html",
 rating="", fit="El mayor volumen de resenas del dataset entre empresas puras de servicio (507). Grupo con delegaciones en Valencia, Alicante, Elche y Murcia, equipo de ingenieros propio y cartera residencial + proyectos comerciales. Instalacion, reparacion y mantenimiento de climatizacion y energias renovables.",
 pain="Atencion 'con cita previa' y varias delegaciones: el telefono central concentra leads de 4 provincias. Cada llamada perdida fuera de horario es un presupuesto de instalacion completo que se va a la competencia.",
 note="Empresa con 507 resenas y delegaciones en 4 provincias (Valencia, Alicante, Elche, Murcia). Solo ofrecen formulario web, sin email directo: senal clara de que el telefono es el canal principal de entrada. Buen candidato para hablar de captacion multi-delegacion, calificacion de leads y recuperacion de llamadas perdidas fuera del horario de cita previa."),

dict(idx=15, adj=+3, adj_why="email + WhatsApp + nombre del fundador publicos y verificables",
 email="flavio@implica-t.com", email_status="possible_email", phone="+34 672 35 34 35", whatsapp="672 353 435",
 contact_name="Flavio Severini", contact_role="Fundador / responsable tecnico (perfil LinkedIn propio de AEROCLIMAPRO)",
 source="https://www.linkedin.com/in/flavio-severini-42281869/ ; https://aeroclimapro.es/ ; https://www.houzz.es/profesionales/servicios-de-climatizacion/solar-panels-and-aerotermia-flavio-severini-pfvwes-pf~1580984332",
 rating="", fit="194 resenas y especializacion en aerotermia + placas solares + aire acondicionado: ticket medio alto y ciclo de venta consultivo (estudios a medida). 16 anos de experiencia declarados. Persona de contacto identificada por nombre y cargo.",
 pain="Negocio de ticket alto que depende de captar y cualificar bien cada consulta. Un tecnico-fundador que atiende el telefono mientras instala pierde leads de aerotermia de varios miles de euros.",
 note="Aerotermia y fotovoltaica ademas de aire acondicionado: ticket medio alto y venta consultiva. Fundador identificado (Flavio Severini) con LinkedIn activo, lo que facilita un primer contacto personal. OJO: el email publicado esta en el dominio implica-t.com, no en aeroclimapro.es -> confirmar antes de escribir."),

dict(idx=12, adj=+3, adj_why="rating publico alto (4,8) y perfil B2B+B2C confirmado; sin email publico",
 email="", email_status="no_email_found", phone="688 91 93 23", whatsapp="",
 contact_name="", contact_role="",
 source="https://empresite.eleconomista.es/LAYRE-CLIMATIZACION.html ; https://www.oopiniones.com/aire-acondicionado-valencia-layre-climatizacion-sl-51012 ; https://www.facebook.com/LAYRECLIMATIZACION/",
 rating="4,8 (fuente: oopiniones.com, sin verificar en Google)",
 fit="212 resenas y mas de 20 anos en el mercado. Sociedad limitada (Layre Climatizacion S.L.) con clientes residenciales y comerciales, en climatizacion y ventilacion.",
 pain="Horario partido (9-14 y 16-18) con dos ventanas cerradas al dia: las llamadas de averia en verano se concentran justo en las horas sin cobertura.",
 note="S.L. consolidada, 212 resenas y 20+ anos, con horario partido 9-14 / 16-18. El hueco de mediodia y la tarde-noche son el argumento mas directo: en temporada alta de averias esas son horas de maxima demanda. Sin email publico, solo telefono: entrada por llamada."),

dict(idx=4, adj=+4, adj_why="email propio verificado en pagina de contacto + WhatsApp declarado",
 email="info@aireclim.com", email_status="verified_public_email", phone="691 257 547", whatsapp="Si (declarado en su web; numero no confirmado por separado)",
 contact_name="", contact_role="",
 source="https://aireclim.com/contacto/ ; https://aireclim.com/",
 rating="", fit="186 resenas, web propia bien estructurada con secciones de instalacion, climatizacion y servicio tecnico. Ofrece contacto por formulario, telefono y WhatsApp: ya trabaja captacion multicanal.",
 pain="Horario 9-18 de lunes a viernes, cerrado fines de semana. Ya usan WhatsApp y formulario, asi que reciben consultas 24/7 pero solo pueden responderlas en horario de oficina: cola de leads sin atender cada noche y cada fin de semana.",
 note="Ya captan por formulario + telefono + WhatsApp pero cierran a las 18:00 y no abren fines de semana. El discurso natural es: 'los leads siguen entrando cuando cerrais, quien los responde'. Email de contacto publico y verificado en su propia pagina."),

dict(idx=0, adj=+2, adj_why="mayor volumen de resenas de la categoria contratista; email solo en directorio",
 email="climelectricvalencia@gmail.com", email_status="possible_email", phone="963 766 379 / 960 659 140 / 632 194 082", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.cylex.es/valencia/climelectric-12855746.html ; https://www.climelectric.com/contactar",
 rating="", fit="596 resenas, el volumen mas alto entre empresas de servicio del dataset. Mas de 20 anos declarados, gama domestica y comercial/industrial, con mantenimiento, instalacion y reparacion. Tres numeros de telefono publicados: senal de varias lineas de entrada.",
 pain="Tres telefonos publicos y 596 resenas implican un flujo de llamadas alto y disperso. Sin un filtro previo, el equipo tecnico pierde horas en consultas que no acaban en trabajo.",
 note="596 resenas: probablemente el mayor flujo de clientes del dataset entre empresas de servicio puro. Publican TRES telefonos distintos, senal de que el canal telefonico esta saturado y sin cualificar. Email localizado en directorio (Cylex), no en su web: confirmar antes de usar."),

dict(idx=168, adj=+3, adj_why="email propio verificado + nombre del titular publico",
 email="contacto@electricistasvalencia.eu", email_status="verified_public_email", phone="655 608 439", whatsapp="",
 contact_name="Jordi Gallardo", contact_role="Titular / electricista responsable (25+ anos de experiencia, segun fichas publicas)",
 source="https://www.electricistabarato.es/electricidad-gallardo-valencia/ ; https://www.aireycalefaccion.es/empresa/electricidad-gallardo-valencia-4100366/ ; https://www.yelp.com/biz/electricidad-gallardo-valencia",
 rating="", fit="258 resenas con horario amplio (L-V 08:00-20:00). Combina electricidad con aire acondicionado y calefaccion, lo que multiplica los motivos de llamada entrante.",
 pain="12 horas de atencion declaradas al dia con un equipo pequeno: es imposible que alguien coja el telefono mientras estan en casa del cliente. Mezcla de urgencias electricas y climatizacion sin triaje.",
 note="258 resenas y horario declarado 08:00-20:00: prometen 12 horas de disponibilidad que un equipo pequeno no puede cubrir con el movil en la mano. Titular identificado (Jordi Gallardo). Email propio verificado. Encaje muy directo con 'no perder ninguna llamada y filtrar urgencias'."),

dict(idx=19, adj=-1, adj_why="emails ofuscados en los directorios; no se pudo obtener email publico",
 email="", email_status="no_email_found", phone="961 338 306 / 677 629 065 (urgencias)", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.serviciotecnicodevalencia.es/contacto/ ; https://www.paginasamarillas.es/f/valencia/climelgas-servicio-tecnico-de-valencia_231837089_000000001.html",
 rating="", fit="95 resenas. Servicio tecnico multiservicio con urgencias 24h: electrodomesticos, aire acondicionado y calefaccion, instalacion y reparacion. Dos direcciones publicadas en Valencia.",
 pain="Prometen asistencia 24 horas para urgencias del hogar. Ese compromiso solo se sostiene si alguien responde de madrugada; si no, la promesa se convierte en resenas negativas.",
 note="Se posicionan como urgencias 24 horas con una linea especifica de urgencias (677 629 065). Es el perfil donde el coste de una llamada no atendida es mas evidente y mas facil de cuantificar en la conversacion comercial."),

dict(idx=27, adj=+4, adj_why="email propio verificado + empresa instaladora autorizada (razon social identificada)",
 email="info@climargas.es", email_status="verified_public_email", phone="961 939 219", whatsapp="",
 contact_name="", contact_role="",
 source="http://climargas.es/contacto/ ; https://www.energias-renovables.com/empresas/climargas ; https://empresite.eleconomista.es/CLIMENT-MARTINEZ-GAS.html",
 rating="", fit="125 resenas. Razon social CLIMENT MARTINEZ GAS S.L.U., empresa instaladora autorizada por la Conselleria de Industria y colaboradora de Gas Natural. Cartera de servicios muy amplia: gas, calefaccion, fontaneria, climatizacion y aerotermia.",
 pain="Ser colaborador de Gas Natural y empresa autorizada genera llamadas de tramite (certificados, revisiones, altas) que saturan la linea y no siempre requieren un tecnico al telefono.",
 note="Instaladora autorizada por Conselleria y colaboradora de Gas Natural: mucha llamada de tramite y revision, ademas de averias. Cinco lineas de servicio (gas, calefaccion, fontaneria, clima, aerotermia) = muchas preguntas repetitivas que una recepcionista AI puede resolver sin pasar al tecnico."),

dict(idx=7, adj=+1, adj_why="email en dominio .es distinto al .net que figura en Google Maps; requiere confirmacion",
 email="info@climasolution.es", email_status="possible_email", phone="603 312 060 / 960 223 228", whatsapp="",
 contact_name="", contact_role="",
 source="https://climasolution.es/contactanos/ ; https://www.paginasamarillas.es/f/valencia/clima-solution_234284065_000000001.html",
 rating="", fit="140 resenas. Declaran 15+ anos de experiencia y cobertura de toda la provincia de Valencia, con instalacion, reparacion y mantenimiento para vivienda, comercio e industria.",
 pain="Cobertura provincial completa con oficina en el centro: el desplazamiento es caro y cada visita mal cualificada por telefono es un dia de tecnico perdido.",
 note="140 resenas y cobertura de toda la provincia con perfil residencial + comercial + industrial. AVISO: en Google Maps figura climasolution.net pero la web activa localizada es climasolution.es (mismo domicilio y marca) -> confirmar el dominio correcto antes de escribir."),

dict(idx=20, adj=+1, adj_why="WhatsApp publico y red multi-ciudad; sin email publico",
 email="", email_status="no_email_found", phone="624 274 900", whatsapp="624 274 900 (aceptan WhatsApp, declarado en su web)",
 contact_name="", contact_role="",
 source="https://serviciotecnico-aplus.com/ ; https://serviciotecnico-aplus.com/servicio-tecnico-multimarca-electrodomesticos-aire-acondicionado/",
 rating="", fit="124 resenas. Servicio tecnico multimarca independiente con unidades tecnicas propias en Valencia, Madrid y Mallorca: estructura operativa real de varias ciudades.",
 pain="En Valencia solo atienden de 8:00 a 14:00 (en Madrid y Mallorca hasta las 20:00). Media jornada de llamadas de Valencia queda sin cubrir mientras las otras plazas si atienden.",
 note="Operan Valencia, Madrid y Mallorca, pero en Valencia solo atienden de 8:00 a 14:00 frente a las 20:00 de las otras plazas. Argumento comercial listo: 'Valencia pierde media jornada de llamadas respecto a vuestras otras delegaciones'. Ya usan WhatsApp como canal."),

dict(idx=49, adj=+4, adj_why="email propio verificado, horario amplio y sabados",
 email="info@tecnicosvalencia.es", email_status="verified_public_email", phone="643 566 948", whatsapp="",
 contact_name="", contact_role="",
 source="https://tecnicosvalencia.es/contacto-instalaciones-reparaciones-televisores-lavadoras-frigorificos-secadoras-ordenadores-aires-acondicionados-termos-calentadores-antenas/ ; https://trustlocal.es/valencia/valencia/instalador-aire-acondicionado/tecnicos-fernando-valencia/",
 rating="", fit="123 resenas. Horario muy amplio: L-V 08:00-19:00 y sabados 09:00-14:00, con urgencias declaradas. Instalacion y reparacion de aire acondicionado, termos, calentadores y electrodomesticos.",
 pain="11 horas diarias mas sabados y urgencias con una plantilla pequena: el telefono suena mientras el tecnico esta en una reparacion. Alto volumen de llamadas repetitivas de bajo valor (precios, plazos, marcas).",
 note="Horario declarado 08:00-19:00 mas sabados y urgencias: prometen mucha disponibilidad con estructura pequena. Multiservicio (clima + electrodomesticos + termos) implica muchas llamadas de consulta basica facilmente automatizables. Email propio verificado."),

dict(idx=53, adj=+4, adj_why="email propio verificado y segmento B2B explicito (oficinas, empresas, edificios)",
 email="viventia@viventia.eu", email_status="verified_public_email", phone="963 680 491", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.viventia.eu/contacto/ ; https://infonif.economia3.com/telefono-direccion/valencia/viventia-servicios-integrales-sl",
 rating="", fit="90 resenas. S.L. de servicios integrales (energia, obras, fontaneria, reformas) que declara explicitamente instalacion y mantenimiento de climatizacion para viviendas, oficinas, empresas y edificios de publica concurrencia.",
 pain="Cartera B2B de mantenimiento: cada aviso de una oficina o comunidad entra por telefono y debe registrarse y priorizarse. Cierran a las 15:00 los viernes.",
 note="De las pocas del listado que declaran abiertamente cartera de empresas, oficinas y edificios de publica concurrencia, ademas de vivienda. El mantenimiento B2B genera avisos recurrentes que hay que registrar y priorizar: encaje directo con captura y calificacion automatica. Email corporativo verificado."),

dict(idx=25, adj=+3, adj_why="SAT oficial Daikin verificado en la red del fabricante + email en dominio propio",
 email="n.blanco@estracfrigus.es", email_status="verified_public_email", phone="963 663 286", whatsapp="",
 contact_name="", contact_role="",
 source="https://estracfrigus.es/index.php?s=contacto.php&tit=Contacto ; https://www.daikin.es/es_es/donde-encontrar-daikin/red-de-asistencia-tecnica/satos/estracfrigus-sl.html",
 rating="", fit="52 resenas. Aparece en la red oficial de asistencia tecnica de Daikin, lo que garantiza flujo continuo de avisos derivados del fabricante ademas de los propios. S.L. con instalaciones de fontaneria, refrigeracion y climatizacion.",
 pain="Ser SAT oficial de Daikin significa recibir avisos derivados que hay que registrar, agendar y confirmar. Ese trabajo administrativo por telefono es puro coste y es exactamente lo automatizable.",
 note="SAT dentro de la red oficial Daikin (verificado en daikin.es): recibe avisos derivados del fabricante ademas de los propios, con la carga administrativa de agendar y confirmar cada uno. Email en dominio propio (n.blanco@), lo que sugiere contacto directo con persona concreta."),

dict(idx=195, adj=+5, adj_why="perfil 100% B2B (hosteleria/alimentacion) + email propio verificado + rating publico 4,9",
 email="info@articrefrigeracio.es", email_status="verified_public_email", phone="+34 622 505 356", whatsapp="",
 contact_name="", contact_role="",
 source="https://articrefrigeracio.es/ ; https://www.paginasamarillas.es/f/valencia/artic-refrigeracio-camaras-frigorificas-y-aire-acondicionado_235226768_000000001.html",
 rating="4,9 (agregado publicado en su propia web sobre 79 resenas)",
 fit="81 resenas y el perfil mas claramente B2B del listado: camaras frigorificas y aire acondicionado para hosteleria, panificadoras y alimentacion. Publican ofertas de empleo, senal de equipo en crecimiento.",
 pain="En camaras frigorificas una averia es perdida de mercancia: el cliente llama con urgencia y, si no responden en minutos, llama al siguiente. Cierran a las 18:00 y no atienden fines de semana, cuando la hosteleria mas opera.",
 note="El caso B2B mas potente del listado: camaras frigorificas para hosteleria y alimentacion, donde una averia no atendida significa perdida de genero. Cierran a las 18:00 y fines de semana, justo cuando los bares y restaurantes estan abiertos. Ademas publican ofertas de empleo (equipo creciendo) y muestran 4,9/5 sobre 79 resenas."),

dict(idx=31, adj=+4, adj_why="multi-provincia verificado (Valencia/Alicante/Murcia) + email y WhatsApp propios",
 email="info@davofrio.com", email_status="verified_public_email", phone="960 002 033", whatsapp="673 549 318",
 contact_name="", contact_role="",
 source="https://www.davofrio.com/contacto/ ; https://www.davofrio.com/climatizacion/aire-acondicionado/reparacion-valencia/",
 rating="", fit="45 resenas en la ficha de Valencia pero estructura de ingenieria de climatizacion HVAC con sedes en Valencia, Alicante y Murcia. Instalacion, mantenimiento preventivo y correctivo.",
 pain="Tres provincias con una sola marca: los leads entran mezclados y hay que enrutar cada uno a la delegacion correcta antes de poder atenderlo.",
 note="Ingenieria de climatizacion HVAC con delegaciones en Valencia, Alicante y Murcia y web multiidioma. Ya tienen email y WhatsApp publicos: entienden la captacion digital. El gancho es el enrutado automatico de leads por provincia y la cualificacion previa de proyectos."),

dict(idx=29, adj=0, adj_why="email ofuscado en las fuentes; solo telefonos verificables",
 email="", email_status="no_email_found", phone="960 737 007 / 639 690 753", whatsapp="",
 contact_name="", contact_role="",
 source="https://electroclimavalencia.es/ ; https://www.electro-clima.es/contactar-electroclima.html",
 rating="", fit="120 resenas. Suministro e instalacion de climatizacion de todas las gamas y marcas, con cobertura de toda la provincia de Valencia.",
 pain="Atencion 9:00-17:00 de lunes a viernes: la franja de tarde-noche, cuando el particular llama al volver del trabajo, queda descubierta.",
 note="120 resenas con atencion declarada solo de 9:00 a 17:00 L-V. El particular que descubre que su aire no enfria llama al llegar a casa, entre las 18:00 y las 22:00, justo cuando no hay nadie. Publican dos lineas (fijo y movil) pero ningun email: la entrada es 100% telefonica."),

dict(idx=92, adj=+5, adj_why="email propio verificado, empresa familiar de 2a generacion con nombres publicos, cartera B2B (hosteleria)",
 email="contacto@instalacionesnavarrohnos.es", email_status="verified_public_email", phone="963 663 909 / 686 469 722", whatsapp="",
 contact_name="Helios Navarro y Manuel Navarro", contact_role="Segunda generacion al frente de la empresa (fundada por Pedro y Jose Navarro en 1975), segun la pagina 'Nosotros' de su web",
 source="https://instalacionesnavarrohnos.es/contacto/ ; https://instalacionesnavarrohnos.es/nosotros/",
 rating="", fit="51 resenas y 50 anos de historia (fundada en 1975). S.L. especializada en suelo radiante, aerotermia, calefaccion, solar, fontaneria y tratamiento de aguas. Su blog documenta trabajos en hosteleria: cartera B2B real.",
 pain="Horario partido 8-14 y 16-20 mas sabados por la manana: mucha franja abierta pero con huecos, y un negocio de instalaciones de ticket alto donde perder una consulta de aerotermia cuesta miles de euros.",
 note="Empresa familiar fundada en 1975, hoy en segunda generacion con dos responsables identificados por nombre (Helios y Manuel Navarro): permite un acercamiento personal y no generico. Ticket alto (suelo radiante, aerotermia) y trabajos documentados en hosteleria. Email corporativo verificado en su propia web."),

dict(idx=11, adj=+4, adj_why="sociedad anonima con CIF verificado y email corporativo propio",
 email="mairo@mairoclimatizacion.com", email_status="verified_public_email", phone="963 403 352", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.cylex.es/valencia/mairo-valenciana-de-climatizacion-s-a--11159073.html ; https://es.kompass.com/c/mairo-valenciana-de-climatizacion/es1301775/ ; https://empresite.eleconomista.es/MAIRO-VALENCIANA-CLIMATACION.html",
 rating="", fit="109 resenas. Es una SOCIEDAD ANONIMA (CIF A46222360), figura juridica poco habitual en el sector y senal de una estructura mayor y mas antigua que la media del listado. CNAE 4322: fontaneria, calefaccion y aire acondicionado.",
 pain="Estructura de S.A. con volumen de obra: el telefono mezcla clientes finales, proveedores y obra nueva sin ningun filtro previo.",
 note="Una de las dos unicas SOCIEDADES ANONIMAS del listado (CIF A46222360): estructura mas grande y antigua que la PYME tipica del sector, con capacidad presupuestaria real para un servicio de 300-500 EUR/mes. 109 resenas. Email corporativo en dominio propio."),

dict(idx=190, adj=+4, adj_why="email y horario propios verificados; base de clientes declarada +1000",
 email="napersc@gmail.com", email_status="verified_public_email", phone="651 564 805", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.naper.pro/contacto/ ; https://www.valenciaenamora.com/aire-acondicionado-naper-climatizacion-de-valencia/",
 rating="4,8 (declarado en su propia web)",
 fit="105 resenas y mas de 1.000 clientes declarados en Valencia. Instalacion, reparacion y mantenimiento de aire acondicionado y aerotermia. Web propia con pagina de servicios segmentada por tipo de cliente.",
 pain="Mas de 1.000 clientes con horario 8:00-19:00 y sin fines de semana. Una cartera de ese tamano genera un flujo constante de mantenimientos y averias que hay que agendar manualmente.",
 note="Declaran mas de 1.000 clientes en Valencia y 4,8/5. Una base instalada asi genera un flujo continuo de llamadas de mantenimiento y averia que hoy se agendan a mano. Segmentan su web por tipo de cliente (particulares/empresas), asi que entienden la diferencia de valor entre leads."),

dict(idx=215, adj=+1, adj_why="telefono verificado en multiples fuentes; email en dominio distinto al de Google Maps",
 email="info@grimaldosclimatizacion.com", email_status="possible_email", phone="963 950 794", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.paginasamarillas.es/f/valencia/antonio-grimaldos-s-l-_018633123_000000001.html ; https://www.grimaldosclimatizacion.com/ ; https://www.cylex.es/valencia/antonio-grimaldos-s-l--11254003.html",
 rating="", fit="41 resenas. S.L. con larga trayectoria que cubre las tres patas del ICP: instalacion, reparacion y mantenimiento de climatizacion, calefaccion y ACS. Ademas es SAT de marca (Saivod, solo aire acondicionado).",
 pain="Ser servicio tecnico de marca genera avisos derivados con obligacion de respuesta rapida; la ficha telefonica aparece incluso en webs de identificacion de llamadas, senal de alto volumen de trafico telefonico.",
 note="Cubre instalacion + reparacion + mantenimiento (el triple perfil que mejor encaja) y ademas es SAT de marca. AVISO: en Google Maps figura grimaldosclimatizacion.es pero la web localizada es el .com; se han encontrado dos emails distintos (info@grimaldosclimatizacion.com y agv@metha.es) -> confirmar cual esta operativo."),

dict(idx=8, adj=+4, adj_why="SAT oficial de 4 marcas + email propio verificado",
 email="info@midasatclima.com", email_status="verified_public_email", phone="963 953 470 / 671 942 415", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.midasatclima.com/contacto.php ; https://www.midasatclima.com/servicios.html ; https://empresite.eleconomista.es/MIDASAT-CLIMA.html",
 rating="", fit="55 resenas. S.L. que es servicio tecnico OFICIAL de cuatro marcas a la vez (Immergas, Viessmann, Bronpi, Lasian) para Valencia y provincia: flujo garantizado de avisos derivados. Gas, calefaccion, aire acondicionado y solar.",
 pain="Cuatro contratos de SAT oficial concentran mucho aviso entrante con SLA de respuesta. Cierran los viernes a las 15:00 y no atienden tardes de viernes ni fines de semana.",
 note="Servicio tecnico OFICIAL de cuatro fabricantes (Immergas, Viessmann, Bronpi, Lasian) para Valencia y provincia: el volumen de avisos derivados no depende de su marketing, entra solo. Cierran viernes a las 15:00. Encaje muy claro con registro y agendado automatico de avisos."),

dict(idx=222, adj=0, adj_why="telefono verificado, sin email publico localizable",
 email="", email_status="no_email_found", phone="963 125 526", whatsapp="",
 contact_name="", contact_role="",
 source="https://serviciodereparacion.es/servicio-tecnico-mitsubishi-electric-valencia/ ; https://www.cylex.es/valencia/servicio-t%C3%A9cnico-mitsubishi-valencia---g-e-14501600.html",
 rating="", fit="54 resenas. Servicio tecnico especializado en Mitsubishi Electric, marca premium de climatizacion: cliente final con equipos caros y expectativa alta de servicio.",
 pain="Se posicionan sobre una marca premium pero el unico canal de contacto publico es el telefono, sin email ni formulario visible. Toda la captacion depende de que alguien descuelgue entre las 8:00 y las 18:00.",
 note="Especialistas en una sola marca premium (Mitsubishi Electric): clientes con equipos de alto valor y poca tolerancia a esperar. No publican ningun email, solo telefono: el 100% de sus leads depende de descolgar. Argumento directo sobre llamadas perdidas."),

dict(idx=191, adj=+4, adj_why="doble email (propio + gmail) y tres lineas telefonicas verificadas",
 email="info@aircovalvalencia.es", email_status="verified_public_email", phone="961 133 997 / 640 824 607 / 640 016 370", whatsapp="",
 contact_name="", contact_role="",
 source="https://aircovalvalencia.es/ ; https://www.paginasamarillas.es/f/valencia/aircoval_225677624_000000001.html ; https://www.cylex.es/valencia/aircoval-12869951.html",
 rating="", fit="84 resenas y mas de 20 anos declarados. Instalacion, mantenimiento y reparacion. Tienen incluso una pagina dedicada a 'empresas de aire acondicionado en Valencia': trabajan el posicionamiento activamente.",
 pain="Publican TRES numeros de telefono y un horario partido muy fragmentado (10-14 y 16:30-19, viernes solo manana). Un cliente que llame un viernes por la tarde no encuentra a nadie en ninguna de las tres lineas.",
 note="Tres lineas telefonicas publicadas y horario partido muy fragmentado (viernes solo manana). Ese patron -multiples numeros + horario roto- es la senal clasica de llamadas que se escapan. Invierten en SEO propio, asi que ya pagan por generar leads que despues no siempre pueden atender."),

dict(idx=241, adj=+1, adj_why="email de tipo personal encontrado en registro empresarial; requiere confirmacion",
 email="sergiogassomota@gmail.com", email_status="possible_email", phone="611 078 013", whatsapp="",
 contact_name="Sergio Gasso Mota", contact_role="Posible administrador (inferido del registro empresarial; SIN VERIFICAR)",
 source="https://climasolucionesvalencia.com/contacto/ ; https://empresite.eleconomista.es/CLIMA-SOLUCIONES-VALENCIA.html",
 rating="", fit="34 resenas. S.L. constituida que combina distribucion y venta con instalacion, reparacion, mantenimiento y montaje de instalaciones termicas: ventilacion, aire acondicionado, calderas y calentadores.",
 pain="Estructura pequena con un unico movil de contacto: cuando el responsable esta instalando, no hay nadie atendiendo la linea comercial.",
 note="S.L. con actividad de instalacion y mantenimiento termico ademas de venta. El unico contacto localizado es un movil y un email personal: senal de que la atencion depende de una sola persona. OJO: el nombre y cargo proceden de un registro empresarial y NO estan verificados; confirmar antes de personalizar."),

dict(idx=225, adj=+2, adj_why="empresa familiar con 20+ anos y telefonos verificados; email ofuscado en las fuentes",
 email="", email_status="no_email_found", phone="963 349 064 / 651 840 693", whatsapp="",
 contact_name="", contact_role="",
 source="https://humifred.com/ ; https://www.cylex.es/valencia/humifred-santacreu-s-l--11244661.html ; https://ieferia.interempresas.net/Climatizacion/Contacto-Humifred-Santacreu-S-L-876094.html",
 rating="", fit="16 resenas pero perfil de empresa solida: S.L. familiar desde 2001, con importacion, distribucion, instalacion, mantenimiento y reparacion de aire acondicionado y refrigeracion. Presencia en portales profesionales del sector (Interempresas).",
 pain="Atencion solo de 9:00 a 14:00: cinco horas al dia. Mas de la mitad de la jornada laboral tipica de sus clientes queda sin cobertura telefonica.",
 note="Atienden solo de 9:00 a 14:00, la franja de atencion mas corta de todo el top 30. Empresa familiar desde 2001 con actividad de distribucion ademas de servicio, y presencia en portales profesionales del sector. El argumento de cobertura horaria aqui es casi automatico."),

dict(idx=208, adj=+2, adj_why="declaran servicio 24 horas y WhatsApp; sin email publico",
 email="", email_status="no_email_found", phone="651 020 311", whatsapp="651 020 311 (WhatsApp declarado en su web)",
 contact_name="", contact_role="",
 source="https://arimaxclimatizacion.es/ ; https://www.paginasamarillas.es/f/valencia/arimax-climatizacion_231852674_000000001.html",
 rating="", fit="54 resenas. Instalacion, reparacion y mantenimiento de climatizacion y refrigeracion, con servicio declarado 24 horas y captacion por formulario y WhatsApp.",
 pain="Anuncian servicio 24 horas con un unico movil de contacto. O alguien duerme con el telefono, o la promesa de 24h no se cumple: es el hueco mas facil de senalar en una conversacion comercial.",
 note="Anuncian SERVICIO 24 HORAS pero publican un solo movil y ningun email. Es el perfil ideal para la conversacion: 'como cubris las 24 horas que prometeis con un unico numero'. Ya usan WhatsApp, asi que aceptan canales automatizados."),

dict(idx=3, adj=+3, adj_why="email propio verificado; nicho de aerotermia (ticket alto)",
 email="info@climavita.es", email_status="verified_public_email", phone="614 325 787", whatsapp="",
 contact_name="", contact_role="",
 source="https://climavita.es/ ; https://cys-climavita.com/",
 rating="", fit="27 resenas. Climatizacion y aerotermia para viviendas, con web propia orientada a soluciones y proyecto a medida. Ticket medio alto por el peso de la aerotermia.",
 pain="Negocio de proyectos de aerotermia con un unico movil publicado: cada consulta perdida es un proyecto de varios miles de euros, no una reparacion de 80 EUR.",
 note="Especializados en aerotermia para vivienda: pocos leads pero de valor muy alto, lo que hace que perder uno duela mucho mas que en reparacion. Un unico movil de contacto y email propio verificado. Buen candidato para hablar de ROI por lead recuperado, no por volumen."),

dict(idx=1, adj=+3, adj_why="email propio verificado, horario amplio con sabados y ambito nacional declarado",
 email="info@climalem.es", email_status="verified_public_email", phone="963 858 895 / 695 666 438", whatsapp="",
 contact_name="", contact_role="",
 source="https://climalem.es/ ; https://www.paginasamarillas.es/f/valencia/climalem_235165719_000000001.html ; https://empresite.eleconomista.es/CLIMALEM.html",
 rating="", fit="52 resenas. Venta e instalacion de climatizacion con sede en Valencia y operacion declarada en practicamente todo el territorio nacional. Tecnicos con 24+ anos de experiencia. Abren sabados de 9 a 14.",
 pain="Atienden solo con cita previa segun su propia ficha de Google, y operan a nivel nacional desde una sede: filtrar y agendar correctamente cada consulta es critico para no desplazar tecnicos en balde.",
 note="Su ficha de Google indica expresamente 'atencion al publico con cita previa': todo su modelo depende de agendar bien. Operan desde Valencia a nivel nacional y abren sabados. La agenda automatica de citas es aqui el argumento central, mas que las llamadas perdidas."),

dict(idx=189, adj=0, adj_why="solo formulario web, sin email publico; telefonos verificados",
 email="", email_status="no_email_found", phone="963 504 298 / 654 117 522", whatsapp="",
 contact_name="", contact_role="",
 source="http://www.airfutur.com/CONTACTO/ ; https://www.paginasamarillas.es/f/valencia/air-futur_200821247_000000001.html ; https://www.cylex.es/valencia/air-futur-11252780.html",
 rating="", fit="48 resenas. Cubre las tres actividades del ICP a la vez segun su clasificacion: reparacion de aire acondicionado, contratista de aire acondicionado y empresa de climatizacion, con local propio.",
 pain="Horario partido corto (9:30-13:30 y 16:30-19:30) y cerrado los sabados, con contacto unicamente por formulario web y telefono. Web muy basica que no captura informacion del cliente.",
 note="Horario partido corto y cerrado sabados, con una web tecnicamente antigua cuyo unico canal es un formulario. Cubren instalacion, reparacion y climatizacion general. Perfil de empresa consolidada con captacion digital claramente mejorable: buen candidato para mostrar el antes/despues."),

dict(idx=17, adj=-1, adj_why="email ofuscado en las fuentes; solo telefono de directorio",
 email="", email_status="no_email_found", phone="641 937 004", whatsapp="",
 contact_name="", contact_role="",
 source="https://www.cylex.es/valencia/refrivalencia-13858491.html ; https://refrivalencia.com/ ; https://firmania.es/valencia/refrivalencia-1828612",
 rating="", fit="46 resenas. Empresa de climatizacion, aire acondicionado, calefaccion y ventilacion con web propia y local en Benimaclet.",
 pain="Solo se ha podido localizar un movil como via de contacto y ningun email publico: dependencia total del telefono para entrar en la empresa.",
 note="Cartera de cuatro lineas (clima, aire acondicionado, calefaccion, ventilacion) con web propia, pero el unico contacto localizable publicamente es un movil. Dependencia total del telefono. Prioridad B: verificar telefono en su web antes de llamar, ya que procede de directorio."),
]

# ---------- 3 backups (prioridad C) para completar el top 30 ----------
R += [
dict(idx=33, adj=+2, adj_why="email publico verificado y 30+ anos declarados",
 email="climatronsoluciones@gmail.com", email_status="verified_public_email", phone="669 777 750", whatsapp="",
 contact_name="", contact_role="",
 source="https://climatron.net/ ; https://www.qdq.com/climatron-1189986 ; https://burjassot.comercioscomunitatvalenciana.com/es/comercios/view/climatron",
 rating="", fit="41 resenas y mas de 30 anos de experiencia declarados. Instalacion, sustitucion, reparacion y mantenimiento de conductos, Airzone, split, multisplit y cassette, en viviendas Y locales comerciales.",
 pain="Un unico movil de contacto para cuatro tipos de servicio y dos segmentos (hogar y local comercial), sin ningun filtro previo de la consulta.",
 note="30+ anos y trabajo tanto en vivienda como en local comercial, con gama tecnica amplia (conductos, Airzone, multisplit, cassette). AVISO: Google Maps la situa en C/ Ciscar 16 (Valencia) pero su web y los directorios la situan en Burjassot -> confirmar la direccion real antes de visitar."),

dict(idx=41, adj=+2, adj_why="email corporativo verificado y perfil industrial B2B",
 email="instalaciones@novofrio.com", email_status="verified_public_email", phone="963 910 001", whatsapp="",
 contact_name="", contact_role="",
 source="https://novofrio.com/contacto/ ; https://www.aefyt.es/index.php/directorio-de-empresas/34-novofrio-sl ; https://empresite.eleconomista.es/NOVOFRIO.html",
 rating="", fit="Pocas resenas (11) pero S.L. con perfil industrial solido: instalaciones y mantenimiento de frio y climatizacion, y miembro del directorio de AEFYT (asociacion sectorial de frio y tecnologia). Cliente tipico B2B con contratos de mantenimiento.",
 pain="Negocio de contratos de mantenimiento industrial donde los avisos entran por telefono en horario 8-17 y cada parada de equipo tiene coste directo para el cliente.",
 note="Perfil B2B industrial (frio y climatizacion) y miembro de AEFYT, la asociacion sectorial. Pocas resenas de Google porque su cliente es empresa, no particular: no penalizar por ello. El valor aqui esta en la gestion de avisos de mantenimiento con contrato, no en captacion de leads nuevos."),

dict(idx=69, adj=+2, adj_why="email corporativo verificado, nicho B2B tecnico y dos lineas fijas",
 email="pertegas@pertegas.com", email_status="verified_public_email", phone="963 692 062 / 963 931 083", whatsapp="",
 contact_name="", contact_role="",
 source="https://pertegas.com/index.php?s=contacto.php&tit=Contacto ; https://pertegas.com/ ; https://www.lomejordelbarrio.com/benimaclet/climatizacion/pertegas-climatizacion",
 rating="", fit="Solo 11 resenas, pero empresa creada en 2003 y especializada en un nicho tecnico de alto valor: presurizacion de vias de evacuacion, ventilacion de sotanos y garajes y ventilacion industrial en naves, ademas de climatizacion y mantenimientos.",
 pain="Cliente B2B (comunidades, naves, garajes) con normativa de por medio: muchas llamadas de consulta tecnica y de mantenimiento obligatorio que hoy resuelve personal cualificado al telefono.",
 note="Nicho tecnico B2B (presurizacion de vias de evacuacion, ventilacion industrial y de garajes) con seccion propia de mantenimientos. Dos lineas fijas y email corporativo. Pocas resenas porque su cliente es profesional: el valor esta en filtrar consultas tecnicas y gestionar los mantenimientos recurrentes."),
]


# ---------- AJUSTE DE ENRIQUECIMIENTO (FASE 3): reglas uniformes, no discrecionales ----------
# Cada senal esta VERIFICADA en las fuentes citadas en contact_source.
REGLAS = {
 'email_verificado':  ( 2, "email publico verificado en dominio propio"),
 'email_posible':     ( 1, "email localizado pero pendiente de confirmar"),
 'sin_email':         (-1, "ningun email publico localizable"),
 'multisede':         ( 2, "opera desde varias sedes/provincias (estructura real)"),
 'b2b':               ( 2, "cartera comercial/industrial explicita, no solo residencial"),
 'acreditacion':      ( 1, "SAT oficial de fabricante, instaladora autorizada o asociacion sectorial"),
 'sociedad_anonima':  ( 1, "figura juridica de S.A. (estructura mayor que la media del sector)"),
 'nombre_contacto':   ( 1, "interlocutor identificado con nombre y cargo publicos"),
 'carga_llamadas':    ( 2, "senal directa de alto volumen telefonico (24h declarado, 3+ lineas o base de clientes grande)"),
 'identidad_dudosa':  (-2, "dominio o direccion no coinciden con la ficha de Google Maps"),
}
FLAGS = {
  5:['multisede','b2b','sin_email'],                 15:['nombre_contacto','email_posible','identidad_dudosa'],
 12:['b2b','sin_email'],                              4:['email_verificado'],
  0:['carga_llamadas','email_posible'],             168:['nombre_contacto','email_verificado'],
 19:['carga_llamadas','sin_email'],                  27:['email_verificado','acreditacion'],
  7:['b2b','email_posible','identidad_dudosa'],      20:['multisede','sin_email'],
 49:['email_verificado','carga_llamadas'],           53:['b2b','email_verificado'],
 25:['acreditacion','email_verificado'],            195:['b2b','email_verificado'],
 31:['multisede','email_verificado'],                29:['sin_email'],
 92:['b2b','nombre_contacto','email_verificado'],    11:['email_verificado','sociedad_anonima'],
190:['carga_llamadas','email_verificado'],          215:['acreditacion','email_posible','identidad_dudosa'],
  8:['acreditacion','email_verificado'],            222:['acreditacion','sin_email'],
191:['carga_llamadas','email_verificado'],          241:['email_posible'],
225:['sin_email'],                                  208:['carga_llamadas','sin_email'],
  3:['email_verificado'],                             1:['email_verificado'],
189:['sin_email'],                                   17:['sin_email'],
 33:['b2b','identidad_dudosa','email_verificado'],   41:['b2b','acreditacion','email_verificado'],
 69:['b2b','email_verificado'],
}

for r in R:
    fl = FLAGS[r['idx']]
    r['adj'] = sum(REGLAS[f][0] for f in fl)
    r['adj_why'] = "; ".join(REGLAS[f][1] for f in fl)
    b = B(r['idx']); r['_b'] = b
    r['_final'] = round(min(100.0, b['score'] + r['adj']), 1)

# Se investigaron 33 candidatas; se conservan las 30 de mayor puntuacion final.
todas = sorted(R, key=lambda r: -r['_final'])
rank_sorted, fuera = todas[:30], todas[30:]

def priority(r):
    # Tramos por puntuacion final, no discrecionales:
    # A (>=84) contactar primero | B (77-84) contactar despues | C (<77) backup
    if r['_final'] >= 84: return 'A'
    if r['_final'] >= 77: return 'B'
    return 'C'

HDR = ['rank','company_name','score','category','website','address','rating','review_count','email','email_status',
       'phone','whatsapp','contact_name','contact_role','contact_source','why_good_fit','potential_pain',
       'personalization_note','contact_priority']
with open('output/valencia_hvac_top30_enriched.csv','w',newline='',encoding='utf-8') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(HDR)
    for n, r in enumerate(rank_sorted, 1):
        b = r['_b']; r['_rank'] = n; r['_prio'] = priority(r)
        w.writerow([n, b['title'], r['_final'], b['category'], b['website'] or 'sin web en el CSV',
                    b['address'], r['rating'] or 'no disponible (el CSV de Google Maps no incluye rating)',
                    b['reviews'], r['email'] or 'no encontrado', r['email_status'],
                    r['phone'] or 'no encontrado', r['whatsapp'] or 'no encontrado publicamente',
                    r['contact_name'] or 'no encontrado', fix(r['contact_role']) or 'no encontrado',
                    r['source'], fix(r['fit']), fix(r['pain']), fix(r['note']), r['_prio']])

json.dump([{'rank':r['_rank'],'title':r['_b']['title'],'final':r['_final'],'base':r['_b']['score'],
            'adj':r['adj'],'adj_why':r['adj_why'],'reviews':r['_b']['reviews'],'prio':r['_prio'],
            'email':r['email'],'email_status':r['email_status'],'phone':r['phone'],'whatsapp':r['whatsapp'],
            'contact_name':r['contact_name'],'contact_role':r['contact_role'],'website':r['_b']['website'],
            'category':r['_b']['category'],'address':r['_b']['address'],'source':r['source'],
            'fit':fix(r['fit']),'pain':fix(r['pain']),'note':fix(r['note'])} for r in rank_sorted],
          open('output/top30_enriched.json','w'), ensure_ascii=False, indent=1)
json.dump([{'title':r['_b']['title'],'final':r['_final'],'reviews':r['_b']['reviews']} for r in fuera],
          open('output/casi_dentro.json','w'), ensure_ascii=False, indent=1)

print("OK -> output/valencia_hvac_top30_enriched.csv\n")
K = rank_sorted
ev = sum(1 for r in K if r['email_status']=='verified_public_email')
ep = sum(1 for r in K if r['email_status']=='possible_email')
ph = sum(1 for r in K if r['phone']); wa = sum(1 for r in K if r['whatsapp']); nm = sum(1 for r in K if r['contact_name'])
print(f"email verificado: {ev}/30 ({ev/30*100:.0f}%) | posible: {ep} ({ep/30*100:.0f}%) | total con email: {ev+ep} ({(ev+ep)/30*100:.0f}%)")
print(f"telefono: {ph}/30 ({ph/30*100:.0f}%) | whatsapp publico: {wa}/30 ({wa/30*100:.0f}%) | nombre de contacto: {nm}/30 ({nm/30*100:.0f}%)")
from collections import Counter
print("prioridades:", dict(sorted(Counter(r['_prio'] for r in K).items())))
print("\nfuera del top30 (investigadas pero descartadas por puntuacion):", [(r['_b']['title'], r['_final']) for r in fuera])
print()
for r in K:
    print(f"{r['_rank']:2d}. {r['_b']['title'][:42]:42} {r['_final']:5.1f} (base {r['_b']['score']:4.1f} {r['adj']:+d})  {r['_b']['reviews']:5d} res  {r['_prio']}  {r['email_status']}")
