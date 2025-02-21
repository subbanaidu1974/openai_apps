
// src/main.ts

import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app/app.module';
import { environment } from './environments/environment';

if (environment.production) {
  enableProdMode();
}

const bootstrap = async () => {
  try {
    await platformBrowserDynamic().bootstrapModule(AppModule);
    console.log('Application bootstrapped successfully!');
  } catch (err) {
    console.error('Error bootstrapping the application:', err);
  }
};

bootstrap();

