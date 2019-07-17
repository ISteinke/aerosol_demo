from netCDF4 import Dataset as netcdf_dataset
import numpy as np
import pandas as pd
import sys

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

def geo_idx(dd, dd_array):
    """
     search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
    ##check if input longitude in 180 fmat and convert to 360:
    if(dd_array.max()>180 and dd<0):
        dd = 360 + dd
    geo_idx = (np.abs(dd_array - dd)).argmin()
    return geo_idx

##turn to fxn
def getPointDF(dirname,filename,in_lat,in_lon,make_csv=True):
    ##open netcdf
    nc = netcdf_dataset(dirname+filename)
    ##pick a point
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]

    lat_idx = geo_idx(in_lat, lats)
    lon_idx = geo_idx(in_lon, lons)
    ##pull out variables at that point (lev1 only) for each variable (pre-defined list)
    vardf = pd.DataFrame(index=variable_names,columns=month_names)
        #dict/df: key=varname, value=12x1 array retrieved 
    ##pull out 1 layer of variable to add to df -- internal loop
    for varname in variable_names:
        var = nc[varname]
        if (len(var.shape)==3): ##2d var
            vardf.loc[varname,:] = var[:,lat_idx,lon_idx]
        elif(len(var.shape)==4): ##3d var
            vardf.loc[varname,:] = var[:,0,lat_idx,lon_idx]
    ##write to csv with newfilename
    if(make_csv):
        newfilename = dirname+filename.split(".")[0]+'_'+str(in_lat)+'_'+str(in_lon)+".csv"
        vardf.to_csv(newfilename)
    return(vardf)

dirname = sys.argv[1]
filename = sys.argv[2]
in_lat = float(sys.argv[3])
in_lon = float(sys.argv[4])


getPointDF(dirname,filename,in_lat,in_lon,make_csv=True)