#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""xpecgenGUI.py: A GUI for the xpecgen module"""


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
__author__ = "Dih5"
#----------------------------------------------------------------------#


from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from tkinter import messagebox

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


import threading
import queue

import os

from glob import glob

import re #Regular expressions, used for sorting


from . import xpecgen as xg



class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    # Based on the content from this post:
    # http://stackoverflow.com/questions/3221956/what-is-the-simplest-way-to-make-tooltips-in-tkinter

    def __init__(self, widget, text, color="#ffe14c"):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.color = color
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                      background=self.color, relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class ParBox():
    """Add a parameter entry with labels preceding and succeeding it and a tooltip"""

    def __init__(self, master=None, textvariable=0, lblText="", unitsTxt="", helpTxt="", row=0, read_only=False):

        self.lbl = Label(master, text=lblText)
        self.lbl.grid(row=row, column=0, sticky=W)

        self.txt = Entry(master, textvariable=textvariable)
        self.txt.grid(row=row, column=1, sticky=W + E)

        self.units = Label(master, text=unitsTxt, anchor=W)
        self.units.grid(row=row, column=2, sticky=W)

        if helpTxt != "":
            self.lblTT = CreateToolTip(self.lbl, helpTxt)
            self.txtTT = CreateToolTip(self.txt, helpTxt)
        if read_only:
            self.txt["state"]="readonly"
            


