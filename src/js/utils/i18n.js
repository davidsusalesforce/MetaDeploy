// @flow

import i18n_backend from 'i18next-xhr-backend';
import i18n_detector from 'i18next-browser-languagedetector';
import { reactI18nextModule } from 'react-i18next';
import { use } from 'i18next';

export default use(i18n_detector)
  .use(i18n_backend)
  .use(reactI18nextModule)
  .init({
    lng: 'en',
    fallbackLng: 'en',
    keySeparator: false,
    nsSeparator: false,
    interpolation: {
      escapeValue: false,
    },
    saveMissing: true,
    backend: {
      loadPath: '/static/{{lng}}/{{ns}}.json',
    },
  });
