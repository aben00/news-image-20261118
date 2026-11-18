// news-image-20261118 entry (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// /output/entry.png. The image is an infographic summing up Wednesday
// 18 November 2026 in six illustrated stories, drawn by draw.py in this
// repository. The copy is deterministic: every run writes the same bytes.
//
// Run outside the grader's container with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

// The output name stays entry.png either way, per the competition rules
// (a PNG or a JPEG is told apart by its first bytes, not its extension).
// copyFileSync moves the bytes unchanged, so the two graded runs agree.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
