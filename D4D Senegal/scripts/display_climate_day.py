import os
import json
import collections
import warnings
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

basepath='../data'

def get_country_shape():
    with open(os.path.join(basepath,'Senegal_GeoJson.json'),'r') as f:
        geojson=json.loads(f.read())
    return geojson['coordinates']

def plot_geojson_shape(coords):
    if isinstance(coords[0][0], collections.Iterable):
        for c in coords: 
            plot_geojson_shape(c)
    else:
        x = [i for i,j in coords]
        y = [j for i,j in coords]
        plt.plot(x,y,'lightgray')

def display_climate_day(prefix, year, res_in_arcsec):

    rainNodes,rains   = climate_for_year_from_file(os.path.join(basepath, prefix + '_rainfall_daily.bin'), year)
    tempNodes,temps   = climate_for_year_from_file(os.path.join(basepath, prefix + '_air_temperature_daily.bin'), year)
    humidNodes,humids = climate_for_year_from_file(os.path.join(basepath, prefix + '_relative_humidity_daily.bin'), year)

    def lons_lats_from_nodes(nodes):
        latlons=[lat_lon_from_nodeid(n,res_in_arcsec/3600.) for n in nodes]
        return list(reversed(zip(*latlons)))

    day_of_year=301
    rain  = rains[day_of_year-1,:]
    temp  = temps[day_of_year-1,:]
    humid = humids[day_of_year-1,:]

    fig, ax = plt.subplots(figsize=(16,6.5))
    fig.subplots_adjust(left=0.05, bottom=0.1, top=0.9, right=0.97)
    txt = fig.text(0.5, 0.95, '%d - day %d' % (year, day_of_year), fontweight='bold', ha='center')

    country_shape=get_country_shape()

    rain_scatter_panel=plt.subplot(231,aspect=1)
    rain_pos=lons_lats_from_nodes(rainNodes)
    rain_scatter=plt.scatter(*rain_pos,c=rain,s=5,cmap='Greens',lw=0, norm=mpl.colors.LogNorm(), vmin=0.1, vmax=100)
    plt.colorbar()
    plot_geojson_shape(country_shape)

    rain_hist_panel=plt.subplot(234)
    print('Rainfall (mm): [%0.2f - %0.2f]' % (min(rain),max(rain)))
    plt.hist(rain, bins=np.arange(0,100,1), alpha=0.3)
    rain_hist_panel.set_xlabel('Rainfall (mm)')

    nan_temps=np.array([np.isnan(t) for t in temp])
    if sum(nan_temps):
        print('%d NaN temps' % sum(nan_temps))
    def scrub_NaNs(values):
        npvalues=np.array(values)
        scrubbed_values=npvalues[nan_temps==0]
        return scrubbed_values

    temp_scatter_panel=plt.subplot(232,aspect=1)
    temp_pos=lons_lats_from_nodes(scrub_NaNs(tempNodes))
    temp_scatter=plt.scatter(*temp_pos,c=scrub_NaNs(temp),s=5,cmap='Spectral_r',lw=0, vmin=15, vmax=35)
    plt.colorbar()
    plot_geojson_shape(country_shape)

    temp_hist_panel=plt.subplot(235)
    print('Air temperature (C): [%0.2f - %0.2f]' % (min(temp),max(temp)))
    plt.hist(temp, bins=np.arange(0,50,0.2), alpha=0.3)
    temp_hist_panel.set_xlabel('Air temperature (C)')

    humid_scatter_panel=plt.subplot(233,aspect=1)
    humid_pos=lons_lats_from_nodes(humidNodes)
    humid_scatter=plt.scatter(*humid_pos,c=humid,s=5,cmap=plt.cm.get_cmap('Blues'),lw=0, vmin=0, vmax=1)
    plt.colorbar(humid_scatter)
    plot_geojson_shape(country_shape)

    humid_hist_panel=plt.subplot(236)
    print('Relative humidity: [%d - %d%%]' % (100*min(humid),100*max(humid)))
    plt.hist(humid, bins=np.arange(0,1.01,0.01), alpha=0.3)
    humid_hist_panel.set_xlabel('Relative Humidity')

    def redraw(doy):
        txt.set_text('%d - day %d' % (year, doy))

        rain=rains[doy-1,:]
        rain_scatter.set_array(rain)
        rain_hist_panel.clear()
        rain_hist_panel.hist(rain, bins=np.arange(0,100,1), alpha=0.3)
        rain_hist_panel.set_xlabel('Rainfall (mm)')

        temp=scrub_NaNs(temps[doy-1,:])
        temp_scatter.set_array(temp)
        temp_hist_panel.clear()
        temp_hist_panel.hist(temp, bins=np.arange(0,50,0.2), alpha=0.3)
        temp_hist_panel.set_xlabel('Air temperature (C)')

        humid=humids[doy-1,:]
        humid_scatter.set_array(humid)
        humid_hist_panel.clear()
        humid_hist_panel.hist(humid, bins=np.arange(0,1.01,0.01), alpha=0.3)
        humid_hist_panel.set_xlabel('Relative Humidity')

        fig.canvas.draw()

    class Index:
        def __init__(self):
            self.doy = day_of_year
            self.ntsteps = 365
            
        def minus_day(self, event):
            self.doy = self.doy-1 if self.doy > 1 else self.doy
            redraw(self.doy)

        def plus_day(self, event):
            self.doy = self.doy+1 if self.doy < self.ntsteps-1 else self.doy
            redraw(self.doy)

        def minus_wk(self, event):
            self.doy = self.doy-7 if self.doy > 7 else self.doy
            redraw(self.doy)

        def plus_wk(self, event):
            self.doy = self.doy+7 if self.doy < self.ntsteps-7 else self.doy
            redraw(self.doy)

        def minus_mo(self, event):
            self.doy = self.doy-30 if self.doy > 30 else self.doy
            redraw(self.doy)

        def plus_mo(self, event):
            self.doy = self.doy+30 if self.doy < self.ntsteps-30 else self.doy
            redraw(self.doy)

    callback = Index()

    axprev = plt.axes([0.4, 0.94, 0.04, 0.04])
    axnext = plt.axes([0.56, 0.94, 0.04, 0.04])
    axprevwk = plt.axes([0.34, 0.94, 0.04, 0.04])
    axnextwk = plt.axes([0.62, 0.94, 0.04, 0.04])
    axprevmo = plt.axes([0.28, 0.94, 0.04, 0.04])
    axnextmo = plt.axes([0.68, 0.94, 0.04, 0.04])

    bnext = Button(axnext, '+1d')
    bnext.on_clicked(callback.plus_day)

    bprev = Button(axprev, '-1d')
    bprev.on_clicked(callback.minus_day)

    bnextwk = Button(axnextwk, '+1w')
    bnextwk.on_clicked(callback.plus_wk)

    bprevwk = Button(axprevwk, '-1w')
    bprevwk.on_clicked(callback.minus_wk)

    bnextmo = Button(axnextmo, '+1m')
    bnextmo.on_clicked(callback.plus_mo)

    bprevmo = Button(axprevmo, '-1m')
    bprevmo.on_clicked(callback.minus_mo)

    plt.show()

