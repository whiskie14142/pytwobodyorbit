# -*- coding: utf-8 -*-
"""Testing and demonstrating program for 'solveGauss' of pytwobodyorbit
Created on Fri Dec 14 08:44:47 2018

@author: Shushi Uetsuki/whiskie14142
"""

import numpy as np
import tkinter
from pytwobodyorbit import TwoBodyOrbit
from pytwobodyorbit import solveGauss
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


class TestLamberts(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.arline = None
        self.arsc = None

        self.create_widgets()
        
    def create_widgets(self):
        self.Lspace0 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace0.grid(row=0, column=0)

        self.comment = tkinter.Text(self, width=80, height=17, wrap=tkinter.WORD)
        scom = """This program demonstrates 'solveGauss' function of the module pytwobodyorbit.

The 'solveGauss' function solves so-called 'Lambert's Probrem', computes a two-
body orbit of an object, from its initiating position, terminating position,
and flight time; it yields initial velocity and terminal velocity of the object.

In this program, we use the Sun as the central body; resulting orbit is
prograde; the unit of length is meters, and the unit of time is seconds.

Edit coordinates of initiating position and terminating position, and flight
time.  Then click [Compute and Draw] button.  Note that you specify the flight
time in days, and this program converts it into seconds internally.

This program shows you initial velocity and terminal velocity of the object.
In addition, it shows you the orbit in a 3-D chart, Classical orbital elements,
and Residuals of terminating position and velocity."""

        self.comment.insert(1.0, scom)
        self.comment['state'] = tkinter.DISABLED
        self.comment.grid(row=1, column=0, columnspan=3)
        
        self.Lspace = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace.grid(row=2, column=0)
        
        self.L1_X = tkinter.Label(self, text='Initiating Position: Pos1_X  ')
        self.L1_X.grid(row=3, column=0, sticky=tkinter.E)
        self.pos1_X = tkinter.StringVar(value='1.500000e11')
        self.Epos1_X = tkinter.Entry(self, bd=1, textvariable=self.pos1_X)
        self.Epos1_X.grid(row=3, column=1, sticky=tkinter.W)
        
        self.L1_Y = tkinter.Label(self, text='Initiating Position: Pos1_Y  ')
        self.L1_Y.grid(row=4, column=0, sticky=tkinter.E)
        self.pos1_Y = tkinter.StringVar(value='0.000000e11')
        self.Epos1_Y = tkinter.Entry(self, bd=1, textvariable=self.pos1_Y)
        self.Epos1_Y.grid(row=4, column=1, sticky=tkinter.W)
        
        self.L1_Z = tkinter.Label(self, text='Initiating Position: Pos1_Z  ')
        self.L1_Z.grid(row=5, column=0, sticky=tkinter.E)
        self.pos1_Z = tkinter.StringVar(value='0.000000e11')
        self.Epos1_Z = tkinter.Entry(self, bd=1, textvariable=self.pos1_Z)
        self.Epos1_Z.grid(row=5, column=1, sticky=tkinter.W)
        
        self.Lspace2 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace2.grid(row=6, column=0)
        
        self.L2_X = tkinter.Label(self, text='Terminating Position: Pos2_X  ')
        self.L2_X.grid(row=7, column=0, sticky=tkinter.E)
        self.pos2_X = tkinter.StringVar(value='-0.500000e11')
        self.Epos2_X = tkinter.Entry(self, bd=1, textvariable=self.pos2_X)
        self.Epos2_X.grid(row=7, column=1, sticky=tkinter.W)
        self.L2_Y = tkinter.Label(self, text='Terminating Position: Pos2_Y  ')
        self.L2_Y.grid(row=8, column=0, sticky=tkinter.E)
        self.pos2_Y = tkinter.StringVar(value='1.300000e11')
        self.Epos2_Y = tkinter.Entry(self, bd=1, textvariable=self.pos2_Y)
        self.Epos2_Y.grid(row=8, column=1, sticky=tkinter.W)
        self.L2_Z = tkinter.Label(self, text='Terminating Position: Pos2_Z  ')
        self.L2_Z.grid(row=9, column=0, sticky=tkinter.E)
        self.pos2_Z = tkinter.StringVar(value='0.400000e11')
        self.Epos2_Z = tkinter.Entry(self, bd=1, textvariable=self.pos2_Z)
        self.Epos2_Z.grid(row=9, column=1, sticky=tkinter.W)
        
        self.Lspace3 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace3.grid(row=10, column=0)
        
        self.Ltime = tkinter.Label(self, text='Flight Time (days)  ')
        self.Ltime.grid(row=11, column=0, sticky=tkinter.E)
        self.ftime = tkinter.StringVar(value='100.0')
        self.Eftime = tkinter.Entry(self, bd=1, textvariable=self.ftime)
        self.Eftime.grid(row=11, column=1, sticky=tkinter.W)

        self.Lspace4 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace4.grid(row=12, column=0)
        
        self.solve_Lam = tkinter.Button(self)
        self.solve_Lam['text'] = 'Compute and Draw'
        self.solve_Lam['command'] = self.compute
        self.solve_Lam.grid(row=13, column=1, sticky=tkinter.W)
        
        self.Lspace5 = tkinter.Label(self, text=' ', font=('Arial',9,'bold'))
        self.Lspace5.grid(row=14, column=0, columnspan=3)

        self.Lspace6 = tkinter.Label(self, text=' ', font=('Times', 4))
        self.Lspace6.grid(row=29, column=0)
        
        self.quitapp = tkinter.Button(self)
        self.quitapp['text'] = 'Quit'
        self.quitapp['command'] = self.master.destroy
        self.quitapp.grid(row=30, column=2)
        
        self.compute()
        

    def compute(self):
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
        self.arsc = ax.scatter(ps[0], ps[1], ps[2], marker='x', color='b')
        
        # Get flight time (days) and convert into seconds
        duration = float(self.ftime.get()) * secofday
        self.Lspace5['text'] = ' '
        try:
            # Compute initial and terminal velocity with solveGauss.
            # You may try ccw=False.
            ivel, tvel = solveGauss(pos1, pos2, duration, mu, 
                                ccw=True    # Indicates prograde orbit
                                    )
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
        
        # Get Classical orbital elements
        kepl = orbit.elmKepl()
        skepl = 'Classical Orbital Elements'
        for ix in kepl:
            skepl = skepl + '\n    ' + ix + ' = ' + str(kepl[ix]) + '                                '
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
    mw.title("Demonstrate 'solveGauss' function of pytwobodyorbit")
    mw.geometry('600x800+10+10')
    app = TestLamberts(master=mw)
    app.mainloop()
