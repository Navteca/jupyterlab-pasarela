import base64
import binascii
import json
import nbformat as nbf
import re
import requests
import tornado
import validators
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from subprocess import check_output

NOTEBOOK_NAME = 'Untitled.ipynb'


class CustomError(Exception):
    pass


def _get_pasarela_usage() -> str:
    help_content = ""
    try:
        response = requests.get('https://api.github.com/repos/navteca/oss-pasarela/contents/USAGE.md')
        response.raise_for_status()
        data = response.json()
        base64_content = data['content']
        bytes_content = base64.b64decode(base64_content)
        help_content = bytes_content.decode()
    except requests.exceptions.HTTPError as e:
        raise CustomError(e.response.reason)
    except requests.exceptions.RequestException as e:
        raise CustomError(e.response.reason)
    except binascii.Error:
        raise CustomError('Invalid base64 string.')
    else:
        return help_content


def _decode_base64_string(code: str) -> str:
    content = None
    try:
        message_bytes = base64.b64decode(code)
        content = message_bytes.decode()
    except binascii.Error:
        raise CustomError('Invalid base64 string.')
    except Exception as e:
        raise CustomError(e)
    else:
        return content


def _get_notebook_from_url(url: str) -> str:
    try:
        if validators.url(url):
            response = requests.get(url)
            response.raise_for_status()
        else:
            raise CustomError(f'{url} is not a valid url.')
        notebook_content = json.loads(response.text)
        if not isinstance(notebook_content, dict):
            raise nbf.ValidationError('')
        nbf.validate(notebook_content)
    except requests.exceptions.HTTPError as e:
        raise CustomError(e.response.reason)
    except requests.exceptions.RequestException as e:
        raise CustomError(e.response.reason)
    except json.JSONDecodeError as e:
        raise CustomError("Invalid JSON format.")
    except nbf.ValidationError:
        raise CustomError(f'The Url {url} does not contains a valid Notebook format')
    else:
        return notebook_content


def _create_notebook(host: str, code: str, url: str, notebook_content: dict, kernel_name: str, note_book_name: str, err: str) -> None:
    header = None
    kernelspec = check_output('jupyter kernelspec list --json', shell=True).decode("utf-8")
    nb = nbf.v4.new_notebook()

    try:
        if err:
            header = f"""# <span style="color:red">Oops, something went wrong.</span>\n````Reason: {err}````"""
            help_content = _get_pasarela_usage().replace("[jupyterhub_domain]", host)
            nb['cells'] = [nbf.v4.new_markdown_cell(help_content)]
        elif code:
            nb['cells'] = [nbf.v4.new_code_cell(notebook_content)]
        else:
            nb = nbf.from_dict(notebook_content)
            
        if kernel_name:
            if kernel_name not in kernelspec:
                header = f"""# <span style="orange:red">Warning.</span>\n````Reason: Kernel {kernel_name} is not installed````"""
            else:
                nb.metadata['kernelspec'] = {'name' : kernel_name, 'display_name': kernel_name}

        if header:
            nb['cells'].insert(0, nbf.v4.new_markdown_cell(header))
        nbf.write(nb, note_book_name)
    except Exception as e:
        raise CustomError(e)
    else:
        return None


class RouteHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        code = self.get_argument("code", None)
        kernel_name = self.get_argument("kernel_name", None)   
        url = self.get_argument("url", None)                   
        tree = self.get_argument("tree", None)
        err = None
        host = self.request.host
        notebook_content = {}
        path = '/notebooks/' if tree == '' else '/lab/tree/'
        try:
            if not (code or url):
                raise CustomError('Missing code or url argument.')
            notebook_content = _decode_base64_string(code) if code else _get_notebook_from_url(url)            
        except CustomError as e:
            err = e
        finally:
            _create_notebook(host, code, url, notebook_content, kernel_name, NOTEBOOK_NAME, err)
            full_url = self.request.full_url()
            match = re.search("(\/user\/)(.*)(\/pasarela)", full_url)

        # self.redirect('http://' + self.request.host + path + NOTEBOOK_NAME)
        self.redirect('http://' + self.request.host + '/user/' + match.group(2) + path + NOTEBOOK_NAME)


class UsageHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish(_get_pasarela_usage().replace("[jupyterhub_domain]", self.request.host))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "pasarela", "open"), RouteHandler),
        (url_path_join(base_url, "pasarela", "usage"), UsageHandler)
    ]
    web_app.add_handlers(host_pattern, handlers)