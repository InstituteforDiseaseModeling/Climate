#### Contents

`climate_data/` Senegal GeoJSON shape, daily gridded binary files and meta-data headers (2.5arcmin) for Senegal + Gambia in 2013 (Mean air temperature, relative humidity, and rainfall)

`scripts/`
  - `display_climate_radial.py` (An example of reading and plotting from binary files)
  - `display_climate_day.py` (An interactive viewer for each of 365 days of content in binary files)

`figures/` Output of above scripts
  - `weather_station_comparisons/` Information on Senegal weather stations reporting in 2013, comparisons of smoothed interpolated daily values (gray) to weather station readings (colors)

`publications/`
  - `journal.pone.0094741.pdf` Description of methods for generating rasters from weather station and satellite data

#### Dependencies

Running the scripts requires Python and the matplotlib package.
