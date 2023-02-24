import re
import json
import base64
import binascii
import requests
import validators
from subprocess import check_output
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

def _get_pasarela_usage():
    response = requests.get('https://api.github.com/repos/navteca/oss-pasarela/contents/USAGE.md')
    data = response.json()
    base64_content = data['content']
    bytes_content = base64.b64decode(base64_content)
    help_content = bytes_content.decode()

    return help_content
class RouteHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        code = self.get_argument("code", None)
        url = self.get_argument("url", None)
        kernel_name = self.get_argument("kernel_name", None)   

        err = None
        if code:
            try:
                base64_bytes = code.encode('ascii')
                message_bytes = base64.b64decode(base64_bytes)
                notebook_content = message_bytes.decode('ascii')
            except binascii.Error:
                err = 'Invalid base64 string.'
        elif url:
            if validators.url(url):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    err = e.response.reason
                except requests.exceptions.RequestException as e:
                    err = e.response.reason

                if not err:
                    try:
                        notebook_content = json.loads(response.text)
                    except json.JSONDecodeError as e:
                        err = "Invalid JSON format."

                    if not err and ('metadata' not in notebook_content or 'nbformat' not in notebook_content or 'cells' not in notebook_content):
                        err = f'The Url {url} does not contains a valid Notebook format'
            else:
                err = f'{url} is not a valid url.'
        else:        
            err = 'Missing code or url argument.'

        nb = nbf.v4.new_notebook()
        NOTEBOOK_NAME = 'Untitled.ipynb'

        if err:
            header = f"""# <span style="color:red">Oops, something went wrong.</span>\n````Reason: {err}````"""
            help_content = _get_pasarela_usage()
            nb['cells'] = [nbf.v4.new_markdown_cell(header), nbf.v4.new_markdown_cell(help_content)]
        else:
            header = f""" This notebook has been generated by OSS Pasarela extension. """
            if code:
                nb['cells'] = [nbf.v4.new_code_cell(notebook_content)]
            else:
                nb = nbf.from_dict(notebook_content)
            
            nb['cells'].insert(0, nbf.v4.new_markdown_cell(header))

            kernelspec = check_output('jupyter kernelspec list --json', shell=True).decode("utf-8")
            if kernel_name:
                if kernel_name not in kernelspec:
                    err = f"""# <span style="orange:red">Warning.</span>\n````Reason: Kernel {kernel_name} is not installed````"""
                else:
                    nb.metadata['kernelspec'] = {'name' : kernel_name, 'display_name': kernel_name}

            if url and 'kernelspec' in nb.metadata and 'name' in nb.metadata.kernelspec and nb.metadata.kernelspec.name not in kernelspec:
                err = f"""# <span style="orange:red">Warning.</span>\n````Reason: Kernel {nb.metadata['kernelspec']['name']} is not installed````"""
            
            if err:
                nb['cells'].insert(0, nbf.v4.new_markdown_cell(err))

        nbf.write(nb, NOTEBOOK_NAME)

        full_url = self.request.full_url()
        match = re.search("(\/user\/)(.*)(\/pasarela)", full_url)
        self.redirect('http://' + self.request.host + '/user/' + match.group(2) + '/lab/tree/' + NOTEBOOK_NAME)
class UsageHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        # self.finish('This is a test')
        self.finish(_get_pasarela_usage())

def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "pasarela", "open"), RouteHandler),
        (url_path_join(base_url, "pasarela", "usage"), UsageHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)