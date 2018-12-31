# pytwobodyorbit
**pytwobodyorbit** is a module that provides various computations about two-body orbits, including:
* Defines the orbit by position and velocity of an object
* Defines the orbit by classical orbital elements
* Computes position and velocity of an object at a given time
* Provides a series of points on orbital trajectory of an object for visualization
* Solves so-called **Lambert's problem** (When two positions and flight time between them are given, the module computes initial and terminal velocity of the object).

The module contains **TwoBodyOrbit** class and **lambert** function.

## TwoBodyOrbit (Class)
A class that provides a two-body orbit of a celestial body, which orbits around or flies by a central body. 

#### Attributes
* **bodyname**: The name of the celestial body
* **mothername**: The name of the central body
* **mu**: Gravitational parameter (mu) of the central body
  * The dimension of mu prescribes units of length and time used in the instance. For example, when you use the default value of mu (1.32712440041e20), the unit of length should be meters, and the unit of time should be seconds.

#### Methods
* **setOrbCart**: Define the orbit by Cartesian orbital elements (the position and velocity of the body). Arguments are as follows:
  * t: Time
  * pos: Position of the body [x, y, z]; an array-like object
  * vel: Velocity of the body [xd, yd,zd]; an array-like object
* **setOrbKepl**: Define the orbit by classical orbital elements (Keplerian orbital elements). Arguments are as follows:
  * epoch: Epoch
  * a: Semi-major axis
  * e: Eccentricity; 1.0 is not allowed
  * i: Orbital inclination in degrees
  * LoAN: Longitude of ascending node in degrees; if inclination is zero, this value defines a reference longitude of AoP
  * AoP: Argument of periapsis in degrees; if inclination is zero, this value indicates an angle from the reference longitude; for a circular orbit, this value defines a imaginary periapsis
  * Following three keyword parameters (TA, T, MA) are mutually exclusive.  You should specify one of them.
    * TA: True anomaly at epoch in degrees; for a circular orbit, this value indicates an angle from the imaginary periapsis
    * T: Periapsis passage time; for a circular orbit, this value indicates passage time for the imaginary periapsis
    * MA: Mean anomaly at epoch in degrees; for a hyperbolic trajectory, you cannot specify this argument; for a circular orbit, this value indicates anomaly form the imaginary periapsis

* **posvel**: Returns position and velocity of the body for given true anomaly
* **points**: Returns points on orbital trajectory for visualization
* **posvelatt**: Returns position and velocity of the body for given time
* **elmKepl**: Returns classical orbital elements (Keplerian orbital elements) of the orbit

#### Usage

    from pytwobodyorbit import TwoBodyOrbit
    sunmu = 1.32712440041e20
    orbit = TwoBodyOrbit("Space Probe", mu=sunmu)   # create an instance
    t0 = 0.0                                        # epoch
    pos0 = [1e11, 1.2e11, 0.2e11]                   # position
    vel0 = [-2e4, 1.8e4, 0.0]                       # velocity
    orbit.setOrbCart(t0, pos0, vel0)                # define the orbit
    t1 = 100.0 * 86400                              # time after 100 days
    pos, vel = orbit.posvelatt(t1)                  # get position and velocity at t1
    xs, ys, zs, times = orbit.points(100)           # get points (series of 100 points)
    kepl = orbit.elmKepl()                          # get classical orbital elements

The value for the gravitational parameter (1.32712440041e20) is for the Sun, and it prescribes units of length to meters and units of time to seconds.

## lambert (Function)
A function to solve **Lambert's Problem**. From given initial position and terminal position of a body and flight time, the function computes a two-body orbit and returns initial velocity and terminal velocity of the body. The function returns following two numpy arrays. The origin of axes is the central body.
* ivel: Initial velocity of the body [xd, yd, zd]
* tvel: Terminal velocity of the body [xd, yd, zd]

#### Arguments
* ipos: Initial position of an body [x, y, z]; an array-like object; origin of coordinates is the central body
* tpos: Terminal position of an body [x, y, z]; an array-like object; origin of coordinates is the central body


#### Usage

    from pytwobodyorbit import lambert
    P1 = [1.5e11, 0.0, 0.0]                                 # initial position
    P2 = [-0.5e11, 1.3e11, 0.4e11]                          # terminal position
    Ft = 100.0 * 86400                                      # flight time in seconds
    sunmu = 1.32712440041e20                                # mu of the Sun
    prog = True                                             # Prograde orbit
    ivel, tvel = lambert(P1, P2, Ft, mu=sunmu, ccw=prog)    # get initial velocity and terminal velocity

## Install pytwobodyorbit
**pytwobodyorbit** has been registered on PyPI (Python Package Index). You can install it by pip command of Python as follows.

    pip install pytwobodyorbit

## Required environment
* Python 3

## Packages and Modules
* Numpy

## Referenced document
* 室津義定, 宇宙航行力学, 宇宙工学の基礎I, 共立出版株式会社, Japan, 1993-1998

## Modification Log
#### v1.0.0 January 4, 2019
##### TwoBodyOrbit class
* Initiating method was changed its argument name (mmu to mu)
* Method **setOrbKepl** was added to **TwoBodyOrbit** class
* Method **elmKepl** was changed its returning data; keys of dictionary were modified

##### lambert function
* Function name was changed; from *solveGauss* to **lambert**
* The argument "mu" became to have a default value

#### v0.1.0 November 7, 2016
* Initial release

# Programs for testing and demonstration
This repository contains two programs for testing and demonstration of **pytwobodyorbit** module. Those are **testConvert.py** and **testLambert.py**. You can find their scripts in the "source" directory.

## testConvert.py
A program that demonstrates functionalities of the **TwoBodyOrbit** class of **pytwobodyorbit**. By utilizing the class, the program converts a set of classical orbital elements of a body that orbits around or flies by the Sun, into a set of Cartesian orbital elements, and vice versa. In addition, the program draws a 3D chart of the orbit, from classical orbital elements or Cartesian orbital elements.

The program requires **Numpy** and **matplotlib**.

## testLambert.py

A program that demonstrates the **lambert** function of pytwobodyorbit. By utilizing the function, the program compute a two-body orbit from initial position and terminal position of a body that orbit around or flies by the Sun and flight time between them. The program shows you classical orbital elements of the orbit, and draws the orbit into a 3D chart. For the computation of a two-body orbit, you can choose flight direction of the orbit, one is a direct (prograde) orbit and another is a retrograde orbit.

The program requires **Numpy** and **matplotlib**.
