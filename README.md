# pytwobodyorbit.py
A two-body orbit computation module

The module contains "TwoBodyOrbit" class and "lambert" function.

## TwoBodyOrbit (Class)
A class that provides a two-body orbit of a celestial body, which orbits around or flys by a central body. 

### Attributes
#### bodyname
The name of the celestial body

#### mothername
The name of the central body

#### mu
Gravitational parameter (mu) of the central body

### Methods
#### __init__
Initialize attributes of a instance

#### setOrbCart
Define the orbit by Cartesian orbital elements (the position and velocity of the body).

#### setOrbKepl
Define the orbit by classical orbital elements (Keplerian orbital elements).
Arguments are as follows:
* epoch: Epoch
* a: Semi-major axis
* e: Eccentricity; 1.0 is not allowed
* i: Orbital inclination in degrees
* LoAN: Longitude of ascending node in degrees; if inclination is zero, this value defines a reference longitude of AoP
* AoP: Argument of periapsis in degrees; if inclination is zero, this value indicates an angle from reference longitude; for a circular orbit, this value defines a imaginary periapsis
* TA: True anomaly at epoch in degrees; for a circular orbit, this value indicates an angle from the imaginary periapsis
* T: Periapsis passage time; for a circular orbit, this value indicates passage time for the imaginary periapsis
* MA: Mean anomaly at epoch in degrees; for a hyperbolic trajectory, you cannot specify this argument; for a circular orbit, this value indicates anomaly form the imaginary periapsis
Three keyword parameters (TA, T, MA) are mutually execlusive.  You should specify one of them.

#### posvel
Returns position and velocity of the body for given true anomaly

#### points
Returns points on orbital trajectory for vusualization

#### posvelatt
Returns position and velocity of the body for given time

#### elmKepl
Returns classical orbital elements (Keplerian orbital elements) of the orbit

### Usage

## lambert (Function)
A function to solve "Lambert's Problem"

From given initial position, terminal position, and flight time, compute initial velocity and terminal velocity.

### Usage
In this sampe code we use the default value for mu. The value is gravitational palameter of the Sun.  The value requires length in meters, time in seconds.
    from pytwobodyorbit import TwoBodyOrbit
    orbit = TwoBodyOrbit("Space Probe")     # create an instance
    t0 = 0.0                                # epoch
    pos0 = [1e11, 1.2e11, 0.2e11]           # position
    vel0 = [-2e4, 1.8e4, 0.0]               # velocity
    orbit.setOrbCart(t0, pos0, vel0)        # define the orbit
    t1 = 100.0 * 86400                      # time after 100 days
    pos, vel = orbit.posvelatt(t1)          # get position and velocity
    xs, ys, zs, times = orbit.points(100)   # get points
    kepl = orbit.elmKepl()                  # get classical orbital elements

## Required environment
* Python 3

## Packages and Modules
* Numpy

## Referenced document
* 室津義定, 宇宙航行力学, 宇宙工学の基礎I, 共立出版株式会社, Japan, 1993-1998

## Modification Log
#### 1.0.0 January 4, 2019
* Method "setOrbKepl" was added to "TwoBodyOrbit" class
* Method "elmKepl" changed its returning data; keys of dictionary were changed
* Function name was changed; from "solveGauss" to "lambert"

#### 0.1.0 November 7, 2016
* Initial release

# Programs for testing and demonstration
## testConvert.py


## testLambert.py

