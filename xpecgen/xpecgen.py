#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""xpecgen.py: A module to calculate x-ray spectra generated in tungsten anodes"""

from __future__ import print_function

#----------------------------------------------------------------------#
#                               ,
#                              ▓█      ██
#                             ▄█▌      ╙█▌
#                             ▀█▌      "█▌
#                             ▐█H ╓▄▄▄  █▌
#                             ▓█▄╣█████╥██
#                     ▄▄┐    ▄ ▐█▌ ██M╫█▌ ╓     ▄▄µ
#                 ▄▄  ▐██   ▐▄ ▓█  ██Γ █▀⌐.▄   ║█▌  ╓▄
#                 ▀█▓▓▄██    ▀▄ ▓▌ ██┐▐█ ▄▀    ▓█▌▄▓██
#                   `▀▀███▄ A`╙▄╝└▓███"▀▄▀`ⁿµ,███▀▀"   .
#  -██████▄▄,,   ╓     ╙████▄▄▄█▄ⁿ⌐   ═▄█▄▄,████▀     ▄   ,,╓▄▄█████W
#        `╙▀▀██, ╓ ╙╗.'""▀█▌▀▀█████████████▀▀██T"*.▄▀,, ,▄█▀▀▀Γ'
#         ╓▓██╙██▀▄▄ "▓▄ ██W  ██████▀█████,  ██▌▄▄M ▄▄█▀█▀▄█▓▄
#¢█▄,     ██████▄,[▐█Γ ⌠███████▀███▌║███████████░ "█▌[,▄█▓████     ,▄▓▌
# ╙▀███▄▄,╙█▀▄║▀▀▀███▌ `███████████▓████████████D ▐███▀▀▀▀▄▀█▀,▄▄▓██▀▀
#    Γ T▀▀█▀▀▀█▄╗▌▄▌▀, ▓███▀▀██████████████▀▀████ ┌▀▀▄▄▌Φ█▀▀▀██▀Γ T
#           .▄ "%,,▓▄▄▓█████████████████▓█████████▄▄█╓,/^,,=
#            `"Γ "  └██▓███████████████████████████Γ  ^ ╙▀
#          ,,    ,▄▓▄█▌  ▐██▓████▓█████████▓██▌` ▀█▓▄▒,    ,,
#         █████▓███████▓▄██████▀██████▓█▀██████▄▄███████▓█████⌐
#            ╓▓█▀╙" ▌ "▓██████▄▓████▀████▄███████▀ ║⌐╙▀▀██▄
#          Φ███     ¡╓K█`╘⌐▀████████████████▀╙╡ ▓▀╗╡     ▀██▌
#                ,ΦΓ╟ ▄▓╖▓▄µ ╠▀███▌  ▐████║ ,▄▓▄▀▄,╣7▀,
#               `" ╓█M▀ ▓███╓,▄█▀██▓▄██▀╢▌,,▓███ ╙▀▓▌ ▀
#               ▄▄▄██"▄▓█" ▄▌ ▓  ╓▓███=  ▀ ╙█=`▀█▓ ▀█▓▄▄
#              ▄█▌└█████▀▄▄▌e`▌   ║███   ╘M%▄█▄▐▀██▓█▄ █▄
#            ▄▓█╨  ▀████▐█▀ ▄▄Γ   ▄██▌    ▀▄ ╙██▓████"  ██▄
#           ╓██      "└╓▓█w      ▄█▌╙██▄   .  ██▄'l      ▀█▄
#           ██       ,▄█▀       ╙██  ▐██       ╙██▄       ▓█
#                  ,▄██H                         ██▄▄
#                 ▓█▀                              ▀██⌐
#
#----------------------------------------------------------------------#
__author__ = 'Dih5'
__version__ = "1.0.1"
#----------------------------------------------------------------------#

import math
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
from scipy import interpolate, integrate, optimize

from bisect import bisect_left

import os
from glob import glob

import warnings

import csv
import xlsxwriter


data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")



#--------------------General purpose functions-------------------------#

def logInterp1d(xx, yy, kind='linear'):
    """Log-Log interpolation"""
    logx = np.log10(xx)
    logy = np.log10(yy)
    # No big difference in efficience was found when replacing interp1d by
    # UnivariateSpline
    linInterp = interpolate.interp1d(logx, logy, kind=kind)
    logInterp = lambda zz: np.power(10.0, linInterp(np.log10(zz)))
    return logInterp


