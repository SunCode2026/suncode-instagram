# suncode-instagram

Carruseles de Instagram de SunCode Digital Services.

Cada carpeta `posts/<fecha>-<tema>/` tiene las diapositivas (`01.png`, `02.png`…, 1080×1350) y un `post.json` con el texto y la fecha de publicación. Al subir una carpeta nueva, la Action **Enviar a Buffer** la manda a Buffer como **borrador** programado para esa fecha; se aprueba desde la app de Buffer.

Requiere el secreto `BUFFER_API_KEY` (Settings → Secrets and variables → Actions).
