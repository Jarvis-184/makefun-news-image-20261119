import fs from 'node:fs';
import path from 'node:path';

try {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  const srcPath = path.join(import.meta.dirname, 'entry.png');
  const destPath = path.join(outputDir, 'entry.png');

  if (!fs.existsSync(srcPath)) {
    console.error(`Error: Source file not found at ${srcPath}`);
    process.exit(1);
  }

  fs.mkdirSync(outputDir, { recursive: true });
  fs.copyFileSync(srcPath, destPath);
} catch (err) {
  console.error('Error copying entry.png:', err);
  process.exit(1);
}
