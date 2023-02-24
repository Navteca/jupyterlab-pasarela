import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the oss-pasarela extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'oss-pasarela:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension oss-pasarela is activated!');

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The oss_pasarela server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
