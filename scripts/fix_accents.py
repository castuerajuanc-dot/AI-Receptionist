# -*- coding: utf-8 -*-
"""Restaura las tildes en los campos de texto libre del entregable.
Orden: (1) palabras inequívocas, (2) frases con formas ambiguas (esta/está, perdida/pérdida...).
Las palabras ambiguas NO se tocan a ciegas: solo dentro de las frases del bloque FRASES."""
import re

SUB = [
 ("camaras","cámaras"),("frigorificas","frigoríficas"),("frigorifica","frigorífica"),("hosteleria","hostelería"),
 ("averia","avería"),("averias","averías"),("telefono","teléfono"),("telefonos","teléfonos"),
 ("telefonica","telefónica"),("telefonico","telefónico"),("atencion","atención"),("instalacion","instalación"),
 ("reparacion","reparación"),("climatizacion","climatización"),("alimentacion","alimentación"),
 ("tecnico","técnico"),("tecnica","técnica"),("tecnicos","técnicos"),("tecnicas","técnicas"),
 ("electrodomesticos","electrodomésticos"),("refrigeracion","refrigeración"),("ventilacion","ventilación"),
 ("calefaccion","calefacción"),("fontaneria","fontanería"),("energias","energías"),("ingenieria","ingeniería"),
 ("resenas","reseñas"),("senal","señal"),("senales","señales"),("anos","años"),("numero","número"),
 ("numeros","números"),("unico","único"),("unica","única"),("captacion","captación"),("calificacion","calificación"),
 ("cualificacion","cualificación"),("gestion","gestión"),("delegacion","delegación"),("delegaciones","delegaciones"),
 ("direccion","dirección"),("seccion","sección"),("conversacion","conversación"),("distribucion","distribución"),
 ("importacion","importación"),("exportacion","exportación"),("asociacion","asociación"),
 ("evacuacion","evacuación"),("presurizacion","presurización"),("sotanos","sótanos"),
 ("informacion","información"),("confirmacion","confirmación"),("tramite","trámite"),("tramites","trámites"),
 ("revision","revisión"),("sabados","sábados"),("juridica","jurídica"),("categoria","categoría"),
 ("administracion","administración"),("facil","fácil"),("dificil","difícil"),("practicamente","prácticamente"),
 ("segun","según"),("ademas","además"),("tambien","también"),("aqui","aquí"),("asi","así"),("ahi","ahí"),
 ("despues","después"),("mediodia","mediodía"),("dia","día"),("dias","días"),("linea","línea"),("lineas","líneas"),
 ("movil","móvil"),("moviles","móviles"),("ningun","ningún"),("tipico","típico"),("tipica","típica"),
 ("basica","básica"),("basicas","básicas"),("rapida","rápida"),("automatico","automático"),
 ("automatica","automática"),("automaticamente","automáticamente"),("minimo","mínimo"),("maximo","máximo"),
 ("ultimo","último"),("garantia","garantía"),("energetica","energética"),("termica","térmica"),
 ("termicas","térmicas"),("electrica","eléctrica"),("electricas","eléctricas"),("estructuracion","estructuración"),
 ("cubris","cubrís"),("prometeis","prometéis"),("teneis","tenéis"),("vais","vais"),
 # "publico/pública" como ADJETIVO es siempre con tilde en este texto; el único uso verbal
 # se reescribió en el origen para evitar la ambigüedad.
 ("publico","público"),("publicos","públicos"),("publicas","públicas"),("publica","pública"),
 ("especializacion","especialización"),("generacion","generación"),("identificacion","identificación"),
 ("obligacion","obligación"),("operacion","operación"),("recuperacion","recuperación"),
 ("sustitucion","sustitución"),("genero","género"),("telefonicas","telefónicas"),
 ("manana","mañana"),("mananas","mañanas"),("patron","patrón"),("multiples","múltiples"),
 ("cerrais","cerráis"),("companias","compañías"),("pequena","pequeña"),("pequenas","pequeñas"),
 # Verificado uno a uno sobre el texto real: todos los usos de esta/estan son verbales,
 # todos los de mas son el adverbio, y el unico cual/quien es interrogativo.
 ("esta","está"),("estan","están"),("mas","más"),("cual","cuál"),("quien","quién"),
]

# Se aplican DESPUÉS de SUB, por lo que se escriben ya con las tildes que SUB introdujo.
FRASES = [
 ("teléfonico está","telefónico está"),
 ("el canal telefónico esta saturado","el canal telefónico está saturado"),
 ("restaurantes estan abiertos","restaurantes están abiertos"),
 ("responsable esta instalando","responsable está instalando"),
 ("NO estan verificados","NO están verificados"),("no estan verificados","no están verificados"),
 ("no esta verificado","no está verificado"),("esta acreditada","está acreditada"),
 ("perdida de","pérdida de"),
 ("El mayor volumen","El mayor volumen"),
 ("mas alto","más alto"),("mas alta","más alta"),("mas altas","más altas"),("mas de","más de"),
 ("mas que","más que"),("mas fácil","más fácil"),("mas claro","más claro"),("mas corta","más corta"),
 ("mas grande","más grande"),("mas potente","más potente"),("mas directo","más directo"),
 ("mas evidente","más evidente"),("mas antigua","más antigua"),("mucho mas","mucho más"),
 ("mas de la mitad","más de la mitad"),("y mas","y más"),("mas: ","más: "),
 ("como cubrís","cómo cubrís"),("'como ","'cómo "),
 ("cuantificar","cuantificar"),
]
NO_TOCAR = re.compile(r'(https?://\S+|[\w.+-]+@[\w.-]+)')

def fix(text):
    if not text: return text
    guard = []
    def _g(m):
        guard.append(m.group(0)); return f"\x00{len(guard)-1}\x00"
    out = NO_TOCAR.sub(_g, text)
    for a,b in SUB:
        if a == b: continue
        out = re.sub(rf'\b{a}\b', b, out)
        out = re.sub(rf'\b{a.capitalize()}\b', b.capitalize(), out)
        out = re.sub(rf'\b{a.upper()}\b', b.upper(), out)
    for a,b in FRASES:
        out = out.replace(a,b)
    return re.sub(r'\x00(\d+)\x00', lambda m: guard[int(m.group(1))], out)
