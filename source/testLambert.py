# -*- coding: utf-8 -*-
"""Testing and demonstrating program for 'solveGauss' of pytwobodyorbit
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
mngr.window.setGeometry(660, 40, 600, 600)


class TestLambert(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.arline = None
        self.arsc = None
        self.object = ['  P1', '  P2', '  Sun']
        self.arname = [None, None, None]

        self.create_widgets()
        
    def create_widgets(self):
        self.Lspace0 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace0.grid(row=0, column=0)

        self.comment = tkinter.Text(self, width=80, height=19, 
                        font=('Helvetica', 10), wrap=tkinter.WORD)
        scom = "This program demonstrates 'lambert' function of the module 'pytwobodyorbit'.\n\n" + \
            "The 'lambert' function solves so-called 'Lambert's Probrem'.  It computes a two-body orbit of an object from its initial position (P1), terminal position (P2), and flight time from P1 to P2; it yields initial velocity and terminal velocity of the object.\n\n" + \
            "In this program, we use the Sun as the central body.  The program shows initial velocity and terminal velocity of the object. It shows classical orbital elements, and residuals of terminating position and velocity.  In addition, it shows the orbit in the 3D chart.\n\n" + \
            "USAGE:\nEdit coordinates of P1 and P2, and flight time, and click [Compute Prograde Orb] button for direct (prograde) orbit, or [Compute Retrograde Orb] for retrograde orbit.\n\n" + \
            "UNITS:\nLength - meters\nVelocity - meters per second\nTime - days"

        self.comment.insert(1.0, scom)
        self.comment['state'] = tkinter.DISABLED
        self.comment.grid(row=1, column=0, columnspan=3)
        
        self.Lspace = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace.grid(row=2, column=0)
        
        self.L1_X = tkinter.Label(self, text='Initial Position: P1(X)  ')
        self.L1_X.grid(row=3, column=0, sticky=tkinter.E)
        self.pos1_X = tkinter.StringVar(value=' 1.50000000000e+11')
        self.Epos1_X = tkinter.Entry(self, bd=1, textvariable=self.pos1_X)
        self.Epos1_X.grid(row=3, column=1, sticky=tkinter.W)
        
        self.L1_Y = tkinter.Label(self, text='Initial Position: P1(Y)  ')
        self.L1_Y.grid(row=4, column=0, sticky=tkinter.E)
        self.pos1_Y = tkinter.StringVar(value=' 0.00000000000e+11')
        self.Epos1_Y = tkinter.Entry(self, bd=1, textvariable=self.pos1_Y)
        self.Epos1_Y.grid(row=4, column=1, sticky=tkinter.W)
        
        self.L1_Z = tkinter.Label(self, text='Initial Position: P1(Z)  ')
        self.L1_Z.grid(row=5, column=0, sticky=tkinter.E)
        self.pos1_Z = tkinter.StringVar(value=' 0.00000000000e+11')
        self.Epos1_Z = tkinter.Entry(self, bd=1, textvariable=self.pos1_Z)
        self.Epos1_Z.grid(row=5, column=1, sticky=tkinter.W)
        
        self.Lspace2 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace2.grid(row=6, column=0)
        
        self.L2_X = tkinter.Label(self, text='Terminal Position: P2(X)  ')
        self.L2_X.grid(row=7, column=0, sticky=tkinter.E)
        self.pos2_X = tkinter.StringVar(value='-0.50000000000e+11')
        self.Epos2_X = tkinter.Entry(self, bd=1, textvariable=self.pos2_X)
        self.Epos2_X.grid(row=7, column=1, sticky=tkinter.W)
        self.L2_Y = tkinter.Label(self, text='Terminal Position: P2(Y)  ')
        self.L2_Y.grid(row=8, column=0, sticky=tkinter.E)
        self.pos2_Y = tkinter.StringVar(value=' 1.30000000000e+11')
        self.Epos2_Y = tkinter.Entry(self, bd=1, textvariable=self.pos2_Y)
        self.Epos2_Y.grid(row=8, column=1, sticky=tkinter.W)
        self.L2_Z = tkinter.Label(self, text='Terminal Position: P2(Z)  ')
        self.L2_Z.grid(row=9, column=0, sticky=tkinter.E)
        self.pos2_Z = tkinter.StringVar(value=' 0.40000000000e+11')
        self.Epos2_Z = tkinter.Entry(self, bd=1, textvariable=self.pos2_Z)
        self.Epos2_Z.grid(row=9, column=1, sticky=tkinter.W)
        
        self.Lspace3 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace3.grid(row=10, column=0)
        
        self.Ltime = tkinter.Label(self, text='Flight Time (days)  ')
        self.Ltime.grid(row=11, column=0, sticky=tkinter.E)
        self.ftime = tkinter.StringVar(value=' 100.0')
        self.Eftime = tkinter.Entry(self, bd=1, textvariable=self.ftime)
        self.Eftime.grid(row=11, column=1, sticky=tkinter.W)

        self.Lspace4 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace4.grid(row=12, column=0)
        
        self.solve_Lam_p = tkinter.Button(self)
        self.solve_Lam_p['text'] = ' Compute Prograde Orb '
        self.solve_Lam_p['command'] = self.prograde
        self.solve_Lam_p.grid(row=13, column=1, sticky=tkinter.W)
        
        self.solve_Lam_r = tkinter.Button(self)
        self.solve_Lam_r['text'] = ' Compute Retrograde Orb '
        self.solve_Lam_r['command'] = self.retrograde
        self.solve_Lam_r.grid(row=13, column=2, sticky=tkinter.W)
        
        self.Lspace5 = tkinter.Label(self, text=' ', font=('Arial',9,'bold'))
        self.Lspace5.grid(row=14, column=0, columnspan=3)

        self.Lspace6 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace6.grid(row=29, column=0)
        
        self.quitapp = tkinter.Button(self)
        self.quitapp['text'] = '    Quit    '
        self.quitapp['command'] = self.master.destroy
        self.quitapp.grid(row=30, column=2, sticky=tkinter.E)
        
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
                         
        ps = np.array([pos1, pos2, np.zeros(3)]).T
        
        if self.arsc is not None:
            self.arsc.remove()
            self.arsc = None
            for j in range(3):
                self.arname[j].remove()
                
        self.arsc = ax.scatter(ps[0], ps[1], ps[2], marker='+', color='b')
        for j in range(3):
            self.arname[j] = ax.text(ps[0, j], ps[1, j], ps[2, j], 
                             self.object[j], color='b', fontsize=9)

        if self.arline is not None:
            self.arline[0].remove()
            self.arline = None
        
        # Get flight time (days) and convert into seconds
        duration = float(self.ftime.get()) * secofday
        self.Lspace5['text'] = ' '
        try:
            # Compute initial and terminal velocity with solveGauss.
            # You may try ccw=False.
            ivel, tvel = lambert(pos1, pos2, duration, mu, ccw=prog)
        except ValueError as ve:
            self.Lspace5['text'] = ve.args[0]
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
        skepl = 'Classical Orbital Elements' + \
            '\n    epoch = ' + '{:.6f}'.format(kepl['epoch'] / secofday) + \
            '\n    a = ' + '{:.11e}'.format(kepl['a']) + \
            '\n    e = ' + '{:.11f}'.format(kepl['e']) + \
            '\n    i = ' + '{:12.9f}'.format(kepl['i']) + \
            '\n    LoAN = ' + '{:12.9f}'.format(kepl['LoAN']) + \
            '\n    AoP = ' + '{:12.9f}'.format(kepl['AoP']) + \
            '\n    TA = ' + '{:12.9f}'.format(kepl['TA']) + \
            '\n    T = ' + '{:12.9f}'.format(kepl['T'] / secofday)
        if kepl['MA'] is None:
            skepl = skepl + '\n    MA = None' 
        else:
            skepl = skepl + '\n    MA = ' + '{:12.9f}'.format(kepl['MA'])
        if kepl['n'] is None:
            skepl = skepl + '\n    n = None'
        else:
            skepl = skepl + '\n    n = ' + '{:12.9f}'.format(kepl['n'] * secofday)
        if kepl['P'] is None:
            skepl = skepl + '\n    P = None'
        else:
            skepl = skepl + '\n    P = ' + '{:12.9f}'.format(kepl['P'] / secofday)
        skepl = skepl + '                                '
        self.Lkepl = tkinter.Label(self, text=skepl, justify=tkinter.LEFT, anchor=tkinter.NW, height=12)
        self.Lkepl.grid(row=17, column=0, columnspan=3, sticky=tkinter.W)
        
        # Get points on orbit
        x, y, z, t = orbit.points(1001)
        
        # Plot an orbital line
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
    mw.title("Demonstrate 'lambert' function of pytwobodyorbit")
    mw.geometry('620x880+10+10')
    app = TestLambert(master=mw)
    app.mainloop()
