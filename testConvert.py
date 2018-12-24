# -*- coding: utf-8 -*-
"""Testing and demonstrating program for pytwobodyorbit
Created on Fri Dec 14 08:44:47 2018

@author: Shushi Uetsuki/whiskie14142
"""

import numpy as np
import tkinter
from pytwobodyorbit import TwoBodyOrbit
from pytwobodyorbit import lambert
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib

# Standard gravitational parameter for the Sun
# With this parameter, lenght should be in meters,
# and time should be in seconds
mu = 1.32712440041e20

# Create instance of TwoBodyOrbit
orbit = TwoBodyOrbit('object')

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
mngr.window.setGeometry(640, 50, 600, 600)


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

        self.comment = tkinter.Text(self, width=80, height=19, wrap=tkinter.WORD)
        scom = """This program demonstrates the module 'pytwobodyorbit'.

The 'lambert' function solves so-called 'Lambert's Probrem'.  It computes a 
two-body orbit of an object from its initial position (P1), terminal position 
(P2), and flight time from P1 to P2; it yields initial velocity and terminal 
velocity of the object.

In this program, we use the Sun as the central body; the unit of length is 
meters, and the unit of time is days for input/output.  
Note that unit of a velocity is meters per second.

USAGE:
Edit coordinates of P1 and P2, and flight time, and click [Compute Pro. Orb] 
button for prograde orbit, or [Compute Retro. Orb] for retrograde orbit.

This program shows initial velocity and terminal velocity of the object. It 
shows classical orbital elements, and residuals of terminating position and 
velocity.  In addition, it shows the orbit in the 3D chart.
"""

        self.comment.insert(1.0, scom)
        self.comment['state'] = tkinter.DISABLED
        self.comment.grid(row=1, column=0, columnspan=5)
        
        self.Lspace = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace.grid(row=2, column=0)
        
        self.Ltitle1 = tkinter.Label(self, text='Classical Orbital Elements')
        self.Ltitle1.grid(row=3, column=0, columnspan=2)
        
        self.KE_d = [
                'Epoch  ',
                'Semi-major axis (a)  ',
                'Eccentricity (e)  ',
                'Inclination (i)  ',
                'Longitude of AN (LoAN)  ',
                'Argument of P (AoP)  '
                'True anomaly (TA)  ',
                'Periapsis psg (T)  ',
                'Mean anomaly (MA)  ']
        self.KE_v = [
                '0.000000',
                '1.500000e11',
                '0.200000',
                '15.000000',
                '60.000000',
                '135.000000',
                '70.000000',
                'None',
                'None']
        self.KE_L = []
        self.KE_SV = []
        self.KE_E = []
        
        for j in range(7):
            self.KE_L.append(tkinter.Label(self, text=self.KE_d[j]))
            self.KE_L[j].grid(row=j+4, column=0, sticky=tkinter.E)
            self.KE_SV.append(tkinter.StringVar(value=self.KE_v[j]))
            self.KE_E.append(tkinter.Entry(self, bd=1, textvariable=self.KE_SV[j]))
            self.KE_E[j].grid(row=j+4, column=1, sticky=tkinter.W)

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
                '0.000000',
                '1.000000e11',
                '1.200000e11',
                '0.200000e11',
                '-20000.00',
                '18000.00',
                '0.000000']

        self.CE_L = []
        self.CE_SV = []
        self.CE_E = []

        for j in range(7):
            self.CE_L.append(tkinter.Label(self, text=self.CE_d[j]))
            self.CE_L[j].grid(row=j+4, column=3, sticky=tkinter.W)
            self.CE_SV.append(tkinter.StringVar(value=self.CE_v[j]))
            self.CE_E.append(tkinter.Entry(self, bd=1, textvariable=self.CE_SV[j]))
            self.CE_E[j].grid(row=j+4, column=4, sticky=tkinter.E)

        self.Lspace3 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace3.grid(row=15, column=0)




        
        
        

        self.Lspace4 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace4.grid(row=12, column=0)
        
        self.solve_Lam_p = tkinter.Button(self)
        self.solve_Lam_p['text'] = ' Compute Pro. Orb. '
        self.solve_Lam_p['command'] = self.prograde
        self.solve_Lam_p.grid(row=13, column=1, sticky=tkinter.W)
        
        self.solve_Lam_r = tkinter.Button(self)
        self.solve_Lam_r['text'] = ' Compute Retro. Orb. '
        self.solve_Lam_r['command'] = self.retrograde
        self.solve_Lam_r.grid(row=13, column=2, sticky=tkinter.W)
        
        self.Lspace5 = tkinter.Label(self, text=' ', font=('Arial',9,'bold'))
        self.Lspace5.grid(row=14, column=0, columnspan=3)

        self.Lspace6 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace6.grid(row=29, column=0)
        
        self.quitapp = tkinter.Button(self)
        self.quitapp['text'] = '    Quit    '
        self.quitapp['command'] = self.master.destroy
        self.quitapp.grid(row=30, column=2)
        
    def prograde(self):
        self.compute(prog=True)
        
    def retrograde(self):
        self.compute(prog=False)
        

    def compute(self, prog=True):
        # Clicking of the button [Compute and Draw] runs this method
        
        # Get initiating position
        pos1 = np.array([float(self.pos1_X.get()), float(self.pos1_Y.get()),
                         float(self.pos1_Z.get())])
                         
        # Get terminating position
        pos2 = np.array([float(self.pos2_X.get()), float(self.pos2_Y.get()),
                         float(self.pos2_Z.get())])
                         
        ps = np.array([pos1, pos2, [0.0, 0.0, 0.0]]).T
        
        if self.arsc is not None:
            self.arsc.remove()
            for j in range(3):
                self.arname[j].remove()
                
        self.arsc = ax.scatter(ps[0], ps[1], ps[2], marker='+', color='b')
        for j in range(3):
            self.arname[j] = ax.text(ps[0, j], ps[1, j], ps[2, j], 
                             self.object[j], color='b', fontsize=9)
        
        # Get flight time (days) and convert into seconds
        duration = float(self.ftime.get()) * secofday
        self.Lspace5['text'] = ' '
        try:
            # Compute initial and terminal velocity with solveGauss.
            # You may try ccw=False.
            ivel, tvel = lambert(pos1, pos2, duration, mu, ccw=prog)
        except ValueError:
            self.Lspace5['text'] = 'solveGauss() could not compute initial/terminal velocity. Try different parameters.'
            return

        
        sivel = 'Initial Velocity (meters per second) = ' + str(ivel)
        self.Livel = tkinter.Label(self, text=sivel, width=80, anchor=tkinter.W)
        self.Livel.grid(row=15, column=0, columnspan=3, sticky=tkinter.W)
        stvel = 'Terminate Velocity (meters per second) = ' +str(tvel)
        self.Ltvel = tkinter.Label(self, text=stvel, width=80, anchor=tkinter.W)
        self.Ltvel.grid(row=16, column=0, columnspan=3, sticky=tkinter.W)

        # Define orbit from epoch, initiating position, and initial velocity
        orbit.setOrbCart(0.0, pos1, ivel)
        
        # Get Classical orbital elements and show them
        # Convert unit of time to seconds
        kepl = orbit.elmKepl()
        skepl = 'Classical Orbital Elements'
        for ix in kepl:
            skepl = skepl + '\n    ' + ix + ' = '
            if ix == 'T' or ix == 'P':
                if kepl[ix] is None:
                    skepl = skepl + 'None'
                else:
                    skepl = skepl + str(kepl[ix] / secofday) 
            elif ix == 'MA':
                if kepl[ix] is None:
                    skepl = skepl + 'None'
                else:
                    skepl = skepl + str(kepl[ix]) 
            elif ix == 'n':
                if kepl[ix] is None:
                    skepl = skepl + 'None'
                else:
                    skepl = skepl + str(kepl[ix] * secofday) 
            else:
                skepl = skepl + str(kepl[ix])
            skepl = skepl + '                                '
        self.Lkepl = tkinter.Label(self, text=skepl, justify=tkinter.LEFT, anchor=tkinter.NW, height=12)
        self.Lkepl.grid(row=17, column=0, columnspan=3, sticky=tkinter.W)
        
        # Get points on orbit
        x, y, z, t = orbit.points(1001)
        
        # Plot an orbital line
        if self.arline is not None:
            self.arline[0].remove()
        self.arline = ax.plot(x, y, z, color='r', lw=0.75)
        plt.draw()
        
        # Get predicted position and velocity at the end of the flight
        predpos, predvel = orbit.posvelatt(duration)
        
        # Compute residuals of positions and velocities at the terminating point
        sdpos = 'Residuals in position (meters) = ' + str(pos2 - predpos)
        self.Ldpos = tkinter.Label(self, text=sdpos, width=80, anchor=tkinter.W)
        self.Ldpos.grid(row=19, column=0, columnspan=3, sticky=tkinter.W)
        sdvel = 'Residuals in velocity (meters per second) = ' + str(tvel - predvel)
        self.Ldvel = tkinter.Label(self, text=sdvel, width=80, anchor=tkinter.W)
        self.Ldvel.grid(row=20, column=0, columnspan=3, sticky=tkinter.W)

    
if __name__ == '__main__':
    mw =tkinter.Tk()
    mw.title("Demonstrate pytwobodyorbit")
    mw.geometry('600x830+10+10')
    app = TestConvert(master=mw)
    app.mainloop()
