# -*- coding: utf-8 -*-
"""Testing and demonstrating program for pytwobodyorbit
Created on Fri Dec 14 08:44:47 2018

@author: Shushi Uetsuki/whiskie14142
"""

import numpy as np
import tkinter
from pytwobodyorbit import TwoBodyOrbit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib

# Standard gravitational parameter for the Sun
# With this parameter, lenght should be in meters,
# and time should be in seconds
mu = 1.32712440041e20

# Create instance of TwoBodyOrbit
orbit = TwoBodyOrbit('object', mmu=mu)

# Seconds of a day
secofday = 86400.0

# prepare plotting
matplotlib.rcParams['toolbar'] = 'none'
plt.ion()                       # set pyplot to the interactive mode
fig=plt.figure(figsize=(11,11))
ax=fig.gca(projection='3d', aspect='equal')
ax.set_clip_on(True)
ax.set_xlim(-3.0e11, 3.0e11)
ax.set_ylim(-3.0e11, 3.0e11)
ax.set_zlim(-3.0e11, 3.0e11)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
fig.tight_layout()
fig.canvas.set_window_title('3D Orbit')

ax.text2D(0.02, 1.00, 'Rotate: move mouse with L button held down', transform=ax.transAxes)
ax.text2D(0.02, 0.97, 'Zoom: move mouse up/down with R button held down', transform=ax.transAxes)

mngr = plt.get_current_fig_manager()
mngr.window.setGeometry(680, 40, 600, 600)


