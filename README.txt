Python module for computations about Kepler orbit

This module provides following computations: 
  Compute Keplerian orbital elements from position and velocity, 
  Provide series of points on orbital trajectory for visualization, 
  Predict position and velocity of the object for given time, 
  Solve the Gauss problem (From given two positions and flight duration between 
  them, solveGauss() computes initial and terminal velocity of the object)

Usage: (use help command on python console for definition of I/O)
  orbit = pytwobodyorbit.TwoBodyOrbit('object_name', mname='central_body_name', mmu=mu) 
      # Generate an instance.
  orbit.setOrbCart(epoch, position, velocity) 
      # Initialize the orbit with epoch, position and velocity.
  kepl = orbit.elmKepl() 
      # Get Keplerian orbital elements.
  xs, ys, zs, times = orbit.points(ndata) 
      # Get a series of points of the trajectory.
  ppos, pvel = orbit.posvelatt(t) 
      # Get predicted position and velocity at the time t.

  ivel, tvel = pytwobodyorbit.solveGauss(ipos, tpos, targett, mu, ccw=True)
      # Get initial velocity and terminal velocity of the flight.

Referenced document:
宇宙工学の基礎I 宇宙航行力学, 1993, 室津義定, 共立出版株式会社
