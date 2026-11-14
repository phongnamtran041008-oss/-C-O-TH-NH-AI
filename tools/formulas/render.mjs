// Renders the formulas of Tàng Thư Các: TeX -> SVG (MathJax) -> PNG (resvg).
//
//     node render.mjs jobs.json out-folder
//
// jobs.json: {"supersample": 3, "ex_in_base": 4.5, "jobs": [{"key": "...", "tex": "..."}]}
// Writes <out-folder>/<key>.png and prints one JSON object on stdout:
// {"built": [{"key", "w", "h", "px_w", "px_h"}], "errors": ["..."]}
//
// w and h are in the game's base units (its screen is 480 x 270 of them); the PNG itself
// is `supersample` times that, so it stays sharp at the usual window size.
// MathJax draws every glyph as a path (fontCache: 'none'), so no font is needed here and
// the picture looks the same on every machine.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import { liteAdaptor } from 'mathjax-full/js/adaptors/liteAdaptor.js';
import { RegisterHTMLHandler } from 'mathjax-full/js/handlers/html.js';
import { TeX } from 'mathjax-full/js/input/tex.js';
import { AllPackages } from 'mathjax-full/js/input/tex/AllPackages.js';
import { mathjax } from 'mathjax-full/js/mathjax.js';
import { SVG } from 'mathjax-full/js/output/svg.js';

const [, , jobsPath, outDir] = process.argv;
if (!jobsPath || !outDir) {
  console.error('usage: node render.mjs jobs.json out-folder');
  process.exit(2);
}
const { jobs, supersample = 3, ex_in_base: exInBase = 4.5 } = JSON.parse(readFileSync(jobsPath, 'utf8'));
mkdirSync(outDir, { recursive: true });

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {
  InputJax: new TeX({ packages: AllPackages }),
  OutputJax: new SVG({ fontCache: 'none' }),
});

const built = [];
const errors = [];
for (const { key, tex } of jobs) {
  try {
    const node = doc.convert(tex, { display: true, em: 16, ex: 8, containerWidth: 100000 });
    const svg = adaptor.outerHTML(adaptor.firstChild(node));
    if (/merror|data-mjx-error/.test(svg)) {
      const why = (svg.match(/data-mjx-error="([^"]*)"/) || [, 'TeX error'])[1];
      errors.push(`${key}: ${tex} -> ${why}`);
      continue;
    }
    const size = svg.match(/width="([\d.]+)ex"\s+height="([\d.]+)ex"/);
    if (!size) {
      errors.push(`${key}: ${tex} -> MathJax gave no size`);
      continue;
    }
    const w = +(Number(size[1]) * exInBase).toFixed(2);
    const h = +(Number(size[2]) * exInBase).toFixed(2);
    const png = new Resvg(svg, {
      fitTo: { mode: 'width', value: Math.max(1, Math.round(w * supersample)) },
      font: { loadSystemFonts: false },
    }).render();
    writeFileSync(join(outDir, `${key}.png`), png.asPng());
    built.push({ key, w, h, px_w: png.width, px_h: png.height });
  } catch (e) {
    errors.push(`${key}: ${tex} -> ${e.message}`);
  }
}
process.stdout.write(JSON.stringify({ built, errors }));
