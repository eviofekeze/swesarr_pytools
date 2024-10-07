# Usage

To use swesarr_pytools in a project:

```python
from swesarr_pytools.access_swesarr import AccessSAR
from datetime import date

# Instantiate the Access Object
meta_object = AccessSAR()

# Retrieve meta
swesarr_metadata = meta_object.data_meta

# Retrieve flight path
flight_paths = meta_object.flight_names

# Retrieve flight date
flight_dates = meta_object.flight_dates

# search for flight within a date range
available_dates = meta_object.available_date_within_range(start_date=date(2019, 1, 1),
                                                          end_date=date(2019, 12, 31))

```
