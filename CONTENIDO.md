# Reglas de contenido (las sigue la tarea semanal)

## Semana tipo (hora de Madrid)

| Día | Formato | Pilar | Objetivo |
|---|---|---|---|
| Martes 13:30 | Carrusel 7–9 diapositivas (portada + puntos + cierre) | Educativo: errores, checklists, cómo hacer algo | Guardados + leads (CTA «Comenta WEB / ANÁLISIS») |
| Miércoles 20:30 | Imagen única (una SlidePortada sin «Desliza», sin número de página) | Interacción: situación con la que se identifica un dueño de negocio | Comentarios + envíos |
| Jueves 13:30 | Carrusel 5–7 diapositivas | Historia o proceso: cómo trabaja SunCode, qué aprende Antonio, el antes/después de suncode.es | Guardados + seguidores |

Alternar temas: web, redes sociales, Google/ficha de empresa, contenido, captación de clientes. No repetir un tema que ya esté en `posts/`. Si ya hay una carpeta en `posts/` para uno de esos días, ese día no se crea nada.

## Público y voz

Dueños de pymes y negocios tradicionales (ferreterías, talleres, reformas, panaderías, proveedores agroalimentarios…), sobre todo de Murcia. Español de España, tuteo, frases cortas, cero jerga. Una idea por diapositiva.

## Honestidad (no negociable)

- Nada de cifras, estudios, porcentajes, resultados de clientes, nombres de clientes ni equipo que no estén aquí. SunCode es una agencia de una persona (Antonio, fundador).
- Hechos propios que sí se pueden usar: la web de suncode.es tuvo un formulario que no llegaba (mailto), un teléfono que no coincidía y enlaces rotos, y se rediseñó. SunCode ofrece un análisis de marketing gratuito.
- Mejor un consejo útil y concreto que una promesa.

## Texto del post (post.json)

Gancho en la primera línea, 3–6 líneas de valor, CTA claro, 6–8 hashtags en español (incluir #murcia y #suncode). Sin emojis en exceso (máximo 2).

## Técnico

- Diapositivas: HTML con las plantillas `sc-` de `brand/bundle.css` (estructura en el sistema de diseño «SunCode Instagram»), logo siempre `<img class="sc-logo" src="LOGO">`.
- Exportar: `python3 scripts/render.py posts/<carpeta>/slides.html posts/<carpeta>` (genera 01.jpg…; necesita `brand/fonts/` con Clash Display).
- `post.json`: `text`, `dueAt` en UTC (Madrid = UTC+1 en horario de invierno, UTC+2 en verano), `images` en orden.
- Carpeta: `posts/AAAA-MM-DD-tema-corto/`.
