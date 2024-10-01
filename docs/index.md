# Welcome to swesarr_pytools


[![image](https://img.shields.io/pypi/v/swesarr_pytools.svg)](https://pypi.python.org/pypi/swesarr_pytools)


**Library for data retrieval and processing of NASA GSFC Snow Water Equivalent Synthetic Aperture Radar and Radiometer data.**

swesarr_pytool is a python library for data retrieval and processing of NASA GSFC Snow Water Equivalent Synthetic Aperture Radar and Radiometer data.

The Snow Water Equivalent Synthetic Aperture Radar and Radiometer (SWESARR) is a Tri-Frequency Radar and Radiometer
instrument designed to measure the water content in a snowpack. The instrument, developed at NASA’s Goddard Space Flight
Center, uses active and passive microwave sensors to map the radio frequency emissions of the snowpack, which can then be turned into a measurement of
snow water equivalent.

SWESARR has three active (including a dual Ku band) and three passive bands. Radar data is collected in dual polarization
(VV, VH) while the radiometer makes single polarization (H) observations.



-   Free software: MIT License
-   Documentation: <https://eviofekeze.github.io/swesarr_pytools>


## Features
- Downloading Swesarr data
- Searching available swesarr flights
- Retrieving swesarr flight metadata
- Reading a raster, Lidar and SWESARR
- Converting SWESARR to dataframe
- Combining Fall and Winter SWESARR flights into one data frame for analysis
