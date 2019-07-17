from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


nc = '../data/surface_chem_E3SM_v0_MOA.nc'
nc = netcdf_dataset(nc)

variable_names =  ["mom_a1", "mom_a2", "mom_a3", "mom_a4",
                   "mom_c1", "mom_c2", "mom_c3", "mom_c4",
                   "ncl_a1", "ncl_a2", "ncl_a3",
                   "ncl_c1", "ncl_c2", "ncl_c3",
                   "pom_a1", "pom_a3", "pom_a4",
                   "pom_c1", "pom_c3", "pom_c4",
                   "soa_a1", "soa_a2", "soa_a3",
                   "soa_c1", "soa_c2", "soa_c3",
                   "so4_a1", "so4_a2", "so4_a3",
                   "so4_c1", "so4_c2", "so4_c3",
                   "dst_a1", "dst_a3",
                   "dst_c1", "dst_c3",
                   "bc_a1", "bc_a3", "bc_a4",
                   "bc_c1", "bc_c3", "bc_c4",
                   "num_a1", "num_a2", "num_a3", "num_a4",
                   "num_c1", "num_c2", "num_c3", "num_c4",
                   "wat_a1", "wat_a2", "wat_a3", "wat_a4",
                   "Q", "PS", "T",
                   "dgnd_a01", "dgnd_a02",
                   "dgnd_a03", "dgnd_a04"]
month_names = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]

t = nc.dimensions['time']
lat = nc.variables['lat']
lon = nc.variables['lon']

##calculate global concentration for all species
num_names =["num_a1", "num_a2", "num_a3", "num_a4",
            "num_c1", "num_c2", "num_c3", "num_c4"]

empty_array = np.zeros_like(nc.variables[num_names[0]])
empty_array = empty_array.reshape(12,192,288)

num_sum = deepcopy(empty_array)

for i in range(len(num_names)): #add modes together (lat/lon/time pointwise)
    num_sum+=nc.variables[num_names[i]][:,0,:,:]

##Calculate moist density
# Vapor pressure
vapor_pressure = deepcopy(empty_array)
vapor_pressure = nc.variables['Q'][:,0,:,:]/(nc.variables['Q'][:,0,:,:]+0.622) * nc.variables['PS'][:] 
# Moist air density [kg/m3]
moist_density = deepcopy(empty_array)
moist_density = (nc.variables['PS'][:] - vapor_pressure)/(287.0531 * nc.variables['T'][:,0,:,:]) + vapor_pressure/(461.4964 * nc.variables['T'][:,0,:,:])

#multiply concentration by moist density to reach aerosol conc per m^3 
    #(lat/lon/time pointwise still)
num_sum_vol = num_sum * moist_density

#take average of months (end up with lat/lon array, size 1 in time dimension)
num_sum_vol_avg = np.sum(num_sum_vol,axis=0)/12.

## ALL-MODE ANNUAL PLOT

ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

cs = plt.contourf(lon[:],lat[:],num_sum_vol_avg) 

cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
cbar.set_label('Total species number per cubic meter')

plt.title("Global ANN avg Aerosol Concentration: All Modes")

plt.savefig('ann_allmodes.png',type='png')

plt.close()

## MODE-SPECIFIC ANNUAL PLOT

modelongnames = ['Accumulation','Aitken','Coarse','Primary Carbon']
modenumbers = ['1','2','3','4']

for modenumber in modenumbers:
    modelongname = modelongnames[int(modenumber) - 1] 
    idx = []
    for i in range(len(num_names)):
        tempnum = list(num_names[i])
        try:
            tempnum.index(modenumber)
            idx.append(i)
        except:
            pass
    num_sum = deepcopy(empty_array)

    for i in idx: #add modes together (lat/lon/time pointwise)
        num_sum+=nc.variables[num_names[i]][:,0,:,:]

    ##Calculate moist density
    # Vapor pressure
    vapor_pressure = deepcopy(empty_array)
    vapor_pressure = nc.variables['Q'][:,0,:,:]/(nc.variables['Q'][:,0,:,:]+0.622) * nc.variables['PS'][:] 
    # Moist air density [kg/m3]
    moist_density = deepcopy(empty_array)
    moist_density = (nc.variables['PS'][:] - vapor_pressure)/(287.0531 * nc.variables['T'][:,0,:,:]) + vapor_pressure/(461.4964 * nc.variables['T'][:,0,:,:])

    #multiply concentration by moist density to reach aerosol conc per m^3 
        #(lat/lon/time pointwise still)
    num_sum_vol = num_sum * moist_density

    #take average of months (end up with lat/lon array, size 1 in time dimension)
    num_sum_vol_avg = np.sum(num_sum_vol,axis=0)/12.

    ##plot

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()

    cs = plt.contourf(lon[:],lat[:],num_sum_vol_avg) 

    cbar = plt.colorbar(cs, ax=ax, orientation='horizontal')
    cbar.set_label('Total species number per cubic meter')

    plt.title("Global ANN avg Aerosol Concentration: Mode " + modenumber)
    plt.suptitle(modelongname)

    plt.savefig('ann_mode'+modelongname+'.png',type='png')
    plt.close()
