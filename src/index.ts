import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette, MainAreaWidget } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { linkIcon } from '@jupyterlab/ui-components';
import { PasarelaHelpWidget } from './widgets/PasarelaHelpWidget';
import 'bootstrap/dist/css/bootstrap.min.css';
/**
 * Initialization data for the pasarela extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'oss-pasarela:plugin',
  autoStart: true,
  requires: [ICommandPalette, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    launcher: ILauncher
  ) => {
    const { commands } = app;

    const command = 'pasarela:open';
    commands.addCommand(command, {
      caption: 'Pasarela help',
      label: 'Pasarela help',
      icon: args => (args['isPalette'] ? undefined : linkIcon),
      execute: () => {
        const content = new PasarelaHelpWidget();
        const widget = new MainAreaWidget<PasarelaHelpWidget>({ content });
        widget.title.label = 'Pasarela help';
        widget.title.icon = linkIcon;
        app.shell.add(widget, 'main');
      }
    });

    if (launcher) {
      launcher.add({
        command
      });
    }

    palette.addItem({ command, category: 'OSS Extensions' });
  }
};

export default plugin;
