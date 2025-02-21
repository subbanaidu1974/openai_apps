// src/polyfills.ts

// Import zone.js for Angular's change detection
import 'zone.js';  // Included with Angular CLI.

// Polyfill for older browsers
import 'core-js/stable';
import 'regenerator-runtime/runtime';

// Importing specific polyfills for various features
import 'core-js/es/reflect'; // Reflect API
import 'core-js/es/symbol';  // Symbol API
import 'core-js/es/promise';  // Promise API
import 'core-js/es/array';    // Array methods
import 'core-js/es/object';    // Object methods

// For IE11 support
import 'classlist.js';  // Run `npm install --save classlist.js`.
import 'web-animations-js';  // Run `npm install --save web-animations-js`.

// Zone.js is required by Angular itself.
(window as any).__Zone_disable_ErrorStack = true; // Disable error stack for zone.js
(window as any).__Zone_enable_cross_context_check = true; // Enable cross-context check for zone.js
