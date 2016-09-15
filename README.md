# xpecgen
[![release v1.0.0](http://img.shields.io/badge/release-v1.0.0-blue.svg)](https://github.com/dih5/xpecgen/releases/latest)
[![license GNU GPLv3](https://img.shields.io/badge/license-GNU%20GPLv3-blue.svg)](https://raw.githubusercontent.com/Dih5/xpecgen/master/LICENSE.txt)
[![Semantic Versioning](https://img.shields.io/badge/SemVer-2.0.0-brightgreen.svg)](http://semver.org/spec/v2.0.0.html)
[![PyPI](https://img.shields.io/pypi/v/xpecgen.svg)](https://pypi.python.org/pypi/xpecgen)
[![status](http://joss.theoj.org/papers/970f9606afd29308e2dcc77216429ee7/status.svg)](http://joss.theoj.org/papers/970f9606afd29308e2dcc77216429ee7)

A python package with a GUI to calculate **x**-ray s**pec**tra **gen**erated in tungsten anodes.

* [Features](#features)
* [Usage example](#usage-example)
* [Installation](#installation)
* [Requisites](#requisites)
	* [Install a scientific python distribution](#install-a-scientific-python-distribution)
	* [Install python and the packages](#install-python-and-the-packages)
* [Download and run](#download-and-run)
* [Documentation](#documentation)
* [License](#license)
* [Versioning](#versioning)
* [Requests](#requests)
* [Model details](#model-details)
* [Citation](#citation)
* [References](#references)

## Features
* X-ray spectra calculation using the models from [\[1\]](#Ref1).
* HVL calculation.
* Python library and Graphical User Interface.
* Export to xlsx files (Excel Spreadsheet).

## Usage example
### GUI
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/DemoPar.png)
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/DemoPlot.png)
### Console
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/DemoConsole.png)

## Installation
If you have [pip](https://pip.pypa.io/en/stable/installing/) you can install xpecgen as a package by running
```
pip install xpecgen
```
and then you can launch the GUI by just executing
```
xpecgen
```
or check the [demo.py](demo/demo.py) explaining its use as a library. You will need tk to make use of the GUI. See the [requisites](#requisites) if you need help for this.

If you do not have python3 installed yet, also check the [requisites](#requisites).

## Requisites
You need python3 with the following packages to run this program:
```
matplotlib, numpy, scipy, XlsxWriter, tk
```
The last one is only needed if you want to make use of the GUI.

You can [install a scientific python distribution](#install-a-scientific-python-distribution) providing them or you can install [only what you need](#install-python-and-the-packages). The first is recommended for Windows users, the latter for Linux users.


###Install a scientific python distribution:
For example you can try [Anaconda](https://www.continuum.io/downloads). Make sure you choose the python 3.X installer.
Since this will install pip, you might want to use the [pip installer](#installation).

###Install python and the packages:
- Download [python 3.X](https://www.python.org/) for your OS. See specific instructions to install from repositories below.
- Use the [pip installer](#Installation) (recommended) or manually install the additional packages. See specific instructions below.

#### Windows
As a general advice, forget it. Scipy depends on lots of C, Cython and Fortran code that needs to be compiled before use.
I suggest you just go for [a scientific python distribution](#install-a-scientific-python-distribution).

There are also some alternatives which are actually Linux in disguise:
- In Windows 10 you can make use of the bash shell to install from the Ubuntu repositories. Check out [this guide](http://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) and the Ubuntu specific instructions. (I have not tested this yet).
- Install Ubuntu (or any other Linux) in a virtual machine using [VirtualBox](https://www.virtualbox.org/).
- [Switch to Linux](https://www.google.com/search?q=why+switch+to+linux).

#### Ubuntu
```bash
sudo apt-get update
sudo apt-get install python3 python3-matplotlib python3-numpy python3-scipy python3-xlsxwriter python3-tk
```
#### Arch Linux
```bash
sudo pacman -S python python-matplotlib python-numpy python-scipy python-xlsxwriter tk
```
#### Fedora
(Not tested)
```bash
sudo yum install -y python-pip
sudo yum install -y lapack lapack-devel blas blas-devel 
sudo yum install -y blas-static lapack-static
sudo pip install numpy
sudo pip install scipy
sudo pip install openpyxl
```
On Fedora 23 onwards, use dnf instead of yum

##Download and run
You can also download and execute the program without installing it, as long as you meet the [requisites](#requisites).
Download and extract the [zip file](https://github.com/Dih5/xpecgen/archive/master.zip) of the repository.
To start the GUI, open xpecgen/xpecgenGUI.py with your python3 interpreter. In Windows you can use xpecgenGUI.bat in the same folder to launch it.


##Documentation
You can use the python help system to check the library documentation:
```python3
from xpecgen import xpecgen as xg
help(xg)
```


##License
This package is released under
[the GNU GPLv3 license](https://raw.githubusercontent.com/Dih5/xpecgen/master/LICENSE.txt).


## Versioning
Releases of this package will be numbered using
[Semantic Versioning guidelines](http://semver.org/).

## Requests
If you find any bugs or have a feature request you may create an [issue on GitHub](https://github.com/dih5/xpecgen/issues).
You may also considering forking and sending a pull request if you are an experienced developer.

## Model details
To have a general overview of the model see [\[1\]](#Ref1).
The bremsstrahlung calculation is done using full interpolations for the electron fluence, so none of the simplifications in section IV.C were used in this implementation.
Both characteristic peaks models in section II.D were implemented. The polynomial one is used by default.
Half-value layers are calculated using the exponential model of attenuation (aka narrow beam geometry). In the GUI they are calculated in the sense of dose, but the library allows for generalizing this to any desired reponse function.

## Citation
If you use this application to make use of the models in [\[1\]](#Ref1), you should cite it.

##References
<a name="Ref1">\[1\]</a> Hernández, G., Fernández F. 2016. "A model of tungsten x-ray anode spectra." Medical Physics, *43* 4655. [doi:10.1118/1.4955120](http://dx.doi.org/10.1118/1.4955120)
