# Pasarela Extension
Pasarela is a Jupyterlab server extension that allows a user to open a Jupyter Notebook with pre-populated code provided either in base64 format or as the URL of an external publicly available notebook file. To use the extension on this system, you open a new window with a specially crafted URL as follows:

**Base URL**:

https://[jupyterhub_domain]/user/[username]/pasarela/open

First, replace [username] with your JupyterHub username.

**Required Parameters (use only one):**

**code** - the base64 encoded source code that will pre-populate a cell in a new notebook on this system

-**or**-

**url** - the URL of a publicly-accessible Jupyter notebook file, the contents of which will be opened in a new notebook on system

**Optional Parameters**:

**kernel_name** - the specific Notebook kernel on this system to use to open the new Notebook. If unspecified, Jupyterlab will ask you to select a kernel to use when you first open the notebook.

### Open a Notebook with a base64 string code
The following URL will open a notebook for the user *jovyan*. The notebook will be pre-populated with the base64 decoded content provided. Jupyterlab will ask which kernel is to be used for the notebook

> https://[jupyterhub_domain]/user/jovyan/pasarela/open?code=cHJpbnQoIkhlbGxvIFdvcmxkIik=


The following URL will open a notebook for the user *jovyan*. The notebook will be pre-populated with the base64 decoded content provided and will use the “python3” kernel.

> https://[jupyterhub_domain]/user/jovyan/pasarela/open?code=cHJpbnQoIkhlbGxvIFdvcmxkIik=&kernel_name=python3


### Open a Notebook with a URL
The following URL will open a notebook for the user *jovyan*. The notebook will be pre-populated with contents of the Jupyter notebook file at the specified URL. Jupyterlab will ask which kernel is to be used for the notebook

> https://[jupyterhub_domain]/user/jovyan/pasarela/open?url=https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsExampleXarray.ipynb