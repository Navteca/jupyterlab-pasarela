import { ReactWidget } from '@jupyterlab/apputils';

import React from 'react';
import { PasarelaHelpComponent } from '../components/PasarelaHelpComponent';
/**
 * A React Widget that wraps a PasarelaHelpComponent.
 */
export class PasarelaHelpWidget extends ReactWidget {
  /**
   * Constructs a new PasarelaHelpWidget.
   */
  constructor() {
    super();
    this.addClass('jp-ReactWidget');
  }

  render(): JSX.Element {
    return <PasarelaHelpComponent />;
  }
}
