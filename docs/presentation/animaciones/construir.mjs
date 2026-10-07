// Construye las animaciones de Health Access Bridge con Archify (https://github.com/tt-a1i/archify, MIT).
//
// Uso (desde docs/presentation/animaciones, con Archify clonado en <ruta-archify>/archify):
//   node construir.mjs <ruta-a-archify/bin/archify.mjs> [nombre ...]
// Para cada fuentes/<nombre>.json agrega el idioma español (meta.locale y las traducciones del visor que trae
// Archify en examples/locales/es.json), valida con `finalize` (incluye una verificación en navegador real)
// y escribe <nombre>.html en esta carpeta. Los HTML son autosuficientes: se abren sin instalar nada.
import { execFileSync } from 'node:child_process';
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const aqui = dirname(fileURLToPath(import.meta.url));
const [bin, ...pedidos] = process.argv.slice(2);
if (!bin) {
  console.error('Uso: node construir.mjs <ruta-a-archify/bin/archify.mjs> [nombre ...]');
  process.exit(2);
}
const raizArchify = resolve(dirname(bin), '..');
const traducciones = JSON.parse(readFileSync(join(raizArchify, 'examples', 'locales', 'es.json'), 'utf8'));
delete traducciones.$schema;

const fuentes = readdirSync(join(aqui, 'fuentes')).filter((f) => f.endsWith('.json')).map((f) => f.slice(0, -5));
const nombres = pedidos.length ? pedidos : fuentes;
mkdirSync(join(aqui, '.build'), { recursive: true });

let fallos = 0;
for (const nombre of nombres) {
  const fuente = JSON.parse(readFileSync(join(aqui, 'fuentes', `${nombre}.json`), 'utf8'));
  fuente.meta.locale = 'es';
  fuente.meta.translations = traducciones;
  const candidato = join(aqui, '.build', `${nombre}.json`);
  writeFileSync(candidato, JSON.stringify(fuente, null, 2));
  try {
    const salida = execFileSync(
      'node',
      [bin, 'finalize', fuente.diagram_type, candidato, fuente.meta.output, '--quality', 'showcase', '--json'],
      { cwd: aqui, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] },
    );
    console.log(`OK  ${nombre}: ${salida.split('\n').filter(Boolean).slice(0, 3).join(' | ').slice(0, 300)}`);
  } catch (e) {
    fallos++;
    console.error(`ERROR ${nombre}:\n${(e.stdout || '').slice(0, 3000)}\n${(e.stderr || '').slice(0, 1500)}`);
  }
}
process.exit(fallos ? 1 : 0);
