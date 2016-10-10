# -*- coding: utf-8 -*-
"""Comutations about Kepler Orbits

This module provide computations about Kepler orbits, including:
  Compute Keplerian orbital elements from position and velocity
  Provide seriese of points on orbital trajectory for visualization
  Predict position and velocity of the object for given time
  Solve the Gauss problem  (From given two positions and flight duration 
  between them, solveGauss() computes initial and terminal velocity of 
  the object)

@author: whiskie14142
"""

import numpy as np
import math
from scipy.optimize import newton
from scipy.optimize import bisect

  
class TwoBodyOrbit:
    """Class for the Kepler orbit of a celestial object
    
    """
    def timeFperi(self, ta):
        """Computes time from periapsis passage for given true anomaly
        
        Args:
            ta: True Anomaly in radians
        Returns: sec_from_peri
            sec_from_peri: Time from periapsis passage (float). Unit of time
                           depends on gravitational parameter (mu)
        """
        if not self._setOrb:
            raise(RuntimeError('Orbit has not been defined: TwoBodyOrbit'))
            
        r = self.a * (1.0 - self.e ** 2) / (1.0 + self.e * np.cos(ta))
        if self.e < 1.0:
            b_over_a = np.sqrt(1.0 - self.e ** 2)
            ecc_anm = np.arctan2(r * np.sin(ta) / b_over_a, self.a * self.e \
                + r * np.cos(ta))
            if ecc_anm < 0.0: ecc_anm += math.pi * 2.0
            sec_from_peri = np.sqrt(self.a **3 / self.mu) * (ecc_anm - self.e \
                * np.sin(ecc_anm))
        elif self.e == 1.0:
            ecc_anm = np.sqrt(self.p) * np.tan(ta / 2.0)
            sec_from_peri = (self.p * ecc_anm + ecc_anm ** 3 / 3.0) / 2.0 / \
                np.sqrt(self.mu)
        else:
            sy = (self.e + np.cos(ta)) / (1.0 + self.e * np.cos(ta))
            lf = np.log(sy + np.sqrt(sy ** 2 - 1.0))
            if (ta < 0.0) or (ta > math.pi): lf = lf * (-1.0)
            sec_from_peri = np.sqrt((-1.0) * self.a ** 3 / self.mu) * (self.e \
                * np.sinh(lf) - lf)
        return sec_from_peri
        
    def posvel(self, ta):
        """Comuputs position and velocity for given true anomaly
        
        Args:
            ta: True Anomaly in radians
        Returns: rv, vv
            rv: Position (x,y,z) as numpy array
            vv: Velocity (xd,yd,zd) as numpy array
                Units are depend on gravitational parameter (mu)
        """
        if not self._setOrb:
            raise(RuntimeError('Orbit has not been defined: TwoBodyOrbit'))

        PV = self.ev / np.sqrt(np.dot(self.ev, self.ev))
        QV = np.cross(self.hv, PV) / np.sqrt(np.dot(self.hv, self.hv))
        r = self.p / (1.0 + self.e * np.cos(ta))
        rv = r * np.cos(ta) * PV + r * np.sin(ta) * QV
        vv = np.sqrt(self.mu / self.p) * ((-1.0) * np.sin(ta) * PV + (self.e \
            + np.cos(ta)) * QV)
        return rv, vv

    def __init__(self, bname, mname='Sol', mmu=1.32712440041e20):
        """
        Args:
            bname: Name of the object which orbit around the central body
            mname: Name of the body
            mmu : Gravitational parameter (mu) of the central body
                Default value is mu of the Sun.
                
                mu should be:
                if Mc >> Mo
                    mu = GMc
                else
                    mu = G(Mc + Mo)

                where
                    G: Newton's gravitational constant
                    Mc: mass of the central body
                    Mo: mass of the object
        """
        self._setOrb = False
        self.bodyname = bname
        self.mothername = mname
        self.mu = mmu
    
    def setOrbCart(self, t, pos, vel):
        """Define the orbit by epoch, position, and velocity
        
        Args:
            t: Epoch
            pos: Position (x,y,z), array like object
            vel: Velocity (xd,yd,zd), array like object
                Units are depend on gravitational parameter (mu)
                Origin of coordinates are position of the central body
        """
        self.t0 = t
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self._setOrb = True
        
        # Computes Keplerian orbital elements
        r0 = np.array(self.pos)
        r0len = np.sqrt(np.dot(r0, r0))
        
        rd0 = np.array(self.vel)
        rd0len2 = np.dot(rd0, rd0)
        
        ev = ((rd0len2 - self.mu/r0len) * r0 - np.dot(r0, rd0) * rd0) / self.mu
        # eccentricity vector
        
        h = np.cross(r0, rd0)
        hlen2 = np.dot(h, h)
        hlen = np.sqrt(hlen2)
        
        K = np.array([0., 0., 1.])
        n = np.cross(K, h)
        n_norm = n / np.sqrt(np.dot(n, n))
        
        hn = np.cross(h, n)
        hn_norm = hn / np.sqrt(np.dot(hn, hn))
        
        he = np.cross(h, ev)
        he_norm = he / np.sqrt(np.dot(he, he))
        ev_norm = ev / np.sqrt(np.dot(ev, ev))
        
        self.hv = h                             # orbital mormentum vecctor
        self.p = hlen2 / self.mu                # semi-latus rectum
        self.ev = ev                            # eccentricity vector
        self.e = np.sqrt(np.dot(ev, ev))        # eccentricity
        self.a = self.p / (1.0 - self.e ** 2)   # semi-major axis
        self.i = np.arccos(h[2] / hlen)         # inclination (radians)
        self.lan = np.arctan2(n[1], n[0])       # longitude of ascending node (radians)
        if self.lan < 0.0:
            self.lan += math.pi * 2.0
        self.parg = np.arctan2(np.dot(ev, hn_norm), np.dot(ev, n_norm))    # periapsis argument (radians)
        if self.parg < 0.0:
            self.parg += math.pi * 2.0
        self.ta0 = np.arctan2(np.dot(he_norm, r0), np.dot(ev_norm, r0))     # true anomaly of epoch

        # time from recent periapsis, mean anomaly, periapsis passage time        
        timef = self.timeFperi(self.ta0)
        self.ma = None
        self.pr = None
        self.n = None
        if self.e < 1.0:
            self.pr = (2.0 * math.pi * np.sqrt(self.a ** 3 /self.mu))   # orbital period
            self.ma = timef / self.pr * math.pi * 2.0                   # Mean anomaly (rad)
            self.n = 2.0 * math.pi / self.pr                            # mean motion (rad/time)
        self.T = self.t0 - timef                                        # periapsis passage time
    
    def points(self, ndata):
        """Returns points on orbital trajectory for visualization
        
        Args:
            ndata: Number of points
        Returns: xs, ys, zs, times
            xs: Array of x-coordinates (Numpy array)
            ys: Array of y-coordinates (Numpy array)
            zs: Array of z-coordinates (Numpy array)
            times: Array of times (Numpy array)
            
            Origin of coordinates are position of the central body
        """
        if not self._setOrb:
            raise(RuntimeError('Orbit has not been defined: TwoBodyOrbit'))

        times = np.zeros(ndata)
        xs = np.zeros(ndata)
        ys = np.zeros(ndata)
        zs = np.zeros(ndata)
        tas = np.zeros(ndata)
        
        if self.e < 1.0:
            tas =np.linspace(0.0, math.pi * 2.0, ndata)
        else:
            if self.e == 1.0:
                stop = math.pi
                start = (-1.) * stop
            else:
                stop = math.pi - np.arccos(1.0 / self.e)
                start = (-1.) * stop
            delta = (stop - start) / (ndata + 1)
            tas = np.linspace(start + delta, stop - delta, ndata)
        for j in range(ndata):
            ta =tas[j]
            times[j] = self.timeFperi(ta) + self.T
            xyz, xdydzd =self.posvel(ta)
            xs[j] = xyz[0]
            ys[j] = xyz[1]
            zs[j] = xyz[2]
        
        return xs, ys, zs, times

    def posvelatt(self, t):
        """Returns position and velocity of the object at given t
        
        Args:
            t: Time
        Returns: newpos, newvel
            newpos: Position of the object at t (x,y,z) (Numpy array)
            newvel: Velocity of the object at t (xd,yd,zd) (Numpy array)
        Exception:
            RuntimeError: 
            
            Origin of coordinates are position of the central body
        """
        def _Cz(z):
            if z < 0:
                return (1.0 - np.cosh(np.sqrt((-1)*z))) / z
            else:
                return (1.0 - np.cos(np.sqrt(z))) / z
            
        def _Sz(z):
            if z < 0:
                sqz = np.sqrt((-1)*z)
                return (np.sinh(sqz) - sqz) / sqz ** 3
            else:
                sqz = np.sqrt(z)
                return (sqz - np.sin(sqz)) / sqz ** 3

        def _func(xn, targett):
            z = xn * xn / self.a
            sr = np.sqrt(np.dot(self.pos, self.pos))
            tn = (np.dot(self.pos, self.vel) / np.sqrt(self.mu) * xn * xn \
                * _Cz(z) + (1.0 - sr / self.a) * xn ** 3 * _Sz(z) + sr * xn) \
                / np.sqrt(self.mu) - targett
            return tn
        
        def _fprime(x, targett):
            z = x * x / self.a
            sqmu = np.sqrt(self.mu)
            sr = np.sqrt(np.dot(self.pos, self.pos))
            dtdx = (x * x * _Cz(z) + np.dot(self.pos, self.vel) / sqmu * x \
                * (1.0 - z * _Sz(z)) + sr * (1.0 - z * _Cz(z))) / sqmu
            return dtdx

        if not self._setOrb:
            raise(RuntimeError('Orbit has not been defined: TwoBodyOrbit'))

        delta_t = (t - self.t0)
        if delta_t == 0.0:
            return self.pos + 0.0, self.vel + 0.0
            # you should not return self.pos. it can cause trouble!
        x0 = np.sqrt(self.mu) * delta_t / self.a
        try:
            # compute with scipy.optimize.newton
            xn = newton(_func, x0, args=(delta_t,), fprime=_fprime)
        except RuntimeError:
            # Configure boundaries for scipy.optimize.bisect
            # b1: Lower boundary
            # b2: Upper boundary
            f0 = _func(x0, delta_t)
            if f0 < 0.0:
                b1 = x0
                found = False
                for i in range(50):
                    x1 = x0 + 10 ** (i + 1)
                    test = _func(x1, delta_t)
                    if test > 0.0:
                        found = True
                        b2 = x1
                        break
                if not found:
                    raise(RuntimeError('Could not compute position and ' +
                    'velocity: TwoBodyOrbit.posvelatt'))
            else:
                b2 = x0
                found = False
                for i in range(50):
                    x1 = x0 - 10 ** (i + 1)
                    test = _func(x1, delta_t)
                    if test < 0.0:
                        found = True
                        b1 = x1
                        break
                if not found:
                    raise(RuntimeError('Could not compute position and ' + 
                    'velocity: TwoBodyOrbit.posvelatt'))

            # compute with scipy.optimize.bisect
            xn = bisect(_func, b1, b2, args=(delta_t,), maxiter=200)
            
        z = xn * xn / self.a
        sr = np.sqrt(np.dot(self.pos, self.pos))
        sqmu = np.sqrt(self.mu)
        val_f = 1.0 - xn * xn / sr * _Cz(z)
        val_g = delta_t - xn ** 3 / sqmu * _Sz(z)
        newpos = self.pos * val_f + self.vel * val_g
        newr = np.sqrt(np.dot(newpos, newpos))
        val_fd = sqmu / sr / newr * xn * (z * _Sz(z) - 1.0)
        val_gd = 1.0 - xn * xn / newr * _Cz(z)
        newvel = self.pos * val_fd + self.vel * val_gd
        return newpos, newvel
    
    def elmKepl(self):
        """Returns Keplerian orbital element
        
        Returns:
            kepl: Dictionary of orbital elements.
                'a': Semimajor axis
                'e': Eccentricity
                'i': Inclination in degrees
                'Lomega': Longitude of ascending node in degrees
                'Somega': Argument of periapsis in degrees
                'TAoE': True anomaly at epoch in degrees
                'T': Periapsis passage time
                'ma': Mean anomaly at epoch in degrees (elliptic orbit only)
                'n': Mean motion in degrees (elliptic orbit only)
                'P': Orbital period (elliptic orbit only)
        """
        if not self._setOrb:
            raise(RuntimeError('Orbit has not been defined: TwoBodyOrbit'))

        kepl = {'epoch':self.t0, \
        'a':self.a, \
        'e':self.e, \
        'i':math.degrees(self.i), \
        'Lomega':math.degrees(self.lan), \
        'Somega':math.degrees(self.parg), \
        'TAoE':math.degrees(self.ta0), \
        'T':self.T}
        if self.e < 1.0:
            kepl['ma'] = math.degrees(self.ma)
            kepl['n'] = math.degrees(self.n)
            kepl['P'] = self.pr
        return kepl