# This custom implemenation of dblquad is based in the one in numpy
#(Cf. https://github.com/scipy/scipy/blob/v0.16.1/scipy/integrate/quadpack.py#L449 )
# It was modified to work only in rectangular regions (no g(x) nor h(x))
# to set the inner integral epsrel
# and to increase the limit of points taken
def _infunc(x, func, c, d, more_args, epsrel):
    myargs = (x,) + more_args
    return integrate.quad(func, c, d, args=myargs, epsrel=epsrel, limit=2000)[0]


def custom_dblquad(func, a, b, c, d, args=(), epsabs=1.49e-8, epsrel=1.49e-8, maxp1=50, limit=50):
    return integrate.quad(_infunc, a, b, (func, c, d, args, epsrel),
                          epsabs=epsabs, epsrel=epsrel, maxp1=maxp1, limit=2000)


def triangle(x, loc=0, size=0.5, area=1):
    """
    The triangle window function centered in loc, of given size and area, evaluated in x
    Mathematica code: If[Abs[(x - loc)/size] > 1, 0, 1 - Abs[(x - loc)/size]]/Abs[size*area]
    """
    # t=abs((x-loc)/size)
    # return 0 if t>1 else (1-t)*abs(area/size)
    # Temporal variable code is disabled to avoid problems with plot_function.
    # See note there.
    return 0 if abs((x - loc) / size) > 1 else (1 - abs((x - loc) / size)) * abs(area / size)

#--------------------Spectrum model functionality----------------------#


