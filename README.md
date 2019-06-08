# Neutron Programming Language

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/484ce81d17ca468b8a93f0aa52720072)](https://app.codacy.com/app/MonliH/neutron?utm_source=github.com&utm_medium=referral&utm_content=the-neutron-foundation/neutron&utm_campaign=Badge_Grade_Dashboard)
[![Documentation Status](https://readthedocs.org/projects/neutron-lang/badge/?version=latest)](https://neutron-lang.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-GPL%203.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![Version](https://img.shields.io/badge/version-v0.0.1--alpha.1-orange.svg)](https://github.com/the-neutron-foundation/neutron/releases)
![Maintenance](https://img.shields.io/maintenance/yes/2019.svg)
[![Gitter](https://img.shields.io/gitter/room/The-Neutron_Foundation/Neutron.svg)](https://gitter.im/The-Neutron-Foundation)

Neutron is a programming language inspired by C, Python, and Java. It is faster than normal Python 3 in most tests. Binary releases [here](https://github.com/the-neutron-foundation/neutron/releases). NOTE: the precomilled binaries don't work on Windows 10 (even the `.exe` ones). If on windows, you can try to [compile](https://neutron-lang.readthedocs.io/en/latest/introduction.html#installation) yourself.

# Documentation
There is a ReadTheDocs [here](https://neutron-lang.readthedocs.io/en/latest/). You may also look at the [grammar file](./grammar.txt) (very rough). There is also a [Gitter Chat here](https://gitter.im/The-Neutron-Foundation).

# Basic Usage
To use, run the filename as the first argument. For example, on Unix-like systems, you could do:

```
./neutron.bin path/to/neutron/file.ntn
```

The filename for neutron files is `.ntn`. For example, `important_file.ntn`.

# Features
- [x] **Numpy  arrays Builtin!!**
- [x] Classes
- [x] Functions
- [x] Built-Ins (e.g. print, get, stdin, to_int)
- [x] Primitive Types (Integers, Floats, Booleans, Strings)
- [x] Python Lists and Tuples
- [x] While loops
- [ ] For Loops
