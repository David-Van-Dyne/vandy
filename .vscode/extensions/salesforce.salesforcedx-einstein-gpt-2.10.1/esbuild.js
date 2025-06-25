/**
 * Copyright (c) 2023, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 **/
const { build } = require('esbuild');

const baseConfig = {
  bundle: true,
  minify: process.env.NODE_ENV === 'production',
  sourcemap: process.env.NODE_ENV !== 'production'
};

const webviewConfig = {
  ...baseConfig,
  target: 'es2020',
  format: 'esm',
  entryPoints: ['./views/sidebar/sidebarView.ts'],
  outfile: './out/views/sidebar/sidebarView.js'
};

(async () => {
  const args = process.argv.slice(2);
  try {
    // Build extension and webview code
    await build(webviewConfig);
    console.log('build complete');
  } catch (err) {
    process.stderr.write(err.stderr);
    process.exit(1);
  }
})();