def get_xpix_ypix(nodeid):
    ypix = (nodeid-1) & 2**16-1
    xpix = (nodeid-1) >> 16
    return (xpix,ypix)

def lat_lon_from_nodeid(nodeid, res_in_deg):
    xpix,ypix = get_xpix_ypix(nodeid)
    lat = (0.5+ypix)*res_in_deg - 90.0
    lon = (0.5+xpix)*res_in_deg - 180.0
    return (lat,lon)

def nodeid_from_lat_lon(lat, lon, res_in_deg):
    xpix = int(math.floor((lon + 180.0) / res_in_deg))
    ypix = int(math.floor((lat + 90.0) / res_in_deg))
    nodeid = (xpix << 16) + ypix + 1
    return nodeid

def parse_node_offsets(nodeOffsets, n_nodes):
    nodeIds=[]
    lastOffset=-1
    if len(nodeOffsets)/16 != n_nodes:
        raise Exception('Offset length not compatible with # of nodes from header')
    for i in range(n_nodes):
        nodeId=int(nodeOffsets[i*16:i*16+8],16)
        offset=int(nodeOffsets[i*16+8:i*16+16],16)
        if offset < lastOffset:
            raise Exception('Offsets not sequential')
        else:
            lastOffset=offset
        nodeIds.append(nodeId)
    return nodeIds

def climate_for_year_from_file(climatefile, year):
    with open(climatefile+'.json','r') as header:
        hj=json.loads(header.read())
        n_nodes = hj['Metadata']['NodeCount']
        n_tstep = hj['Metadata']['DatavalueCount']
        years   = hj['Metadata']['OriginalDataYears']
        first_year = int(years.split('-')[0])
        print(os.path.basename(climatefile))
        print( "\tThere are %d nodes and %d time steps" % (n_nodes, n_tstep) )
        print( "\tExtracting year %d from file with range %s" % (year, years) )
        nodeIds = parse_node_offsets(hj['NodeOffsets'], n_nodes)

    with open(climatefile, 'rb') as bin_file:
        channel_dtype = np.dtype( [ ( 'data', '<f4', (1, n_tstep ) ) ] )
        channel_data = np.fromfile( bin_file, dtype=channel_dtype )
        channel_data = np.transpose( channel_data['data'].reshape(n_nodes, n_tstep) )

    if first_year > year or 365*(year-first_year+1) > n_tstep:
        raise Exception('Year %d is not in climate file range: %s' % (year,years))
    if hj['Metadata']['StartDayOfYear'] != 'January 1':
        raise Exception('Starting on days other than January 1st (i.e. %s) not supported' % hj['Metadata']['StartDayOfYear'])

    data = channel_data[365*(year-first_year):365*(year-first_year+1)][:]

    nan_count = np.isnan(data).sum()
    if nan_count:
        warnings.warn('There are %d NaN values in %s' % (nan_count,climatefile), RuntimeWarning)
    inf_count = np.isinf(data).sum()
    if inf_count:
        warnings.warn('There are %d Inf values in %s' % (inf_count,climatefile), RuntimeWarning)
        
    return nodeIds,data

if __name__ == '__main__':    
    display_climate_day('Senegal_Gambia_2.5arcmin', year=2013, res_in_arcsec=150)