def solveGauss(ipos, tpos, targett, mu, ccw=True):
    """Solve the Gauss Problem
    
    From given initial position, terminal position, and flight duration, 
    compute initial velocity and terminal velocity.
    Args: ipos, tpos, targett, mu, ccw
        ipos: Initial position of the object (x,y,z) as Numpy array
        tpos: Terminal position of the object (x,y,z) as Numpy array
        targett: Orbital duration
        mu: Gravitational parameter of the central body
        ccw: Flag for orbital direction. If True, counter clockwise
    Returns: ivel, tvel
        ivel: Initial velocity of the object (xd,yd,zd) as Numpy array
        tvel: Terminal velocity of the object (xd,yd,zd) as Numpy array
    Exception:
        ValueError: When input data (ipos, tpos, targett) are incovenient,
                    this function raises exception
                    
        Origin of coordinates are position of the central body
    """
    
    def _Cz(z):
        if z < 0:
            return (1.0 - np.cosh(np.sqrt((-1)*z))) / z
        else:
            return (1.0 - np.cos(np.sqrt(z))) / z
            
    def _Sz(z):
        if z < 0:
            sqz = np.sqrt((-1)*z)
            return (np.sinh(sqz) - sqz) / sqz ** 3
        else:
            sqz = np.sqrt(z)
            return (sqz - np.sin(sqz)) / sqz ** 3

    def _func(z, targett, r1pr2, A, mu):
        val_y = r1pr2 - A * (1.0 - z * _Sz(z)) / np.sqrt(_Cz(z))
        val_x = np.sqrt(val_y / _Cz(z))
        t = (val_x ** 3 * _Sz(z) + A * np.sqrt(val_y)) / np.sqrt(mu)

        return t - targett

    sipos = np.array(ipos)
    stpos = np.array(tpos)
    tsec = targett * 1.0
    
    r1 = np.sqrt(np.dot(sipos, sipos))
    r2 = np.sqrt(np.dot(stpos, stpos))

    r1cr2 = np.cross(sipos, stpos)
    r1dr2 = np.dot(sipos, stpos)
    sindnu = np.sqrt(np.dot(r1cr2, r1cr2)) / r1 / r2

    if r1cr2[2] < 0.0: sindnu = (-1) * sindnu
    if not ccw: sindnu = (-1) * sindnu
        
    cosdnu = r1dr2 / r1 / r2
    A = np.sqrt(r1 * r2) * sindnu / np.sqrt(1.0 - cosdnu)
    r1pr2 = r1 + r2

    dnu = np.arctan2(sindnu, cosdnu)
    if dnu < 0.0: dnu += (math.pi * 2.0)

    # Check difference of true anomaly of two points
    # The threshold 0.001 is an empirical value
    if dnu < 0.001 or dnu > (math.pi * 2.0 - 0.001):
        raise(ValueError('Difference in true anomaly is too small:' +
                            ' solveGauss'))
    
    # Check difference of true anomaly of two points
    # The threshold 0.00001 is an empirical value
    if (dnu - math.pi) ** 2 < 0.00001 ** 2:
        raise(ValueError('Two points are placed opposite each' +
                            ' other: solveGauss'))
    
    # Configure boundaries for scipy.optimize.bisect
    # b1: Lower boundary
    # b2: Upper boundary
    inf = float('inf')
    minb1 = (-1.0) * (math.pi * 2.0) ** 2   # minimum limit for b1
    
    # find b2 candidate
    found = False
    for i in range(10):
        b2 = (math.pi * 2.0) ** 2 - 1.0 / 10.0 ** i
        test = _func(b2, tsec, r1pr2, A, mu)
        if test == test and test != inf:  # if (not 'nan') and (!= 'inf')
            if test > 0.0:
                found = True
                break
    if not found:
        raise(ValueError('Could not solve Gauss Plobrem: solveGauss'))        
    
    # configure b1, and b2
    b1 = (-1.0) * dnu ** 2
    lastb1 = b2
    found = False
    for i in range(100):
        test = _func(b1, tsec, r1pr2, A, mu)
        if test == test and test != inf:  # if (not 'nan') and (!= 'inf')
            if test > 0.0:
                lastb1 = b1
                b1 = (b1 + minb1) / 2.0
            else:
                b2 = lastb1
                found = True
                break
        else:
            b1 = (b1 + lastb1) /2.0
    if not found:
        raise(ValueError('Could not solve Gauss Plobrem: solveGauss'))        
    
    zn = bisect(_func, b1, b2, args=(tsec, r1pr2, A, mu), maxiter=100)

    val_y = r1pr2 - A * (1.0 - zn * _Sz(zn)) / np.sqrt(_Cz(zn))
    val_f = 1.0 - val_y / r1
    val_g = A * np.sqrt(val_y / mu)
    val_gd = 1.0 - val_y / r2
    
    ivel = (stpos - val_f * sipos) / val_g
    tvel = (val_gd * stpos - sipos) / val_g
    
    return ivel, tvel

def main():
    """Main program for test and demonstration
    
    Run this module as main program, and try 100, 300, 60 for 
    'Flight Duration' at first.  You may try other values also.
    Additionally, you may change parameters in lines commented with '***'
    
    On the plotting window, you can rotate the image (left-button dragging),
    and zoom (right-button dragging-up and dragging-down)
    """
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    
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
    