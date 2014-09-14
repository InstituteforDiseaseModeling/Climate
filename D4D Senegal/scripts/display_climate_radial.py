import os
import json
import random
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# A display of DTK climate input files inspired by: http://www.weather-radials.com/
def display_climate_radial(geography, year, tempdata, raindata):

    #Create figure and polar axis
    fig = plt.figure('%s_radial' % geography, facecolor='white', figsize=(8,8))
    ax = fig.add_subplot(111, polar = True, frameon=False)

    mintemp=-30
    maxtemp=40
    ax.text(0,mintemp, geography.upper(), color='#555555', horizontalalignment='center', size=30)
    ax.text(0,maxtemp+1, str(year), color='#555555', horizontalalignment='center', size=10)

    #Min/Max temps as bars
    for i,(tmin,tmax,tmean) in enumerate(tempdata):
        if np.abs(tmax-tmin)<1:
            tmin=tmin-0.5
            tmax=tmax+0.5
        ax.plot([2*np.pi*i/365.0]*2, [tmin,tmax], color=cm.spectral((tmean+5)/45.0), linewidth=1.5, alpha=0.6);

    # plot rainfall as scatters
    ax.scatter([2*np.pi*r/365. for r in raindata['rainydays']], raindata['tcenters'], s=[100*r for r in raindata['rainfalls']], alpha=0.5, facecolor='#99aacc', linewidth=0)

    # tweak ranges and orientation of polar plot
    ax.set_rmax(maxtemp)
    ax.set_rmin(mintemp)
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")

    #Tweak polar axes, gridding, labels
    ax.tick_params(axis='both', colors='#bbbbbb')

    ax.set_xticks([m*2*np.pi/12 for m in range(12)])
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    ax.set_xticklabels( months, fontsize=10 )
    ax.get_xaxis().grid(False)

    plt.rgrids( (0.01, 10, 20, 30, 40), labels=('0 C', '', '20 C', '', '40 C' ), angle=180) # radii only positive here, but override later
    ax.get_yaxis().grid(which='minor',linestyle='-',color='#bbbbbb', alpha=0.3)
    ax.get_yaxis().grid(which='major',linestyle='-',color='#bbbbbb', alpha=0.4, linewidth=1.4)
    ax.set_yticks([10, 30], minor=True)
    ax.set_yticks([0, 20, 40])
    ax.set_yticklabels( ['0 C', '20 C', '40 C' ], fontsize=10)

    plt.show()

def climate_data_from_file(climatefile, year):
    with open(climatefile+'.json','r') as header:
        hj=json.loads(header.read())
        n_nodes = hj['Metadata']['NodeCount']
        n_tstep = hj['Metadata']['DatavalueCount']
        years   = hj['Metadata']['OriginalDataYears']
        first_year = int(years.split('-')[0])
        print(os.path.basename(climatefile))
        print( "\tThere are %d nodes and %d time steps" % (n_nodes, n_tstep) )
        print( "\tExtracting year %d from file with range %s" % (year, years) )

    with open(climatefile, 'rb') as bin_file:
        channel_dtype = np.dtype( [ ( 'data', '<f4', (1, n_nodes ) ) ] )
        channel_data = np.fromfile( bin_file, dtype=channel_dtype )
        channel_data = np.transpose( channel_data['data'].reshape(n_nodes, n_tstep) )

    if first_year > year or 365*(year-first_year+1) > n_tstep:
        raise Exception('Year %d is not in climate file range: %s' % (year,years))
    if hj['Metadata']['StartDayOfYear'] != 'January 1':
        raise Exception('Starting on days other than January 1st (i.e. %s) not supported' % hj['Metadata']['StartDayOfYear'])

    return channel_data[365*(year-first_year):365*(year-first_year+1)][:]

def get_temperature_data(channel_data):
    tempdata = []
    for d in range(365):
        temps=channel_data[d]
        temps=temps[np.isfinite(temps)]
        tempdata.append((np.min(temps), np.max(temps), np.mean(temps)))
    return tempdata

def get_rainfall_data(channel_data, temperature_data):
    raindata = { 'rainydays':[], 'rainfalls':[], 'tcenters':[] }
    for d in range(365):
        mean_rain=np.mean(channel_data[d])
        if mean_rain > 0:
            raindata['rainydays'].append(d)
            raindata['rainfalls'].append(mean_rain)
            raindata['tcenters'].append(tempdata[d][2]) # mean has idx=2 in tuple
    return raindata

if __name__ == '__main__':

    inputdir='../climate_data'
    year = 2013
    geostring=['Senegal_Gambia_2.5arcmin']
   
    tempdata = get_temperature_data(climate_data_from_file(os.path.join(inputdir,'/'.join(geostring[0:-1]),geostring[-1]+'_air_temperature_daily.bin'), year))
    raindata = get_rainfall_data(climate_data_from_file(os.path.join(inputdir,'/'.join(geostring[0:-1]),geostring[-1]+'_rainfall_daily.bin'), year), tempdata)

    display_climate_radial(geography=geostring[0].split('_')[0], year=year, tempdata=tempdata, raindata=raindata)
