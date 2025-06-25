/**
 * Copyright (c) 2024, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 **/
import js from '@eslint/js';
import header from '@tony.ganchev/eslint-plugin-header';
import tsParser from '@typescript-eslint/parser';
import jest from 'eslint-plugin-jest';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import reactPlugin from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default [
  {
    ignores: ['**/out', '**/dist', '**/coverage', '**/*.d.ts', 'scripts/setup-jest.ts', 'esbuild.js', '.vscode-test/**']
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  eslintPluginPrettierRecommended,
  {
    files: ['**/*.ts'],
    plugins: {
      header,
      jest
    },

    languageOptions: {
      parser: tsParser,
      ecmaVersion: 6,
      sourceType: 'module'
    },

    rules: {
      '@typescript-eslint/naming-convention': [
        'warn',
        {
          selector: 'class',
          format: ['PascalCase']
        }
      ],

      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          ignoreRestSiblings: true,
          caughtErrors: 'none'
        }
      ],

      'header/header': [
        2,
        'block',
        [
          '*',
          {
            pattern: ' \\* Copyright \\(c\\) \\d{4}, salesforce\\.com, inc\\.',
            template: ' * Copyright (c) 2025, salesforce.com, inc.'
          },
          ' * All rights reserved.',
          ' * Licensed under the BSD 3-Clause license.',
          ' * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause',
          ' *'
        ]
      ],

      curly: 'warn',
      eqeqeq: 'warn',
      'no-throw-literal': 'warn',
      'require-await': 'error'
    }
  },
  {
    // Config specific to test directory
    files: ['test/**/*.ts'],
    plugins: {
      jest
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-expressions': 'off',

      '@typescript-eslint/naming-convention': [
        'warn',
        {
          selector: 'class',
          format: ['PascalCase']
        }
      ],
      'jest/padding-around-after-all-blocks': 'error',
      'jest/padding-around-after-each-blocks': 'error',
      'jest/padding-around-before-all-blocks': 'error',
      'jest/padding-around-before-each-blocks': 'error',
      'jest/padding-around-describe-blocks': 'error',
      'jest/padding-around-test-blocks': 'error'
    }
  },
  {
    // Config for react app
    files: ['chat/**/*.{js,jsx,mjs,cjs,ts,tsx}', 'agentWebview/**/*.{js,jsx,mjs,cjs,ts,tsx}'],
    ...reactPlugin.configs.flat.recommended,
    ...reactPlugin.configs.flat['jsx-runtime'],
    plugins: { react: reactPlugin, header, 'react-hooks': reactHooks },
    languageOptions: {
      ...reactPlugin.configs.flat.recommended.languageOptions,
      globals: {
        ...globals.serviceworker,
        ...globals.browser
      }
    },
    settings: {
      react: {
        version: 'detect'
      }
    },
    rules: {
      'react/react-in-jsx-scope': 'off',
      'no-extra-boolean-cast': 'off',
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          ignoreRestSiblings: true,
          caughtErrors: 'none',
          argsIgnorePattern: '^_'
        }
      ],
      'header/header': [
        2,
        'block',
        [
          '*',
          {
            pattern: ' \\* Copyright \\(c\\) \\d{4}, salesforce\\.com, inc\\.',
            template: ' * Copyright (c) 2025, salesforce.com, inc.'
          },
          ' * All rights reserved.',
          ' * Licensed under the BSD 3-Clause license.',
          ' * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause',
          ' *'
        ]
      ],
      ...reactHooks.configs.recommended.rules
    }
  },
  {
    // React test config
    files: ['chat/test/**/*.tsx', 'agentWebview/test/**/*.tsx'],
    plugins: { jest },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      'jest/padding-around-after-all-blocks': 'error',
      'jest/padding-around-after-each-blocks': 'error',
      'jest/padding-around-before-all-blocks': 'error',
      'jest/padding-around-before-each-blocks': 'error',
      'jest/padding-around-describe-blocks': 'error',
      'jest/padding-around-test-blocks': 'error'
    }
  }
];
