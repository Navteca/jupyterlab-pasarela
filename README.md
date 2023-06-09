<br/>
<h2 align="center">
    <p align="center">
        <!-- <img src="img/BXplorer_Logo.png" alt="BXplorer Logo" width="230" height="180"> -->
    </p>
   Pasarela is a Jupyterlab server extension that allows a user to open a Jupyter Notebook with pre-populated code provided either in base64 format or as the URL of an external publicly available notebook file.
</h2>
<br/>

# Contents

- [Why?](#why)
- [Installation](#installation)
- [Usage](#usage)
- [Current Status](#current-status)
- [Want to contribute?](#want-to-contribute)
- [Found an issue? Have suggestions?](#issues-and-suggestions)
- [Licensing](#licensing)
- [Notes](#notes-for-your-consideration)

<br/>

### Why?

Work in progress...

<br/>

### Installation

We are working on having a package in PyPi available. At the moment you can do the following:

```bash
pip install oss-pasarela
```

or

```bash
git clone https://github.com/Navteca/oss-pasarela.git
cd oss-pasarela/
npm install
python -m build
pip install oss_pasarela-<version>-py3-none-any
```

<br/>
if the installation process runs successfully, check if the extension has been activated:

```
jupyter labextension list
jupyter serverextension list
```

<br/>
If not, you might need to run:

```
jupyter labextension enable --py oss_pasarela
jupyter serverextension enable --py oss_pasarela
```

<br/>

### Usage

To use the extension on this system, you open a new window with a specially crafted URL as follows:

**Base URL**:

https://[jupyterhub_domain]/hub/user-redirect/pasarela/open

First, replace [jupyterhub_domain] with your JupyterHub domain.

**Required Parameters (use only one):**

**code** - the base64 encoded source code that will pre-populate a cell in a new notebook on this system

-**or**-

**url** - the URL of a publicly-accessible Jupyter notebook file, the contents of which will be opened in a new notebook on system

**Optional Parameters**:

**kernel_name** - the specific Notebook kernel on this system to use to open the new Notebook. If unspecified, Jupyterlab will ask you to select a kernel to use when you first open the notebook.

### Open a Notebook with a base64 string code
The following URL will open a notebook and it will be pre-populated with the base64 decoded content provided. Jupyterlab will ask which kernel is to be used for the notebook

> https://[jupyterhub_domain]/hub/user-redirect/pasarela/open?code=cHJpbnQoIkhlbGxvIFdvcmxkIik=


The following URL will open a notebook and it will be pre-populated with the base64 decoded content provided and will use the “python3” kernel.

> https://[jupyterhub_domain]/hub/user-redirect/pasarela/open?code=cHJpbnQoIkhlbGxvIFdvcmxkIik=&kernel_name=python3


### Open a Notebook with a URL
The following URL will open a notebook and it will be pre-populated with contents of the Jupyter notebook file at the specified URL. Jupyterlab will ask which kernel is to be used for the notebook

> https://[jupyterhub_domain]/hub/user-redirect/pasarela/open?url=https://cdaweb.gsfc.nasa.gov/WebServices/REST/jupyter/CdasWsExampleXarray.ipynb

<br/>

### Current Status

We are in a very early stage in terms of all the features we want to add to the extension to be even with other extensions. Currently you can do the following:

- Open a Notebook with a base64 string code
- Open a Notebook with a URL

<br/>

### Want to contribute?

First of all, thank you for taking the time to contribute!

Do you find this extension useful, with potential to be great and you like writing code? Please, don't hesitate to contribute. There is so much to do from improving an already existing feature, implement a new one to fixing bugs, etc.

There are a couple ways you can contribute to the extension:

- [Opening issues](https://github.com/Navteca/oss-pasarela/issues): you can open an issue either to report a bug, request an enhancement, ask a question, suggest a new feature, etc.
- [Pull Requests](https://github.com/Navteca/oss-pasarela/pulls): This would be awesome. We suggest you to open an issue or comment an issue before creating the Pull Request.

We are working on a contributor document and guidelines with additional information you might to work on the extension.

<br/>

### Found an issue? Have suggestions?

Please open an [issue](https://github.com/Navteca/oss-pasarela/issues), we would like yo hear from you.

<br/>

### Licensing

[BSD 3-Clause License](LICENSE)

<br/>

### Notes for your consideration

- This project is in early stage. We are continuously working on it to make it better.
- This is one of our first extensions we put out there. We are aware we have so much to learn from the FLOSS communities and that is one of the reasons we why decided to publish it.

