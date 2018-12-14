# -*- coding: utf-8 -*-
"""Main program to test and demonstrate pytwobodyorbit
Created on Fri Dec 14 08:44:47 2018

@author: Shushi Uetsuki/whiskie14142
"""

import numpy as np
import math
import tkinter
import pytwobodyorbit as ptbo
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def set_pos1():
    pass

def set_pos2():
    pass

def set_flighttime():
    pass

def print_Kepler():
    pass




def main():
    """Main program for test and demonstration
    
    Run this module as main program, and try 100, 300, 60 for 
    'Flight Duration' at first.  You may try other values also.
    Additionally, you may change parameters in lines commented with '***'
    
    On the plotting window, you can rotate the image (left-button dragging),
    and zoom (right-button dragging-up and dragging-down)
    """
    
    # Standard gravitational parameter for the Sun (Sol)
    # With this parameter, lenght should be in meters,
    # and time should be in seconds
    mu = 1.32712440041e20
    
    # Create instance of TwoBodyOrbit
    orbit = TwoBodyOrbit('object')
    
    # prepare plotting
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
    
    ar = None
    
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
    main()

