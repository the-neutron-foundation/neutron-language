Introduction
============

Installation
^^^^^^^^^^^^
To use, either install the binaries, or build them yourself. If you built it yourself, you should have numpy installed. Neutron uses a python 3 compiler called `Nuitka <https://nuitka.net/pages/overview.html>`_, which is faster.
Note that running neutron with the defult python implmentation (CPython) won't work, because the import system works differently. To compile from source, get `Nuitka <https://nuitka.net/pages/overview.html>`_.
After that, go to the source folder (the master foldeer) there shoud be a ``neutron`` folder in the master folder, and run the Nuitka build commands. Here are the commands (run in order):

    pip3 install nuitka  # install nuitka
    git clone https://github.com/the-neutron-foundation/neutron  # get repo
    cd neutron
    python3 -m nuitka --follow-imports --include-plugin-directory=./neutron --show-progress --show-scons neutron # compile neutron sing python -m flag

After compilling, you should see a ``neutron.exe`` file and a ``neutron.bin`` file. These are your binaries. To use the .bin binaries on unix systems just run ``./neutron.bin``. On windows, the ``.exe`` file can just be run as ``neutron`` in the cmd.


Usage
^^^^^
