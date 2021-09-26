# SQATT

![Python application](https://github.com/rschuitema/sqatt/workflows/Python%20application/badge.svg)
[![BCH compliance](https://bettercodehub.com/edge/badge/rschuitema/sqatt?branch=master)](https://bettercodehub.com/)

Repository that contains scripts that are useful when analyzing software quality.

It contains scripts to create profiles of specific quality aspects of a code base. These scripts use the output of tools
like:

* [understand](https://scitools.com/)
* [resharper](https://www.jetbrains.com/resharper/)
* [cloc](https://github.com/AlDanial/cloc)
* [lizard](https://github.com/terryyin/lizard)

to create the profiles.

The scripts can create profiles for:

* code size
* complexity
* coding rule violations
* fan-in and fan-out
* function size
* interface size

Furthermore, there is a script to generate an include graph of a C/C++ code base.
