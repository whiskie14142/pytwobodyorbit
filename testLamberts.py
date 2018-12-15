# -*- coding: utf-8 -*-
"""Main program to test and demonstrate pytwobodyorbit
Created on Fri Dec 14 08:44:47 2018

@author: Shushi Uetsuki/whiskie14142
"""

import numpy as np
import math
import tkinter
from pytwobodyorbit import TwoBodyOrbit
from pytwobodyorbit import solveGauss
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib

# Standard gravitational parameter for the Sun (Sol)
# With this parameter, lenght should be in meters,
# and time should be in seconds
mu = 1.32712440041e20

# Create instance of TwoBodyOrbit
orbit = TwoBodyOrbit('object')

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
        self.Lspace0 = tkinter.Label(self, text=' ')
        self.Lspace0.grid(row=0, column=0)

        self.comment = tkinter.Text(self, width=80, height=16, wrap=tkinter.WORD)
        self.comment.insert(1.0, 'Hello\n World World World World World World World World World World nWorld World World World World World World World World World')
#        self.comment['text'] = 'Hello\n World World World World World World World World World World \nWorld World World World World World World World World World'
        self.comment['state'] = tkinter.DISABLED
        self.comment.grid(row=1, column=0, columnspan=3)
        
        self.Lspace = tkinter.Label(self, text=' ')
        self.Lspace.grid(row=2, column=0)
        
        self.L1_X = tkinter.Label(self, text='Pos1_X: ')
        self.L1_X.grid(row=3, column=0)
        self.pos1_X = tkinter.StringVar(value='1.500000e11')
        self.Epos1_X = tkinter.Entry(self, bd=1, textvariable=self.pos1_X)
        self.Epos1_X.grid(row=3, column=1)
        
        self.L1_Y = tkinter.Label(self, text='Pos1_Y: ')
        self.L1_Y.grid(row=4, column=0)
        self.pos1_Y = tkinter.StringVar(value='0.000000e11')
        self.Epos1_Y = tkinter.Entry(self, bd=1, textvariable=self.pos1_Y)
        self.Epos1_Y.grid(row=4, column=1)
        
        self.L1_Z = tkinter.Label(self, text='Pos1_Z: ')
        self.L1_Z.grid(row=5, column=0)
        self.pos1_Z = tkinter.StringVar(value='0.000000e11')
        self.Epos1_Z = tkinter.Entry(self, bd=1, textvariable=self.pos1_Z)
        self.Epos1_Z.grid(row=5, column=1)
        
        self.Lspace2 = tkinter.Label(self, text=' ')
        self.Lspace2.grid(row=6, column=0)
        
        self.L2_X = tkinter.Label(self, text='Pos2_X: ')
        self.L2_X.grid(row=7, column=0)
        self.pos2_X = tkinter.StringVar(value='0.000000e11')
        self.Epos2_X = tkinter.Entry(self, bd=1, textvariable=self.pos2_X)
        self.Epos2_X.grid(row=7, column=1)
        self.L2_Y = tkinter.Label(self, text='Pos2_Y: ')
        self.L2_Y.grid(row=8, column=0)
        self.pos2_Y = tkinter.StringVar(value='1.300000e11')
        self.Epos2_Y = tkinter.Entry(self, bd=1, textvariable=self.pos2_Y)
        self.Epos2_Y.grid(row=8, column=1)
        self.L2_Z = tkinter.Label(self, text='Pos2_Z: ')
        self.L2_Z.grid(row=9, column=0)
        self.pos2_Z = tkinter.StringVar(value='0.200000e11')
        self.Epos2_Z = tkinter.Entry(self, bd=1, textvariable=self.pos2_Z)
        self.Epos2_Z.grid(row=9, column=1)
        
        self.Lspace3 = tkinter.Label(self, text=' ')
        self.Lspace3.grid(row=10, column=0)
        
        self.Ltime = tkinter.Label(self, text='Flight Time (days):')
        self.Ltime.grid(row=11, column=0)
        self.ftime = tkinter.StringVar(value='300.0')
        self.Eftime = tkinter.Entry(self, bd=1, textvariable=self.ftime)
        self.Eftime.grid(row=11, column=1)

        self.Lspace4 = tkinter.Label(self, text=' ')
        self.Lspace4.grid(row=12, column=0)
        
        self.solve_Lam = tkinter.Button(self)
        self.solve_Lam['text'] = 'Compute and Draw'
        self.solve_Lam['command'] = self.compute
        self.solve_Lam.grid(row=13, column=1)
        
        self.quitapp = tkinter.Button(self)
        self.quitapp['text'] = 'Quit'
        self.quitapp['command'] = self.master.destroy
        self.quitapp.grid(row=14, column=2)
        
        self.compute()
        

    def compute(self):
        pos1 = np.array([float(self.pos1_X.get()), float(self.pos1_Y.get()),
                         float(self.pos1_Z.get())])
        pos2 = np.array([float(self.pos2_X.get()), float(self.pos2_Y.get()),
                         float(self.pos2_Z.get())])
        ps = np.array([pos1, pos2, [0.0, 0.0, 0.0]]).T
        
        if self.arsc is not None:
            self.arsc.remove()
        self.arsc = ax.scatter(ps[0], ps[1], ps[2], marker='x', color='b')
        
        duration = float(self.ftime.get()) * 86400.0
        try:
            # Compute initial and terminal velocity with solveGauss.
            # You may try ccw=False.
            ivel, tvel = solveGauss(pos1, pos2, duration, mu, 
                                ccw=True    # ***  Flag for flight direction
                                    )
        except ValueError:
            print('solveGauss could not compute initial/terminal velocity')
            return

        print('  ivel=', ivel)
        print('  tvel=', tvel)

        # Define orbit by epoch, position, and velocity
        orbit.setOrbCart(0.0, pos1, ivel)
        
        # Get Keplerian orbital elements
        kepl = orbit.elmKepl()
        for ix in kepl:
            print(' ', ix, '=', kepl[ix])
            
        # Get points on orbit
        x, y, z, t = orbit.points(1001)
        
        # Plot an orbital line
        if self.arline is not None:
            self.arline[0].remove()
        self.arline = ax.plot(x, y, z, color='r', lw=0.75)
        plt.draw()
        
        # Get predicted position and velocity at the terminal position
        predpos, predvel = orbit.posvelatt(duration)
        
        # Compare position and velocity at terminal point for checking
        print('  delta pos=', pos2 - predpos)
        print('  delta vel=', tvel - predvel)

