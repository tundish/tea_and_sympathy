Tea and Sympathy
::::::::::::::::

This is a technical demonstration of `Balladeer`_.

Balladeer helps you build parser-based Interactive Fiction for the Web.
Balladeer is a Python library.

Installation
++++++++++++

* Windows_
* Linux_

Windows
=======

`Tea and Sympathy` is a command line program.
You use it from the Windows command interpreter.

To launch a new command window:

#. Tap the Windows key so that the Start Menu pops up.
#. Type the word `cmd`.
#. When you see the *Command Prompt* app highlighted, tap the Enter key.

You should see a prompt like this (your user name will differ)::

    Microsoft Windows [Version 10.0.18362.1139]
    (c) 2019 Microsoft Corporation. All rights reserved.

    C:\Users\author>

Prerequisites
-------------

Download and install Python from https://www.python.org/ . You need Python version 3.8 or higher.
Make sure to check the option to add `python` to your environment path.
This makes command line operation more easy.

After you've installed Python, open a command window and type `python`.
You should see something like this::

    C:\Users\author>python
    Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Type `quit()` and press Return.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python -m venv C:\Users\author\balladeer-app

#. Update the package manager within it::

    C:\Users\author\balladeer-app\Scripts\pip install -U pip wheel

#. Install dependencies::

    C:\Users\author\balladeer-app\Scripts\pip install aiohttp

#. Install (or update) Balladeer::

    C:\Users\author\balladeer-app\Scripts\pip install -U balladeer

Download
--------

#. Download the `repository as a zip file <https://github.com/tundish/tea_and_sympathy/archive/master.zip>`_.
   Unzip it to a local directory.

#. `cd` to `tea_and_sympathy`.

Run
---

You can run the demo in two modes.

#. Launch a local web server to play in a browser (`http://localhost:8080`)::

    C:\Users\author\balladeer-app\Scripts\python -m tas.server

#. Or text-only in the terminal::

    C:\Users\author\balladeer-app\Scripts\python -m tas.story

Linux
=====

The Linux command line is generally more easy to work with than the Windows command prompt.
If you're finding the Windows command prompt tricky, you can install `Git Bash`_ which behaves in a
Linux-like way.

I encourage you to move to a Linux operating system when you are able. 
You can try one out at little cost on a `Raspberry Pi`_ or similar device.

Here are the install instructions for Linux. You need Python version 3.8 or higher.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python3 -m venv ~/balladeer-app

#. Update the package manager within it::

    ~/balladeer-app/bin/pip install -U pip wheel

#. Install dependencies::

    ~/balladeer-app/bin/pip install aiohttp

#. Install (or update) Balladeer::

    ~/balladeer-app/bin/pip install -U balladeer

Download
--------

#. Download the `repository as a zip file <https://github.com/tundish/tea_and_sympathy/archive/master.zip>`_.
   Unzip it to a local directory.

#. `cd` to `tea_and_sympathy`.

Run
---

You can run the demo in two modes.

#. Launch a local web server to play the web app (`http://localhost:8080`)::

    ~/balladeer-app/bin/python -m tas.server

#. Or text-only in the terminal::

    ~/balladeer-app/bin/python -m tas.story


The freedom to copy
+++++++++++++++++++

You are free to use this project as a teaching example, or as the basis of your own work.
Please read the licence and make sure you `understand the Affero GPL`_.

.. _Balladeer: https://github.com/tundish/balladeer
.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _web rings: https://www.mic.com/p/how-geocities-webrings-made-the-90s-internet-a-cozier-place-19638198
.. _web feeds: https://en.wikipedia.org/wiki/Web_feed
.. _Git Bash: https://gitforwindows.org/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Raspberry Pi: https://www.raspberrypi.org/
.. _understand the Affero GPL: https://www.gnu.org/licenses/why-affero-gpl.html

