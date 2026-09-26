# rodrigomadera.com

Sitio de Rodrigo Madera, locutor en Impulso FM 107.3.

## Qué hay aquí

| Archivo | Para qué sirve |
| --- | --- |
| `index.html` | El sitio completo. Un solo archivo: estilos, código y fotos incrustadas. |
| `og.jpg` | Imagen que se muestra al compartir el enlace en WhatsApp, redes y buscadores. |
| `CNAME` | Le dice a GitHub Pages que el sitio responde en rodrigomadera.com. |
| `.nojekyll` | Evita que GitHub procese los archivos antes de publicarlos. |

## Cómo cambiar los enlaces

Abre `index.html` y busca el bloque `var CONFIG`, cerca del inicio del `<script>`.
Ahí están la dirección del stream, los enlaces de cada red, el feed del pódcast y
los datos de contacto. Deja en `""` lo que no tengas: el botón no aparece.

También puedes hacerlo desde el navegador, sin tocar el código. Entra a
rodrigomadera.com/#config, llena los campos y pulsa "Generar configuración":
te entrega el bloque listo para pegar aquí.

## Publicación

GitHub Pages sirve la rama `main` desde la raíz. Cada `push` actualiza el sitio
en unos minutos.