class TestConvert(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.arline = None
        self.arsc = None
        self.object = ['  epoch', '  t', '  Sun']
        self.arname = [None, None, None]

        self.create_widgets()
        
    def create_widgets(self):
        self.Lspace0 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace0.grid(row=0, column=0)

        self.comment = tkinter.Text(self, width=80, height=22, 
                        font=('Helvetica', 10), wrap=tkinter.WORD)
        scom = "This program demonstrates the 'TwoBodyOrbit' class of 'pytwobodyorbit'.\n\n" + \
            "An instance of the 'TwoBodyOrbit' can be set the orbital parameters of an object by classical orbital elements (a, e, i, etc.) or by Cartesian orbital elements (position and velocity), and it can outputs Cartesian orbital elements and classical orbital elements of the orbit.\n\n" + \
            "In this program, we can convert a set of classical orbital elements of an object, which is orbiting around the Sun, into a set of Cartesian orbital elements, and vice versa.  In addition, we can see the orbit as a drawing on the 3D chart.\n\n" + \
            "USAGE:\nEdit one set of the orbital elements and click one of the buttons to convert, [To Cartesian ⇒] or [⇐ To Classical].\nEdit one of the 'Time (t)' input field, and click one of the buttons to draw, [Draw from Classical Elements] or [Draw from Cartesian Elements].\n\n" + \
            "UNITS:\nLength - meters\nVelocity - meters per second\nTime - days\nAngle - degrees"

        self.comment.insert(1.0, scom)
        self.comment['state'] = tkinter.DISABLED
        self.comment.grid(row=1, column=0, columnspan=5)
        
        self.Lspace = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace.grid(row=2, column=0)
        
        self.Ltitle1 = tkinter.Label(self, text='Classical Orbital Elements')
        self.Ltitle1.grid(row=3, column=0, columnspan=2)
        
        self.KE_d = [
                'Epoch  ',
                'Semi-maj. axis (a)  ',
                'Eccentricity (e)  ',
                'Inclination (i)  ',
                'Long. of AN (LoAN)  ',
                'Arg. of P (AoP)  ',
                'True anomaly (TA)  ',
                'Periapsis passage (T)  ',
                'Mean anomaly (MA)  ']
        self.KE_v = [
                ' 0.000000',
                ' 1.49597870700e+11',
                ' 0.5000000000',
                ' 15.000000000',
                ' 60.000000000',
                ' 135.000000000',
                ' 0.000000000',
                ' 0.000000',
                ' 0.000000000']
        self.KE_L = []
        self.KE_SV = []
        self.KE_E = []
        self.radio = tkinter.IntVar()
        
        for j in range(9):
            if j < 6:
                self.KE_L.append(tkinter.Label(self, text=self.KE_d[j]))
            else:
                self.KE_L.append(tkinter.Radiobutton(self, text=self.KE_d[j], variable=self.radio, value=j, anchor=tkinter.E, command=self.radioclicked))
            self.KE_L[j].grid(row=j+4, column=0, sticky=tkinter.E)
            self.KE_SV.append(tkinter.StringVar(value=self.KE_v[j]))
            self.KE_E.append(tkinter.Entry(self, bd=1, textvariable=self.KE_SV[j]))
            self.KE_E[j].grid(row=j+4, column=1, sticky=tkinter.E)
        self.KE_L[6].select()
        self.KE_E[7]['state'] = tkinter.DISABLED
        self.KE_E[8]['state'] = tkinter.DISABLED

        self.Ltitle2 = tkinter.Label(self, text='Cartesian Orbital Elements')
        self.Ltitle2.grid(row=3, column=3, columnspan=2)
        
        self.CE_d = [
                '  Epoch',
                '  Position X',
                '  Position Y',
                '  Position Z',
                '  Velocity XD',
                '  Velocity YD',
                '  Velocity ZD']
        self.CE_v = [
                ' 0.000000',
                ' 1.00000000000e+11',
                ' 1.20000000000e+11',
                ' 0.20000000000e+11',
                '-2.00000000000e+04',
                ' 1.80000000000e+04',
                ' 0.00000000000e+00']

        self.CE_L = []
        self.CE_SV = []
        self.CE_E = []

        for j in range(7):
            self.CE_L.append(tkinter.Label(self, text=self.CE_d[j]))
            self.CE_L[j].grid(row=j+4, column=4, sticky=tkinter.W)
            self.CE_SV.append(tkinter.StringVar(value=self.CE_v[j]))
            self.CE_E.append(tkinter.Entry(self, bd=1, textvariable=self.CE_SV[j]))
            self.CE_E[j].grid(row=j+4, column=3, sticky=tkinter.W)

        self.K2C = tkinter.Button(self, width=15)
        self.K2C['text'] = '     To Cartesian ⇒'
        self.K2C['command'] = self.toCartesian
        self.K2C.grid(row=4, column=2, padx=3)

        self.C2K = tkinter.Button(self, width=15)
        self.C2K['text'] = '⇐ To Classical     '
        self.C2K['command'] = self.toClassical
        self.C2K.grid(row=5, column=2)
        
        self.cError = tkinter.Label(self, text=' ',
             anchor=tkinter.NW, justify=tkinter.LEFT, width=15, height=8, 
             font=('Arial',9,'bold'), wraplength=110)
        self.cError.grid(row=6, column=2, rowspan=5)
        

        self.Lspace3 = tkinter.Label(self, text=' ')
        self.Lspace3.grid(row=15, column=0)

        self.Kt_L = tkinter.Label(self, text='Time (t)  ')
        self.Kt_L.grid(row=16, column=0, sticky=tkinter.E)
        self.Kt_SV = tkinter.StringVar(value='100.0')
        self.Kt_E = tkinter.Entry(self, bd=1, textvariable=self.Kt_SV)
        self.Kt_E.grid(row=16, column=1, sticky=tkinter.E)
        
        self.Ct_L = tkinter.Label(self, text='  Time (t)')
        self.Ct_L.grid(row=16, column=4, sticky=tkinter.W)
        self.Ct_SV = tkinter.StringVar(value='100.0')
        self.Ct_E = tkinter.Entry(self, bd=1, textvariable=self.Ct_SV)
        self.Ct_E.grid(row=16, column=3, sticky=tkinter.W)

        self.Lspace4 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace4.grid(row=17, column=0)
        
        self.DfK = tkinter.Button(self)
        self.DfK['text'] = '  Draw from Classical Elements  '
        self.DfK['command'] = self.drawClassical
        self.DfK.grid(row=18, column=0, columnspan=2, sticky=tkinter.E)
        
        self.DfC = tkinter.Button(self)
        self.DfC['text'] = '  Draw from Cartesian Elements  '
        self.DfC['command'] = self.drawCartesian
        self.DfC.grid(row=18, column=3, columnspan=2, sticky=tkinter.W)

        self.dError = tkinter.Label(self, text=' ', font=('Arial',9,'bold'))
        self.dError.grid(row=29, column=0, columnspan=5)
        
        self.quitapp = tkinter.Button(self)
        self.quitapp['text'] = '    Quit    '
        self.quitapp['command'] = self.master.destroy
        self.quitapp.grid(row=30, column=4)

    def radioclicked(self):
        for j in range(6, 9):
            if j != self.radio.get():
                self.KE_E[j]['state'] = tkinter.DISABLED
            else:
                self.KE_E[j]['state'] = tkinter.NORMAL


        
    def toCartesian(self):
        classical = []
        for j in range(6):
            classical.append(float(self.KE_SV[j].get()))
        classical[0] *= secofday    # convert to seconds
        
        if self.radio.get() == 6:
            ta = float(self.KE_SV[6].get())
            try:
                orbit.setOrbKepl(*classical[0:6], TA=ta)
            except ValueError as ve:
                self.cError['text'] = ve.args[0]
                return
        elif self.radio.get() ==7:
            t = float(self.KE_SV[7].get()) * secofday
            try:
                orbit.setOrbKepl(*classical[0:6], T=t)
            except ValueError as ve:
                self.cError['text'] = ve.args[0]
                return
        else:
            ma = float(self.KE_SV[8].get())
            try:
                orbit.setOrbKepl(*classical[0:6], MA=ma)
            except ValueError as ve:
                self.cError['text'] = ve.args[0]
                return
        self.cError['text'] = ' '
        pos, vel = orbit.posvelatt(classical[0])  # pos, vel at epoch
        self.CE_SV[0].set('{: .6f}'.format(classical[0] / secofday))
        for j in range(3):
            self.CE_SV[j+1].set('{: .11e}'.format(pos[j]))
            self.CE_SV[j+4].set('{: .11e}'.format(vel[j]))
        
    def toClassical(self):
        cartesian = []
        for j in range(7):
            cartesian.append(float(self.CE_SV[j].get()))
        cartesian[0] *= secofday    # convert to seconds
        try:
            orbit.setOrbCart(cartesian[0], cartesian[1:4], cartesian[4:7])
        except ValueError as ve:
            self.cError['text'] = ve.args[0]
            return
        
        self.cError['text'] = ' '
        kepl = orbit.elmKepl()      # pos, vel at epoch
        self.KE_SV[0].set('{: .6f}'.format(kepl['epoch'] / secofday))
        self.KE_SV[1].set('{: .11e}'.format(kepl['a']))
        self.KE_SV[2].set('{: .10f}'.format(kepl['e']))
        self.KE_SV[3].set('{: 12.9f}'.format(kepl['i']))
        self.KE_SV[4].set('{: 12.9f}'.format(kepl['LoAN']))
        self.KE_SV[5].set('{: 12.9f}'.format(kepl['AoP']))
        self.KE_SV[6].set('{: 12.9f}'.format(kepl['TA']))
        if kepl['T'] is not None:
            self.KE_SV[7].set('{: .6f}'.format(kepl['T'] / secofday))
        else:
            self.KE_SV[7].set('None')
        if kepl['MA'] is not None:
            self.KE_SV[8].set('{: .6f}'.format(kepl['MA']))
        else:
            self.KE_SV[8].set('None')
        
    def drawCartesian(self):
        # Erase mark and line
        if self.arsc is not None:
            self.arsc.remove()
            for j in range(3):
                self.arname[j].remove()
            self.arsc = None
        if self.arline is not None:
            self.arline[0].remove()
            self.arline = None

        cartesian = []
        for j in range(7):
            cartesian.append(float(self.CE_SV[j].get()))
        cartesian[0] *= secofday    # convert to seconds
        try:
            orbit.setOrbCart(cartesian[0], cartesian[1:4], cartesian[4:7])
        except ValueError as ve:
            self.dError['text'] = ve.args[0]
            return
        self.dError['text'] = ' '
        
        t = float(self.Ct_SV.get()) * secofday
        self.draw(cartesian[0], t)
    
    def drawClassical(self):
        # Erase mark and line
        if self.arsc is not None:
            self.arsc.remove()
            for j in range(3):
                self.arname[j].remove()
            self.arsc = None
        if self.arline is not None:
            self.arline[0].remove()
            self.arline = None

        classical = []
        for j in range(6):
            classical.append(float(self.KE_SV[j].get()))
        classical[0] *= secofday    # convert to seconds
        
        if self.radio.get() == 6:
            ta = float(self.KE_SV[6].get())
            try:
                orbit.setOrbKepl(*classical[0:6], TA=ta)
            except ValueError as ve:
                self.dError['text'] = ve.args[0]
                return
        elif self.radio.get() ==7:
            t = float(self.KE_SV[7].get()) * secofday
            try:
                orbit.setOrbKepl(*classical[0:6], T=t)
            except ValueError as ve:
                self.dError['text'] = ve.args[0]
                return
        else:
            ma = float(self.KE_SV[8].get())
            try:
                orbit.setOrbKepl(*classical[0:6], MA=ma)
            except ValueError as ve:
                self.dError['text'] = ve.args[0]
                return
        self.dError['text'] = ' '
        
        t = float(self.Kt_SV.get()) * secofday
        self.draw(classical[0], t)

    def draw(self, epoch, t):
        try:
            # Position at Epoch
            pos1, vel1 = orbit.posvelatt(epoch)
            # Position at t
            pos2, vel2 = orbit.posvelatt(t)
        except RuntimeError as re:
            self.dError['text'] = re.args[0]
            return
        self.dError['text'] = ' '
        
        ps = np.array([pos1, pos2, np.zeros(3)]).T
        
        # Draw marks
        self.arsc = ax.scatter(ps[0], ps[1], ps[2], marker='+', color='b')
        for j in range(3):
            self.arname[j] = ax.text(ps[0, j], ps[1, j], ps[2, j], 
                             self.object[j], color='b', fontsize=9)

        # Get points on orbit
        x, y, z, t = orbit.points(1001)
        
        # Draw an orbital line
        self.arline = ax.plot(x, y, z, color='r', lw=0.75)
        plt.draw()

if __name__ == '__main__':
    mw =tkinter.Tk()
    mw.title("Demonstrate pytwobodyorbit")
    mw.geometry('630x780+10+10')
    app = TestConvert(master=mw)
    app.mainloop()
