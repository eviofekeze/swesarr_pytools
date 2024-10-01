# swesarr_pytools


[![image](https://img.shields.io/pypi/v/swesarr_pytools.svg)](https://pypi.python.org/pypi/swesarr_pytools)
[![image](https://img.shields.io/conda/vn/conda-forge/swesarr_pytools.svg)](https://anaconda.org/conda-forge/swesarr_pytools)


**Library for  data retrieval and manipulation swesarr data for the NASA database.**
swesarr_pytool is a python Library created for easy data retrieval and manipulation swesarr data for the NASA database.

The Snow Water Equivalent Synthetic Aperture Radar and Radiometer (SWESARR) is a Tri-Frequency Radar and Radiometer
instrument designed to measure the water content in a snowpack. The instrument, developed at NASA’s Goddard Space Flight
Center, uses active and passive microwave sensors to map the radio frequency emissions of the snowpack, which can then be turned into a measurement of
snow water equivalent.

SWESARR has three active (including a dual Ku band) and three passive bands. Radar data is collected in dual polarization
(VV, VH) while the radiometer makes single polarization (H) observations.



-   Free software: MIT License
-   Documentation: https://eviofekeze.github.io/swesarr_pytools


## Features


```commandline
pip install swesarr_pytool
```

### **Usage**
**Accessing metadata**

The package provide a functionality to retrieve available SWESARR flight paths and flight date, additionally
flight path or list of flight path within a date range can be retrieved if such flight path exist

```python
from swesarr_pytools.access_swesarr import AccessSwesarr
from datetime import date


#Instatiate the Access Object
meta_object = AccessSwesarr()

#Retrieve meta
swesarr_metadata = meta_object.data_meta

#Retrieve flight path
flight_paths = meta_object.flight_names

#Retrieve flight date
flight_dates = meta_object.flight_dates

#search for flight within a date range
available_dates = meta_object.available_date_within_range(start_date=date(2019, 1, 1),
                                               end_date=date(2019, 12, 31))

```