class Spectrum:
    """Set of 2D points and discrete components representing a spectrum"""

    def __init__(self):
        self.x = []  # x coordinates (energy) describing the continuum
        self.y = []  # y coordiantes (pdf) describing the continuum
        # Singular components of the spectrum, each list of the form [x, num,
        # relX]
        self.discrete = []
        # num is the area in the peak, x its center and relX a characteristic distance where it should extend
        # how that is represented depends on the window function used

    def clone(self):
        """Return a new Spectrum object cloning self"""
        s = Spectrum()
        s.x = list(self.x)
        s.y = self.y[:]
        s.discrete = self.discrete[:]
        return s

    def get_continuous_function(self):
        """Get an interpolation function representing the continuous part of the spectrum"""
        return interpolate.interp1d(self.x, self.y, bounds_error=False, fill_value=0)

    def get_points(self, peak_shape=triangle, num_discrete=10):
        """Returns two lists of coordinates x y representing the whole spectrum, both the continuos and discrete component
            The mesh is chosen by extending self.x to include details of the discrete peaks num_discrete points are added for each peak.
            peak_shape is a window function used to calculate the peaks. See xpecgen.triangle for a prototypical example.
        """
        if peak_shape == None or self.discrete == []:
            return self.x[:], self.y[:]
        # A mesh for each discrete component:
        discrete_mesh = np.concatenate(list(map(lambda x: np.linspace(
            x[0] - x[2], x[0] + x[2], num=num_discrete, endpoint=True), self.discrete)))
        x2 = sorted(np.concatenate((discrete_mesh, self.x)))
        f = self.get_continuous_function()
        peak = np.vectorize(peak_shape)

        def g(x):
            t = 0
            for l in self.discrete:
                t += peak(x, loc=l[0], size=l[2]) * l[1]
            return t
        y2 = [f(x) + g(x) for x in x2]
        return x2, y2

    def get_plot(self, place, show_mesh=True, prepare_format=True, peak_shape=triangle):
        """Prepare a plot of the data in the given place"""
        if prepare_format:
            place.tick_params(axis='both', which='major', labelsize=10)
            place.tick_params(axis='both', which='minor', labelsize=8)
            place.set_xlabel('E', fontsize=10, fontweight='bold')
            place.set_ylabel('f(E)', fontsize=10, fontweight='bold')

        x2, y2 = self.get_points(peak_shape=peak_shape)
        if show_mesh:
            place.plot(self.x, self.y, 'bo', x2, y2, 'b-')
        else:
            place.plot(x2, y2, 'b-')
        return

    def show_plot(self, joined=True, block=True):
        """Prepare the plot of the data and show it in mutplotlib window """
        plt.clf()
        self.get_plot(plt, prepare_format=False)
        plt.xlabel("E")
        plt.ylabel("f(E)")
        plt.gcf().canvas.set_window_title("".join(('xpecgen v', __version__)))
        plt.show(block=block)

    def export_csv(self, route="a.csv", peak_shape=triangle, transpose=False):
        """Export the data to a csv file (comma-separated values)"""
        x2, y2 = self.get_points(peak_shape=peak_shape)
        with open(route, 'w') as csvfile:
            w = csv.writer(csvfile, dialect='excel')
            if transpose:
                w.writerows([list(a) for a in zip(*[x2, y2])])
            else:
                w.writerow(x2)
                w.writerow(y2)

    def export_xlsx(self, route="a.xlsx", peak_shape=triangle, markers=False):
        """Export the data to a xlsx file (Excel format)"""
        x2, y2 = self.get_points(peak_shape=peak_shape)

        workbook = xlsxwriter.Workbook(route)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        worksheet.write(0, 0, "Energy (keV)", bold)
        worksheet.write(0, 1, "Photon density (1/keV)", bold)
        worksheet.write_column('A2', x2)
        worksheet.write_column('B2', y2)

        # Add a plot
        if markers:
            chart = workbook.add_chart(
                {'type': 'scatter', 'subtype': 'straight_with_markers'})
        else:
            chart = workbook.add_chart(
                {'type': 'scatter', 'subtype': 'straight'})

        chart.add_series({
            'name':       '=Sheet1!$B$1',
            'categories': '=Sheet1!$A$2:$A$' + str(len(x2) + 1),
            'values':     '=Sheet1!$B$2:$B$' + str(len(y2) + 1),
        })
        chart.set_title({'name': 'Emission spectrum'})
        chart.set_x_axis(
            {'name': 'Energy (keV)', 'min': 0, 'max': str(x2[-1])})
        chart.set_y_axis({'name': 'Photon density (1/keV)'})
        chart.set_legend({'position': 'none'})
        chart.set_style(11)

        worksheet.insert_chart('D3', chart, {'x_offset': 25, 'y_offset': 10})

        workbook.close()

    def get_norm(self, weight=None):
        """Return the norm of the spectrum using a weighting function
            weight(E)=1              ->Photon number (Default)
            weight(E)=E              ->Energy
            weight(E)=fluence2Dose(E)->Dose
        """
        if weight == None:
            w = lambda x: 1
        else:
            w = weight
        y2 = list(map(lambda x, y: w(x) * y, self.x, self.y))
        return integrate.simps(y2, x=self.x) + sum([w(a[0]) * a[1] for a in self.discrete])

    def set_norm(self, value=1, weight=None):
        """Set the norm of the spectrum to the given value using a weighting function
            w(E)=1              ->Photon number (Default)
            w(E)=E              ->Energy
            w(E)=fluence2Dose(E)->Dose
        """
        norm = self.get_norm(weight=weight) / value
        self.y = [a / norm for a in self.y]
        self.discrete = [[a[0], a[1] / norm, a[2]] for a in self.discrete]

    def hvl(self, value=0.5, weight=lambda x: 1, mu=lambda x: 1, energy_min=0):
        """Calculate a generalized HVL
            This method calculates the depth of a material with attenuation described by mu
            which is needed for the weighted integral of the spectrum to decay in a factor
            given by value (should be in (0,1))
        """
        # TODO: (?) Cut characteristic if below cutoff. However, such a high cutoff
        # would probably make no sense

        # Use low-energy cutoff
        lowIndex = bisect_left(self.x, energy_min)
        x = self.x[lowIndex:]
        y = self.y[lowIndex:]
        # Normalize to 1 with weighting function
        y2 = list(map(lambda a, b: weight(a) * b, x, y))
        discrete2 = [weight(a[0]) * a[1] for a in self.discrete]
        n2 = integrate.simps(y2, x=x) + sum(discrete2)
        y3 = [a / n2 for a in y2]
        discrete3 = [[a[0], weight(a[0]) * a[1] / n2] for a in self.discrete]
        # Now we only need to add attenuation as a function of depth
        f = lambda t: integrate.simps(list(map(lambda a, b: b * math.exp(-mu(a) * t), x, y3)), x=x) + sum(
            [c[1] * math.exp(-mu(c[0]) * t) for c in discrete3]) - value
        # Search the order of magnitude of the root (using the fact that f is
        # monotonically decreasing)
        a = 1.0
        if f(a) > 0:
            while(f(a) > 0):
                a *= 10.0
            # Now f(a)<=0 and f(a*0.1)>0
            return optimize.brentq(f, a * 0.1, a)
        else:
            while(f(a) < 0):
                a *= 0.1
            # Now f(a)>=0 and f(a*10)<0
            return optimize.brentq(f, a, a * 10.0)

    def attenuate(self, depth=1, mu=lambda x: 1):
        """Attenuate the spectra as if passed thorough a given depth of material with attenuation described by mu
            Use consistent units in depth and mu.
        """
        self.y = list(
            map(lambda x, y: y * math.exp(-mu(x) * depth), self.x, self.y))
        self.discrete = list(
            map(lambda l: [l[0], l[1] * math.exp(-mu(l[0]) * depth), l[2]], self.discrete))

