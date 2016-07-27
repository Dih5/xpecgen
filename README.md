# xpecgen
[![release v0.1.0](http://img.shields.io/badge/release-v0.1.0-orange.svg)](https://github.com/dih5/xpecgen/releases/latest)
[![license GNU GPLv3](https://img.shields.io/badge/license-GNU%20GPLv3-blue.svg)](https://raw.githubusercontent.com/Dih5/xpecgen/master/LICENSE.txt)
[![Semantic Versioning](https://img.shields.io/badge/SemVer-2.0.0-brightgreen.svg)](http://semver.org/spec/v2.0.0.html)

A python package with a GUI to calculate **x**-ray s**pec**tra **gen**erated in tungsten anodes.

* [Features](#features)
* [Usage example](#usage-example)
* [Requisites](#requisites)
	* [The easy way](#the-easy-way)
	* [The DIY way (might be easier)](#the-diy-way-might-be-easier)
* [Download and run](#download-and-run)
* [License](#license)
* [Versioning](#versioning)
* [Model details](#model-details)
* [Citation](#citation)
* [References](#references)

## Features
* X-ray spectra calculation using the models from [\[1\]](#Ref1).
* HVL calculation
* Python library and Graphical User Interface
* Export to xlsx files (Excel Spreadsheet)

## Usage example
### GUI
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/b.png)
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/c.png)
### Console
![alt tag](https://raw.github.com/dih5/xpecgen/master/img/a.png)

## Quick start
1. Make sure you meet the [requisites](#requisites).
2. [Download and run](#download-and-run).

## Requisites
You need python3 with the following packages to run this program:
```
matplotlib, numpy, scipy, XlsxWriter, tk
```
The last one is only needed if you want to make use of the GUI. You can install them [the easy way](#the-easy-way) or you can install [only what you need](#the-diy-way-might-be-easier). The first is recommended for Windows users, the latter for Linux users.

###The easy way
Install a scientific python distribution providing all these packages.
For example you can try [Anaconda](https://www.continuum.io/downloads). Make sure you choose the python 3.X installer.

###The DIY way (might be easier):
- Download [python 3.X](https://www.python.org/) for your OS.
- Install the additional packages. See specific instructions below.

#### Windows
As a general advice, forget it. Scipy depends on lots of C, Cython and Fortran code that needs to be compiled before use.
I suggest you just go for [the easy way](#the-easy-way).
Still, if you have tried and somehow managed to complete this odyssey I would be glad to hear your tale.

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
Download and extract the [zip file](https://github.com/Dih5/xpecgen/archive/master.zip) of the repository.
To start the GUI, open xpecgenGUI.py with your python3 interpreter. In Windows you can use xpecgenGUI.bat to launch it.
To start the interactive command line mode, start the python interpreter in the directory where the files were extracted and follow the usage example.
You can also write a custom script following the example in [demo.py](demo.py).

##License
This package is released under
[the GNU GPLv3 license](https://raw.githubusercontent.com/Dih5/xpecgen/master/LICENSE.txt).


## Versioning
Releases of this package will be numbered using
[Semantic Versioning guidelines](http://semver.org/).

## Model details
To have a general overview of the model see [\[1\]](#Ref1).
The bremsstrahlung calculation is done using full interpolations for the electron fluence, so none of the simplifications in section IV.C were used in this implementation.
Both characteristic peaks models in section II.D were implemented. The polynomial one is used by default.
Half-value layers are calculated using the exponential model of attenuation (aka narrow beam geometry). In the GUI they are calculated in the sense of dose, but the library allows for generalizing this to any desired reponse function.

## Citation
If you use this application to make use of the models in [\[1\]](#Ref1), you should cite it.

##References
<a name="Ref1">\[1\]</a> Hernández, G., Fernández F. 2016. "A model of tungsten x-ray anode spectra." Medical Physics, *43* 4655. [doi:10.1118/1.4955120](http://dx.doi.org/10.1118/1.4955120)
