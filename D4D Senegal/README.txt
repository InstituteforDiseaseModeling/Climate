/*****************************************************************************

Copyright (c) 2014 by Global Good Fund I, LLC. All rights reserved.

Except for any rights expressly granted to you in a separate license with the
Global Good Fund (GGF), GGF reserves all rights, title and interest in the
software and documentation.  GGF grants recipients of this software and
documentation no other rights either expressly, impliedly or by estoppel.

THE SOFTWARE AND DOCUMENTATION ARE PROVIDED "AS IS" AND GGF HEREBY DISCLAIMS
ALL WARRANTIES, EXPRESS OR IMPLIED, OR STATUTORY, INCLUDING IMPLIED WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT.

*****************************************************************************/

Contents of this bundle:

climate_data/
    Senegal GeoJSON shape
    Daily gridded binary files and meta-data headers (2.5arcmin) for Senegal + Gambia in 2013
        Mean air temperature, relative humidity, and rainfall

scripts/
    display_climate_radial.py (An example of reading and plotting from binary files)
    display_climate_day.py (An interactive viewer for each of 365 days of content in binary files)

figures/
    Output of above scripts
    weather_station_comparisons/
        Information on Senegal weather stations reporting in 2013
        Comparisons of smoothed interpolated daily values (gray) to weather station readings (colors)

publications/
    journal.pone.0094741.pdf 
        Description of methods for generating rasters from weather station and satellite data
