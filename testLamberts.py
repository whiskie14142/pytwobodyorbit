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

ar = None



class TestLamberts(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        self.comment = tkinter.Text(self, width=80, wrap=tkinter.WORD)
        self.comment.insert(1.0, 'Hello\n World World World World World World World World World World nWorld World World World World World World World World World')
#        self.comment['text'] = 'Hello\n World World World World World World World World World World \nWorld World World World World World World World World World'
        self.comment['state'] = tkinter.DISABLED
        self.comment.pack()
        
        self.Lspace = tkinter.Label(self, text=' ')
        self.Lspace.pack()
        self.L1_X = tkinter.Label(self, text='Pos1_X: ')
        self.L1_X.pack(side=tkinter.LEFT)
        self.pos1_X = tkinter.StringVar(value='1.500000e11')
        self.Epos1_X = tkinter.Entry(self, bd=1, textvariable=self.pos1_X)
        self.Epos1_X.pack(side=tkinter.LEFT)

    def set_pos1():
        pass
    
    def set_pos2():
        pass
    
    def set_flighttime():
        pass
    
    def print_Kepler():
        pass
    
    def draworbit():
        pass


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
