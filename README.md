# rodrigomadera.com

El dominio funciona como ancla: cada negocio o actividad cuelga de él en su
propia carpeta.

## Estructura

| Dirección | Carpeta | Qué es |
| --- | --- | --- |
| `/` | `index.html` | Portada. Lista las áreas y enlaza a cada una. |
| `/radio/` | `radio/` | La barra nocturna en Impulso FM: reproductor en vivo, los tres programas, biografía y contrataciones. |
| `/socials/` | `socials/` | Todos los enlaces y el contacto, para compartir en redes. Sustituye a solo.to. |
| `/admin/` | `admin/` | Contador de visitas. Lleva `noindex` y nada la enlaza. |

Archivos sueltos en la raíz: `og.jpg` (vista previa al compartir), `CNAME`
(dominio propio) y `.nojekyll`.

Cada página es un solo archivo, con estilos, código y fotos incrustadas. No
dependen unas de otras.

## Agregar un negocio nuevo

1. Crea la carpeta, por ejemplo `tienda/`, con su `index.html` dentro.
   Queda publicado en `rodrigomadera.com/tienda/`.
2. En el `index.html` de la raíz, dentro de `<div class="areas">`, copia un
   bloque `<a class="area">` y cambia el enlace, el color de acento (`--ac`),
   el rótulo, el título y la descripción. Hay un comentario con las
   instrucciones justo ahí.

## Cambiar los enlaces del sitio de radio

Abre `radio/index.html` y busca `var CONFIG`, cerca del inicio del `<script>`:
ahí están el stream, las redes, el feed del pódcast y el contacto. Deja en `""`
lo que no tengas y el botón no aparece.

También se puede desde el navegador, sin tocar código: entra a
`rodrigomadera.com/radio/#config`, llena los campos y pulsa
"Generar configuración".

## Contador de visitas

Usa GoatCounter, que es gratuito y no pone cookies. El código de la cuenta va
en cuatro lugares, y tiene que ser el mismo en todos:

- `index.html` → `var GOATCOUNTER`
- `radio/index.html` → `goatcounter:` dentro de `CONFIG`
- `socials/index.html` → `var GOATCOUNTER`
- `admin/index.html` → `var GOATCOUNTER`

En la configuración de GoatCounter hay que activar
"Allow adding visitor counts to your website" para que `/admin/` pueda leer
las cifras.

## Publicación

GitHub Pages sirve la rama `main` desde la raíz. Cada `push` actualiza el
sitio en unos minutos.

### DNS

En el proveedor del dominio, apuntando a GitHub Pages:

- Cuatro registros **A** en `@`: `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`
- Cuatro registros **AAAA** en `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`,
  `2606:50c0:8002::153`, `2606:50c0:8003::153`
- Un **CNAME** en `www` hacia `rodrigomadera.github.io`

Los AAAA no son opcionales: sin ellos el sitio no abre en redes móviles, que
en México funcionan sobre IPv6.