#--------------------Spectrum calculation functionality----------------#


def get_fluence(E0=100):
    """Returns a function representing fluence(x,u) with x in CSDA units"""
    # List of available energies
    E0_str_list = list(map(lambda x: (os.path.split(x)[1]).split(".csv")[
                       0], glob(os.path.join(data_path, "fluence", "*.csv"))))
    E0_list = sorted(list(map(int, list(filter(str.isdigit, E0_str_list)))))

    E_closest = min(E0_list, key=lambda x: abs(x - E0))

    with open(os.path.join(data_path,"fluence/grid.csv"), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        t = next(r)
        x = np.array([float(a) for a in t[0].split(",")])
        t = next(r)
        u = np.array([float(a) for a in t[0].split(",")])
    t = []
    with open(os.path.join(data_path,"fluence","".join([str(E_closest), ".csv"])), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        for row in r:
            t.append([float(a) for a in row[0].split(",")])
    t = np.array(t)
    f = interpolate.RectBivariateSpline(x, u, t, kx=1, ky=1)
    # Note f is returning numpy 1x1 arrays
    return f
    # return lambda x,u:f(x,u)[0]


def get_cs(E0=100):
    """Returns a function representing cross_section(e_g,u) with e_g in keV
    Physical dimessions are mb/keV
    Note E0 is being used to scale u=e_e/E0
    """
    # NOTE: Data is given for E0>1keV. CS values below this level should be used with caution.
    # The default behaviour is to keep it constant
    with open(os.path.join(data_path,"cs/grid.csv"), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        t = next(r)
        e_e = np.array([float(a) for a in t[0].split(",")])
        log_e_e = np.log10(e_e)
        t = next(r)
        k = np.array([float(a) for a in t[0].split(",")])
    t = []
    with open(os.path.join(data_path,"cs/74.csv"), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        for row in r:
            t.append([float(a) for a in row[0].split(",")])
    t = np.array(t)
    scaled = interpolate.RectBivariateSpline(log_e_e, k, t, kx=3, ky=1)
    mElectron = 511
    Z2 = 74 * 74
    return lambda Eg, u: (u * E0 + mElectron)**2 * Z2 / (u * E0 * Eg * (u * E0 + 2 * mElectron)) * (scaled(np.log10(u * E0), Eg / (u * E0)))


def get_mu(Z=74):
    """Returns a function representing mu(E) with mu in cm^-1 and E in keV for the given material"""
    with open(os.path.join(data_path,"mu","".join([str(Z), ".csv"])), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        t = next(r)
        x = [float(a) for a in t[0].split(",")]
        t = next(r)
        y = [float(a) for a in t[0].split(",")]
    return logInterp1d(x, y)


def get_csda():
    """Returns a function representing the CSDA range in cm in tungsten as a function of E0 in keV"""
    with open(os.path.join(data_path,"csda/74.csv"), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        t = next(r)
        x = [float(a) for a in t[0].split(",")]
        t = next(r)
        y = [float(a) for a in t[0].split(",")]
    return interpolate.interp1d(x, y, kind='linear')


def get_mu_csda(E0):
    """Returns a function representing mu(E) in tungsten with mu in CSDA units"""
    mu = get_mu(74)
    csda = get_csda()(E0)
    return lambda E: mu(E) * csda


def get_fluence_to_dose():
    """Returns a function representing the weighting factor which converts fluence to dose"""
    with open(os.path.join(data_path,"fluence2dose/f2d.csv"), 'r') as csvfile:
        r = csv.reader(csvfile, delimiter=' ', quotechar='|',
                       quoting=csv.QUOTE_MINIMAL)
        t = next(r)
        x = [float(a) for a in t[0].split(",")]
        t = next(r)
        y = [float(a) for a in t[0].split(",")]
    return interpolate.interp1d(x, y, kind='linear')


def get_source_function(fluence, cs, mu, theta, eg, phi=0.0):
    """Returns the attenuated source function for given parameters
    Constant factors are excluded
    s(u,x)
    """
    factor = -mu(eg) / math.sin(math.radians(theta)) / \
        math.cos(math.radians(phi))
    return lambda u, x: fluence(x, u) * cs(eg, u) * math.exp(factor * x)


def integrate_source(fluence, cs, mu, theta, e_g, e_0, phi=0.0, x_min=0.0, x_max=0.6, epsrel=0.1):
    """Find the integral of the source functions for a given photon energy eg
    Constant factors are excluded"""
    if e_g == e_0:
        return 0
    f = get_source_function(fluence, cs, mu, theta, e_g, phi=phi)
    (y, yerr) = custom_dblquad(f, x_min, x_max,
                               e_g / e_0, 1, epsrel=epsrel, limit=100)
    return y


def add_char_radiation(s, method="fraction_above_poly"):
    """Adds characteristic radiation to a calculated bremsstrahlung spectrum
       if a singular component exists in the spectrum, it is replaced.
       Available methods:
       - fraction_above_linear: Use a linear relation between bremsstrahlung above the K-edge and peaks
       - fraction_above_poly: Use polynomial fits between bremsstrahlung above the K-edge and peaks
    """
    s.discrete = []
    if s.x[-1] < 69.51:  # If under k edge, no char radiation
        return

    f = s.get_continuous_function()
    norm = integrate.quad(f, s.x[0], s.x[-1], limit=2000)[0]
    fraction_above = integrate.quad(f, 74, s.x[-1], limit=2000)[0] / norm

    if method == "fraction_above_linear":
        s.discrete.append([58.65, 0.1639 * fraction_above * norm, 1])
        s.discrete.append([67.244, 0.03628 * fraction_above * norm, 1])
        s.discrete.append([69.067, 0.01410 * fraction_above * norm, 1])
    else:
        if method != "fraction_above_poly":
            print(
                "WARNING: Unknown char radiation calculation method. Using fraction_above_poly")
        s.discrete.append([58.65, (0.1912 * fraction_above - 0.00615 *
                                   fraction_above**2 - 0.1279 * fraction_above**3) * norm, 1])
        s.discrete.append([67.244, (0.04239 * fraction_above + 0.002003 *
                                    fraction_above**2 - 0.02356 * fraction_above**3) * norm, 1])
        s.discrete.append([69.067, (0.01437 * fraction_above + 0.002346 *
                                    fraction_above**2 - 0.009332 * fraction_above**3) * norm, 1])

    return


def console_monitor(a, b):
    """Simple monitor function which can be used with calculate_spectrum"""
    print("Calculation: ", a, "/", b)


def calculate_spectrum(E0, theta, eMin, numE, phi=0.0, epsrel=0.2, monitor=console_monitor):
    """Calculates the x-ray spectrum for given parameters.
       monitor defines a function to be called after each iteration,
       with arguments finished_count, total_count
       Characteristic peaks are also calculated by add_char_radiation, which is called with the default parameters.
    """
    # Prepare spectrum
    s = Spectrum()
    s.x = np.linspace(eMin, E0, num=numE, endpoint=True)
    # Prepare integrad function
    fluence = get_fluence(E0)
    cs = get_cs(E0)
    mu = get_mu_csda(E0)

    # quad may raise warnings about the numerical integration method,
    # which are related to the estimated accuracy. Since this is not relevant,
    # they are suppressed.
    warnings.simplefilter("ignore")

    # TODO: (?) multiprocessing might be added here in the future
    for i, e_g in enumerate(s.x):
        s.y.append(integrate_source(fluence, cs, mu,
                                    theta, e_g, E0, phi=phi, epsrel=epsrel))
        if monitor != None:
            monitor(i + 1, numE)

    add_char_radiation(s)

    return s

#---------------------Debug utilities----------------------------------#


def plot_function(f, x_min, x_max, num=100):
    """Plot a function in independent matplotlib window"""
    x = np.linspace(x_min, x_max, num=num, endpoint=True)
    # Instead of y=list(map(f,x)) we vectorize the function to deal with functions returning numpy arrays
    # FIXME: This can lead to problems if local variables are used in the given function!!!
    # Cf. triangle function for an example
    f2 = np.vectorize(f)
    y = f2(x)
    plt.plot(x, y, '-')
    plt.show()
