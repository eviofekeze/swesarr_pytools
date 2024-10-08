# Welcome to swesarr_pytools


[![image](https://img.shields.io/pypi/v/swesarr_pytools.svg)](https://pypi.python.org/pypi/swesarr_pytools)


**Library for data retrieval and processing of NASA GSFC Snow Water Equivalent Synthetic Aperture Radar and Radiometer data.**

swesarr_pytool is a python library for data retrieval and processing of NASA GSFC Snow Water Equivalent Synthetic Aperture Radar and Radiometer data.

The Snow Water Equivalent Synthetic Aperture Radar and Radiometer (SWESARR) is a Tri-Frequency Radar and Radiometer
instrument designed to measure the water content in a snowpack. The instrument, developed at NASA’s Goddard Space Flight
Center, uses active and passive microwave sensors to map the radio frequency emissions of the snowpack, which can then be turned into a measurement of
snow water equivalent.

SWESARR has three active (including a dual Ku band) and three passive bands. Radar data is collected in dual polarization
(VV, VH) while the radiometer makes single polarization (H) observations of microwave brightness temperature. Radiometer
observations were made at three frequencies (10.65, 18.7, and 36.5 GHz; referred to as X, K, and Ka bands,
respectively), at horizontal polarization with a nominal 45-degree look angle.

To learn more about SWESARR, please see this tutorial delivered during the NASA Earth Science & UW Hackweek 2024:
<https://snowex-2024.hackweek.io/tutorials/swesarr/swesarr_tut.html>

For general information about swesarr see:

- <https://earth.gsfc.nasa.gov/bio/instruments/snow-water-equivalent-sar-and-radiometer-swesarr>
- <https://snow.nasa.gov/instruments/swesarr>
- <https://www.thenewtoncorp.com/case-studies/swesarr-snow-water-equivalent-synthetic-aperture-radar-and-radiometer>

---
-   Free software: MIT License
-   Documentation: <https://eviofekeze.github.io/swesarr_pytools>


## Features
- Downloading Swesarr data
- Searching available swesarr flights
- Retrieving swesarr flight metadata
- Reading a raster, Lidar and SWESARR
- Converting SWESARR to dataframe
- Combining Fall and Winter SWESARR flights into one data frame for analysis



**Reference:**

[1] R. Rincón et al., "Performance of Swesarr's Multi-Frequency Dual-Polarimetry Synthetic Aperture Radar During Nasa's
Snowex Airborne Campaign," IGARSS 2020 - 2020 IEEE International Geoscience and Remote Sensing Symposium, Waikoloa, HI,
USA, 2020, pp. 6150-6153, doi: 10.1109/IGARSS39084.2020.9324391. keywords: {Radar;Snow;Radar antennas;Synthetic aperture
radar; Spaceborne radar;Airborne radar;Instruments;Snow;SAR;SWE},

[2] D. R. Boyd, A. M. Alam, M. Kurum, A. C. Gurbuz and B. Osmanoglu, "Preliminary Snow Water Equivalent Retrieval of
SnowEX20 Swesarr Data," IGARSS 2022 - 2022 IEEE International Geoscience and Remote Sensing Symposium, Kuala Lumpur,
Malaysia, 2022, pp. 3927-3930, doi: 10.1109/IGARSS46834.2022.9883412. keywords: {Radio frequency;Sensitivity;Radar
measurements;Spaceborne radar;Snow;NASA;Prediction algorithms;Snow;SWE;Radar;SWESARR;SAR;SnowEx},
