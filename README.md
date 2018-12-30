# pytwobodyorbit
"pytwobodyorbit" is a module that provides various computations about two-body orbits, including:
* Defines the orbit by position and velocity of an object
* Defines the orbit by classical orbital elements
* Computes position and velocity of an object at a given time
* Provides seriese of points on orbital trajectory of an object for visualization
* Solves so-called "Lambert's problem" (When two positions and flight time between them are given, the module computes initial and terminal velocity of the object).

The module contains "TwoBodyOrbit" class and "lambert" function.

## TwoBodyOrbit (Class)
A class that provides a two-body orbit of a celestial body, which orbits around or flys by a central body. 

#### Attributes
* bodyname: The name of the celestial body
* mothername: The name of the central body
* mu: Gravitational parameter (mu) of the central body

#### Methods
* setOrbCart: Define the orbit by Cartesian orbital elements (the position and velocity of the body)
* setOrbKepl: Define the orbit by classical orbital elements (Keplerian orbital elements). Arguments are as follows:
  * epoch: Epoch
  * a: Semi-major axis
  * e: Eccentricity; 1.0 is not allowed
  * i: Orbital inclination in degrees
  * LoAN: Longitude of ascending node in degrees; if inclination is zero, this value defines a reference longitude of AoP
  * AoP: Argument of periapsis in degrees; if inclination is zero, this value indicates an angle from the reference longitude; for a circular orbit, this value defines a imaginary periapsis
  * Following three keyword parameters (TA, T, MA) are mutually execlusive.  You should specify one of them.
    * TA: True anomaly at epoch in degrees; for a circular orbit, this value indicates an angle from the imaginary periapsis
    * T: Periapsis passage time; for a circular orbit, this value indicates passage time for the imaginary periapsis
    * MA: Mean anomaly at epoch in degrees; for a hyperbolic trajectory, you cannot specify this argument; for a circular orbit, this value indicates anomaly form the imaginary periapsis

* posvel: Returns position and velocity of the body for given true anomaly
* points: Returns points on orbital trajectory for vusualization
* posvelatt: Returns position and velocity of the body for given time
* elmKepl: Returns classical orbital elements (Keplerian orbital elements) of the orbit

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

In this sampe code we used the default value for mu. The value is gravitational palameter of the Sun.  The value requires length in meters, time in seconds.

## lambert (Function)
A function to solve "Lambert's Problem". From given initial position, terminal position, and flight time, the function computes initial velocity and terminal velocity.

#### Usage

    from pytwobodyorbit import lambert
    P1 = [1.5e11, 0.0, 0.0]                                 # initial position
    P2 = [-0.5e11, 1.3e11, 0.4e11]                          # terminal position
    Ft = 100.0 * 86400                                      # flight time in seconds
    sunmu = 1.32712440041e20                                # mu of the Sun
    prog = True                                             # Prograde orbit
    ivel, tvel = lambert(P1, P2, Ft, mu=sunmu, ccw=prog)    # get initial velocity and terminal velocity
    
## Required environment
* Python 3

## Packages and Modules
* Numpy

## Referenced document
* 室津義定, 宇宙航行力学, 宇宙工学の基礎I, 共立出版株式会社, Japan, 1993-1998

## Modification Log
#### 1.0.0 January 4, 2019
##### TwoBodyOrbit class
* Constructor method was changed its argument name (mmu to mu)
* Method "setOrbKepl" was added to "TwoBodyOrbit" class
* Method "elmKepl" was changed its returning data; keys of dictionary were modified
##### lambert function
* Function name was changed; from "solveGauss" to "lambert"

#### 0.1.0 November 7, 2016
* Initial release

# Programs for testing and demonstration
## testConvert.py


## testLambert.py

