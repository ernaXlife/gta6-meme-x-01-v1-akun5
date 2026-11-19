// gta6-meme-x-01 entry (Node 22, stdlib only).
// The entry is the X post itself: this program only hands its address to the
// gate by copying POST.json from the repo root to /output/POST.json.
// The house reads the post from X and the judge sees its first picture + text.
// Local test: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));

// Guard: only POST.json is copied; the post on X is the entry.