class XpecgenGUI(Notebook):

    def __init__(self, master=None):
        Notebook.__init__(self, master)
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        self.grid(row=0, column=0, sticky=N + S + E + W)
        self.master.title("".join(('xpecgen v', xg.__version__, " GUI")))
        #self.master.minsize(800, 600)

        self.spectra = []
        self.spectra_labels = []
        self.active_spec = 0  # The active spectrum from the list
        
        #Interpolations used to calculate HVL
        self.fluence_to_dose=xg.get_fluence_to_dose()
        self.mu_Al=xg.get_mu(13)
        self.mu_Cu=xg.get_mu(29)

        self.initVariables()
        self.createWidgets()

        self.history_poll()
        

    def history_poll(self):
        '''Polling method to update changes in spectrum list
           Tk manual advised for polling instead of binding all methods
           that are able to change a listbox
        '''
        try:
            now = self.lstHistory.curselection()[0]
            if now != self.active_spec:
                self.active_spec = now
                self.update_plot()

        except IndexError:
            pass
        self.after(150, self.history_poll)

    def initVariables(self):
        """Create and initialize interface variables"""

        # Calculation-related variables
        self.E0 = DoubleVar()
        self.E0.set(100.0)

        self.Theta = DoubleVar()
        self.Theta.set(12.0)

        self.Phi = DoubleVar()
        self.Phi.set(0.0)

        self.EMin = DoubleVar()
        self.EMin.set(3.0)

        self.NumE = IntVar()
        self.NumE.set(50)

        self.Eps = DoubleVar()
        self.Eps.set(0.5)

        # Operation-related variables

        self.AttenMaterial = StringVar()
        self.AttenMaterial.set("13")

        self.AttenThick = DoubleVar()
        self.AttenThick.set(0.1)
        
        self.NormCriterion = StringVar()
        self.NormCriterion.set("Number")
        
        self.NormValue = DoubleVar()
        self.NormValue.set(1.0)
        
        #Output HVLs
        self.HVL1 = StringVar()
        self.HVL1.set("0")
        self.HVL2 = StringVar()
        self.HVL2.set("0")
        self.HVL3 = StringVar()
        self.HVL3.set("0")
        self.HVL4 = StringVar()
        self.HVL4.set("0")
        #Output Norms
        self.number = StringVar()
        self.number.set("0")
        self.energy = StringVar()
        self.energy.set("0")
        self.dose = StringVar()
        self.dose.set("0")

    def createWidgets(self):
        """Create the widgets in the GUI"""
        self.frmCalc = Frame(self)
        self.frmAnal = Frame(self)
        self.add(self.frmCalc, text='Calculate')
        self.add(self.frmAnal, text='Analyze')

        #self.frmCalc.grid(sticky=N+S+E+W, column=0, row=0)

        # Calculate Tab

        #-Physical parameters
        self.frmPhysPar = LabelFrame(self.frmCalc, text="Physical parameters")
        self.frmPhysPar.grid(row=0, column=0, sticky=N + S + E + W)
        self.ParE0 = ParBox(self.frmPhysPar, self.E0, lblText="Electron Energy (E0)",
                            unitsTxt="keV", helpTxt="Electron kinetic energy in keV.", row=0)
        self.ParTheta = ParBox(self.frmPhysPar, self.Theta, lblText=u"Angle (\u03b8)",
                               unitsTxt="º", helpTxt="X-rays emission angle. The anode's normal is at 90º.", row=1)
        self.ParPhi = ParBox(self.frmPhysPar, self.Phi, lblText=u"Elevation angle (\u03c6)",
                             unitsTxt="º", helpTxt="X-rays emission altitude. The anode's normal is at 0º.", row=2)
        Grid.columnconfigure(self.frmPhysPar, 0, weight=0)
        Grid.columnconfigure(self.frmPhysPar, 1, weight=1)
        Grid.columnconfigure(self.frmPhysPar, 2, weight=0)

        #-Numerical Parameters
        self.frmNumPar = LabelFrame(self.frmCalc, text="Numerical parameters")
        self.frmNumPar.grid(row=0, column=1, sticky=N + S + E + W)
        self.ParEMin = ParBox(self.frmNumPar, self.EMin,
                              lblText="Min energy", unitsTxt="keV", helpTxt="Minimum kinetic energy in the bremsstrahlung calculation. Note this might influence the characteristic peaks prediction.", row=0)
        self.ParNumE = ParBox(self.frmNumPar, self.NumE,
                              lblText="Number of points", unitsTxt="", helpTxt="Amount of points for the mesh were the bremsstrahlung spectrum is calculated.\nBremsstrahlung component is extended by interpolation.",row=1)
        self.ParEps = ParBox(self.frmNumPar, self.Eps, lblText="Integrating tolerance", unitsTxt="",
                             helpTxt="A numerical tolerance parameter used in numerical integration. Values around 0.5 provide fast and accurate calculations. If you want insanely accurate (and physcally irrelevant) numerical integration you can reduce this value, increasing computation time.", row=2)
        Grid.columnconfigure(self.frmNumPar, 0, weight=0)
        Grid.columnconfigure(self.frmNumPar, 1, weight=1)
        Grid.columnconfigure(self.frmNumPar, 2, weight=0)

        #-Buttons, status bar...
        self.cmdCalculate = Button(self.frmCalc, text="Calculate")
        self.cmdCalculate["command"] = self.calculate
        self.cmdCalculate.bind('<Return>', lambda event: self.calculate())
        self.cmdCalculate.bind(
            '<KP_Enter>', lambda event: self.calculate())  # Enter (num. kb)
        self.cmdCalculate.grid(row=1, column=0, sticky=E + W)

        self.barProgress = Progressbar(
            self.frmCalc, orient="horizontal", length=100, mode="determinate")
        self.barProgress.grid(row=1, column=1, columnspan=1, sticky=E + W)

        Grid.columnconfigure(self.frmCalc, 0, weight=1)
        Grid.columnconfigure(self.frmCalc, 1, weight=1)

        Grid.rowconfigure(self.frmCalc, 0, weight=1)
        Grid.rowconfigure(self.frmCalc, 1, weight=0)

        # Analyze tab

        #-History frame
        self.frmHist = LabelFrame(self.frmAnal, text="History")
        self.frmHist.grid(row=0, column=0, sticky=N + S + E + W)
        self.lstHistory = Listbox(self.frmHist, selectmode=BROWSE)
        self.lstHistory.grid(row=0, column=0, sticky=N + S + E + W)
        self.scrollHistory = Scrollbar(self.frmHist, orient=VERTICAL)
        self.scrollHistory.grid(row=0, column=1, sticky=N + S)
        self.lstHistory.config(yscrollcommand=self.scrollHistory.set)
        self.scrollHistory.config(command=self.lstHistory.yview)
        self.cmdCleanHistory = Button(self.frmHist, text="Revert to selected", state=DISABLED)
        self.cmdCleanHistory["command"] = self.clean_history
        self.cmdCleanHistory.grid(row=1, column=0, columnspan=2,sticky=E + W)
        self.cmdExport = Button(self.frmHist, text="Export selected", state=DISABLED)
        self.cmdExport["command"] = self.export
        self.cmdExport.grid(row=2, column=0, columnspan=2,sticky=E + W)

        Grid.rowconfigure(self.frmHist, 0, weight=1)
        Grid.columnconfigure(self.frmHist, 0, weight=1)
        Grid.columnconfigure(self.frmHist, 1, weight=0)

        #-Operations frame
        self.frmOper = LabelFrame(self.frmAnal, text="Spectrum operations")
        self.frmOper.grid(row=1, column=0, sticky=N + S + E + W)
        #--Attenuation
        self.frmOperAtten = LabelFrame(self.frmOper, text="Attenuate")
        self.frmOperAtten.grid(row=0, column=0, sticky=N + S + E + W)
        self.lblAttenMaterial = Label(self.frmOperAtten, text="Material")
        self.lblAttenMaterial.grid()
        self.cmbAttenMaterial = Combobox(
            self.frmOperAtten, textvariable=self.AttenMaterial)
        material_list=list(map(lambda x: (os.path.split(x)[1]).split(
            ".csv")[0], glob(os.path.join(xg.data_path, "mu", "*.csv"))))


        def human_order_key(text):
            '''
            key function to sort in human order. Based in:
            http://nedbatchelder.com/blog/200712/human_sorting.html
            '''
            return [ int(c) if c.isdigit() else c for c in re.split('(\d+)', text) ]
        material_list.sort(key=human_order_key)
        self.cmbAttenMaterial["values"] = material_list
        self.cmbAttenMaterial.grid(row=0, column=1, sticky=E + W)
        self.ParAttenThick = ParBox(
            self.frmOperAtten, self.AttenThick, lblText="Thickness", unitsTxt="cm", row=1)
        self.cmdAtten = Button(self.frmOperAtten, text="Add attenuation", state=DISABLED)
        self.cmdAtten["command"] = self.attenuate
        self.cmdAtten.grid(row=2, column=0, columnspan=3, sticky=E + W)
        Grid.columnconfigure(self.frmOperAtten, 0, weight=0)
        Grid.columnconfigure(self.frmOperAtten, 1, weight=1)
        Grid.columnconfigure(self.frmOperAtten, 2, weight=0)
        
        #--Normalize
        self.frmOperNorm = LabelFrame(self.frmOper, text="Normalize")
        self.frmOperNorm.grid(row=1, column=0, sticky=N + S + E + W)
        self.lblNormCriterion = Label(self.frmOperNorm, text="Criterion")
        self.lblNormCriterion.grid()
        self.cmbNormCriterion = Combobox(
            self.frmOperNorm, textvariable=self.NormCriterion)
        self.criteriaList = ["Number", "Energy (keV)", "Dose (mGy)"]
        self.cmbNormCriterion["values"] = self.criteriaList
        self.cmbNormCriterion.grid(row=0, column=1, sticky=E + W)
        self.ParNormValue = ParBox(
            self.frmOperNorm, self.NormValue, lblText="Value", unitsTxt="", row=1)
        self.cmdNorm = Button(self.frmOperNorm, text="Normalize", state=DISABLED)
        self.cmdNorm["command"] = self.normalize
        self.cmdNorm.grid(row=2, column=0, columnspan=3, sticky=E + W)
        Grid.columnconfigure(self.frmOperNorm, 0, weight=0)
        Grid.columnconfigure(self.frmOperNorm, 1, weight=1)
        Grid.columnconfigure(self.frmOperNorm, 2, weight=0)

        Grid.columnconfigure(self.frmOper, 0, weight=1)
        Grid.rowconfigure(self.frmOper, 0, weight=1)

        #-Plot frame
        self.frmPlot = Frame(self.frmAnal)

        try:
            self.fig = Figure(figsize=(5, 4), dpi=100,
                              facecolor=self.master["bg"])
            self.subfig = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.frmPlot)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

            self.canvasToolbar = NavigationToolbar2TkAgg(
                self.canvas, self.frmPlot)
            self.canvasToolbar.update()
            self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

            self.frmPlot.grid(row=0, column=1, rowspan=3, sticky=N + S + E + W)

            self.matplotlib_embedded = True
        except Exception:
            self.matplotlib_embedded = False
            #self.cmdShowPlot = Button(self.frmPlot,text="Open plot window")
            #self.cmdShowPlot["command"] = self.update_plot
            # self.cmdShowPlot.grid(row=0,column=0)
            print("WARNING: Matplotlib couldn't be embedded in TkAgg.\nUsing independent window instead", file=sys.stderr)
            
        #--Spectral parameters frame
        self.frmSpectralParameters = LabelFrame(self.frmAnal, text="Spectral parameters")
        self.frmSpectralParameters.grid(row=2, column=0, sticky= S + E + W)
        self.ParHVL1 = ParBox(self.frmSpectralParameters, self.HVL1, lblText="1HVL Al", unitsTxt="cm", row=0, read_only=True, helpTxt="Thickness of Al at which the dose produced by the spectrum is halved, according to the exponential attenuation model.")
        self.ParHVL2 = ParBox(self.frmSpectralParameters, self.HVL2, lblText="2HVL Al", unitsTxt="cm", row=1, read_only=True, helpTxt="Thickness of Al at which the dose produced by the spectrum after crossing a HVL is halved again, according to the exponential attenuation model.")
        self.ParHVL3 = ParBox(self.frmSpectralParameters, self.HVL3, lblText="1HVL Cu", unitsTxt="cm", row=2, read_only=True, helpTxt="Thickness of Cu at which the dose produced by the spectrum is halved, according to the exponential attenuation model.")
        self.ParHVL4 = ParBox(self.frmSpectralParameters, self.HVL4, lblText="2HVL Cu", unitsTxt="cm", row=3, read_only=True, helpTxt="Thickness of Cu at which the dose produced by the spectrum after crossing a HVL is halved again, according to the exponential attenuation model.")
        self.ParNorm = ParBox(self.frmSpectralParameters, self.number, lblText="Photon number", unitsTxt="", row=4, read_only=True, helpTxt="Number of photons in the spectrum.")
        self.ParEnergy = ParBox(self.frmSpectralParameters, self.energy, lblText="Energy", unitsTxt="keV", row=5, read_only=True, helpTxt="Total energy in the spectrum.")
        self.ParDose = ParBox(self.frmSpectralParameters, self.dose, lblText="Dose", unitsTxt="mGy", row=6, read_only=True, helpTxt="Dose produced in air by the spectrum, assuming it is describing the differential fluence in particles/keV/cm^2.")
       

        Grid.columnconfigure(self.frmAnal, 0, weight=1)
        if self.matplotlib_embedded:
            # If not embeddeding, use the whole window
            Grid.columnconfigure(self.frmAnal, 1, weight=3)

        Grid.rowconfigure(self.frmAnal, 0, weight=1)
        Grid.rowconfigure(self.frmAnal, 1, weight=1)
        
    def enable_analyze_buttons(self):
        """Enable widgets requiring a calculated spectrum to work"""
        self.cmdCleanHistory["state"] = "normal"
        self.cmdExport["state"] = "normal"
        self.cmdAtten["state"] = "normal"
        self.cmdNorm["state"] = "normal"
        pass

    def update_plot(self):
        """Update the canvas after plotting something
           If matplotlib is not embedded, show it in an independent window
        """
        if self.matplotlib_embedded:
            self.subfig.clear()
            self.spectra[self.active_spec].get_plot(self.subfig)
            self.canvas.draw()
            self.canvasToolbar._views.clear()
            self.canvasToolbar._positions.clear()
            self.canvasToolbar._update_view()
            self.fig.tight_layout()
        else:
            # FIXME: Update if independent window is oppened
            self.spectra[self.active_spec].show_plot(block=False)
        self.update_param()
        
    def update_param(self):
        """Update parameters calculated from the active spectrum"""
        hvlAl=self.spectra[self.active_spec].hvl(0.5,self.fluence_to_dose,self.mu_Al)
        qvlAl=self.spectra[self.active_spec].hvl(0.25,self.fluence_to_dose,self.mu_Al)

        hvlCu=self.spectra[self.active_spec].hvl(0.5,self.fluence_to_dose,self.mu_Cu)
        qvlCu=self.spectra[self.active_spec].hvl(0.25,self.fluence_to_dose,self.mu_Cu)

        #TODO: (?) cache the results
        self.HVL1.set('%s' % float('%.3g' % hvlAl))
        self.HVL2.set('%s' % float('%.3g' % (qvlAl-hvlAl)))
        self.HVL3.set('%s' % float('%.3g' % hvlCu))
        self.HVL4.set('%s' % float('%.3g' % (qvlCu-hvlCu)))
        
        self.number.set('%s' % float('%.3g' % (self.spectra[self.active_spec].get_norm())))
        self.energy.set('%s' % float('%.3g' % (self.spectra[self.active_spec].get_norm(lambda x:x))))
        self.dose.set('%s' % float('%.3g' % (self.spectra[self.active_spec].get_norm(self.fluence_to_dose))))

    def monitor_bar(self, a, b):
        """Update the progress bar"""
        self.barProgress["value"] = a
        self.barProgress["maximum"] = b

    def clean_history(self):
        try:
            now = int(self.lstHistory.curselection()[0])
            if now == len(self.spectra) - 1:  # No need to slice
                return
            self.spectra = self.spectra[0:now + 1]
            self.lstHistory.delete(now + 1, END)

        except IndexError:  # Ignore if nothing selected
            pass
        
    def export(self):
        if self.lstHistory.curselection()==():
            selection=-1
        else:
            selection=int(self.lstHistory.curselection()[0])
        file_opt = options = {}
        options['defaultextension'] = '.xlsx'
        options['filetypes'] = [('Excel Spreadsheet', '.xlsx'), ('Comma-separated values', '.csv')]
        options['initialfile'] = 'spectrum.xlsx'
        options['parent'] = self
        options['title'] = 'Export spectrum'
        filename = tkinter.filedialog.asksaveasfilename(**file_opt)
        if not filename: #Ignore if canceled
            return
        ext=filename.split(".")[-1]

        if ext=="xlsx":
            self.spectra[selection].export_xlsx(filename)
        elif ext=="csv":
            self.spectra[selection].export_csv(filename)
        else:
            messagebox.showerror("Error", "Unknown file extension: "+ext+"\nUse the file types from the dialog to export.")
        pass

    def calculate(self):
        """Calculates a new spectrum"""
        def callback(): #Carry calculation in a different thread to avoid blocking
            s = xg.calculate_spectrum(self.E0.get(), self.Theta.get(), self.EMin.get(
            ), self.NumE.get(), phi=self.Phi.get(), epsrel=self.Eps.get(), monitor=self.monitor_bar)
            self.spectra = [s]
            self.lstHistory.delete(0, END)
            self.lstHistory.insert(END, "Calculated")
            self.queue_calculation.put(1)

        try:
            if self.calc_thread.is_alive():
                # NOTE: This point should be unreachable since cmdCalculate is disabled when calculated
                # In a future it could serve to stop the calculation
                print("WARNING: The calculation can not be stopped in the current version.\nIf you want to abort it, close the application.", file=sys.stderr)
                # TODO: Ask child to stop
                return
        except AttributeError:  # If there is no calculation thread, there is nothing to worry about
            pass
        self.queue_calculation = queue.Queue(maxsize=1)
        # The child will fill the queue to indicate it has ended.
        # The father might fill the queue to ask the children to stop TODO: Not
        # done yet
        self.calc_thread = threading.Thread(target=callback)
        self.calc_thread.setDaemon(True)
        self.calc_thread.start()
        
        self.cmdCalculate["state"]="disabled"
        self.after(250, self.wait_for_calculation)

    def wait_for_calculation(self):
        '''Polling method to wait for the calculation thread to finish
        '''
        if self.queue_calculation.full():
            self.cmdCalculate["state"]="normal"
            self.enable_analyze_buttons()
            self.monitor_bar(0,0)
            self.active_spec = 0
            self.update_plot()
            self.select(1)  # Open analyse tab
        else:
            self.after(250, self.wait_for_calculation)

    def attenuate(self):
        """Attenuate the active spectrum"""
        s2 = self.spectra[-1].clone()
        s2.attenuate(self.AttenThick.get(),
                     xg.get_mu(self.AttenMaterial.get()))
        self.spectra.append(s2)
        self.lstHistory.insert(
            END, "Attenuated: " + str(self.AttenThick.get()) + "cm of " + self.AttenMaterial.get())
        self.lstHistory.selection_clear(0, len(self.spectra) - 2)
        self.lstHistory.selection_set(len(self.spectra) - 1)
        self.update_plot()
        pass
        
    def normalize(self):
        """Normalize the active spectrum"""
        value=self.NormValue.get()
        crit = self.NormCriterion.get()
        if value<=0:
            messagebox.showerror("Error", "The norm of a spectrum must be a positive number.")
            return
        if crit not in self.criteriaList:
            messagebox.showerror("Error", "An unkown criterion was selected.")
            return
        s2 = self.spectra[-1].clone()
        if crit==self.criteriaList[0]:
            s2.set_norm(value)
        elif crit==self.criteriaList[1]:
            s2.set_norm(value,lambda x:x)
        else: #criteriaList[2]
            s2.set_norm(value,self.fluence_to_dose)
        self.spectra.append(s2)
        self.lstHistory.insert(
            END, "Normalized: " + crit + " = " + str(value))
        self.lstHistory.selection_clear(0, len(self.spectra) - 2)
        self.lstHistory.selection_set(len(self.spectra) - 1)
        self.update_plot()
        pass

def main():
    root = Tk()
    app = XpecgenGUI(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