def main():
    """Main program for test and demonstration for solveGauss() of pytwobodyorbit
    
    Run this module as main program, and try 100, 300, 60 for 
    'Flight Duration' at first.  You may try other values also.
    Additionally, you may change parameters in lines commented with '***'
    
    On the plotting window, you can rotate the image (left-button dragging),
    and zoom (right-button dragging-up and dragging-down)
    """
    
    # prepare main window

    
    # You may change following parameters. These lines prepare two points of
    # Gauss problem. Each value should be in meters.
    pos1 = np.array([
                        150000000000.0,     # ***  X of initial point
                        0.0,                # ***  Y of initial point 
                        0.0                 # ***  Z of initial point
                    ])
    pos2 = np.array([
                        0.0,                # ***  X of terminal point
                        130000000000.0,     # ***  Y of terminal point
                        20000000000.0       # ***  Z of terminal point
                    ])
    
    # Plot pos1, pos2, and center position
    ps = np.array([pos1, pos2, [0.0, 0.0, 0.0]]).T
    ax.scatter(ps[0], ps[1], ps[2], marker='x', color='b')
    
    duration = float(self.ftime)


    while True:
        print()
        ans = input('Flight Duration (days) or Q ? ')
        if ans.upper() == 'Q':
            break
    
        if ar != None:
            ar[0].remove()
            ar = None
            
        duration = float(ans) * 86400.0
        try:
            # Compute initial and terminal velocity with solveGauss.
            # You may try ccw=False.
            ivel, tvel = solveGauss(pos1, pos2, duration, mu, 
                                ccw=True    # ***  Flag for flight direction
                                    )
        except ValueError:
            print('solveGauss could not compute initial/terminal velocity')
            continue
        print('  ivel=', ivel)
        print('  tvel=', tvel)
        
        # Define orbit by epoch, position, and velocity
        orbit.setOrbCart(0.0, pos1, ivel)
        
        # Get Keplerian orbital elements
        kepl = orbit.elmKepl()
        for ix in kepl:
            print(' ', ix, '=', kepl[ix])
            
        # Get points on orbit
        x, y, z, t = orbit.points(1001)
        
        # Plot an orbital line
        ar = ax.plot(x, y, z, color='r')
        plt.draw()
        
        # Get predicted position and velocity at the terminal position
        predpos, predvel = orbit.posvelatt(duration)
        
        # Compare position and velocity at terminal point for checking
        print('  delta pos=', pos2 - predpos)
        print('  delta vel=', tvel - predvel)

    
if __name__ == '__main__':
    mw =tkinter.Tk()
    mw.title('solveGauss() test for pytwobodyorbit')
    mw.geometry('600x800+10+10')
    app = TestLamberts(master=mw)
    app.mainloop()
