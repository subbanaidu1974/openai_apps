
// src/test.ts

import 'zone.js';  // Included with Angular CLI.
import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

// Enable production mode if the environment is set to production
if (environment.production) {
  enableProdMode();
}

// Bootstrap the Angular application
platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .catch(err => console.error(err));
