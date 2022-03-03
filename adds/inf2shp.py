#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Title: 
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de



Created on Fri Sep  4 22:44:43 2020
@author: @author: Giacomo Nodjoumi g.nodjoumi@jacobs-unversity.de
"""

import pandas as pd
import geopandas as gpd
from pyproj import CRS
import shutil
from adds.GenUtils import get_paths
import pathlib
from shapely.geometry import Point
import rasterio as rio
import os
# CLON2 = pyproj.CRS.from_user_input('PROJCS["Equirectangular MARS",GEOGCS["GCS_MARS",DATUM["unnamed",SPHEROID["unnamed",3396190,0]],PRIMEM["Reference meridian",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Equirectangular"],PARAMETER["standard_parallel_1",0],PARAMETER["central_meridian",180],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]')
# mars_sphere = CRS.from_proj4('+proj=longlat +R=3396190 +no_defs +type=crs')
# marsUTM = CRS.from_proj4('+proj=tmerc +lat_0=0 +lon_0=0 +k=0.9996 +x_0=0 +y_0=0 +a=3396190 +b=3376200 +units=m +no_defs')
# marsEqui = CRS.from_user_input('PROJCS["Mars_Equidistant_Cylindrical",GEOGCS["Mars 2000",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.89444722361179]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",0],PARAMETER["Standard_Parallel_1",0],UNIT["Meter",1]]')
# mars_EQUI = CRS.from_user_input('PROJCS["Equirectangular MARS",GEOGCS["GCS_MARS",DATUM["unnamed",SPHEROID["unnamed",3395582.0270805,0]],PRIMEM["Reference meridian",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Equirectangular"],PARAMETER["latitude_of_origin",-10],PARAMETER["central_meridian",180],PARAMETER["standard_parallel_1",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]')
# marsPLANCE = CRS.from_user_input('GEOGCS["Mars 2000 planetocentric",DATUM["D_Mars_2000",SPHEROID["Mars_2000_IAU_IAG",3396190.0,169.89444722361179]],PRIMEM["AIRY-0",180],UNIT["Degree",0.017453292519943295]]')
# # from shapely.geometry import Point
#EQUI = CRS.from_user_input('PROJCS["Equirectangular MARS",GEOGCS["GCS_MARS",DATUM["unnamed",SPHEROID["unnamed",3396190,0]],PRIMEM["Reference meridian",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]]],PROJECTION["Equirectangular"],PARAMETER["standard_parallel_1",0],PARAMETER["central_meridian",180],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH]]')
EQUI= CRS.from_wkt('PROJCRS["Equirectangular MARS",BASEGEOGCRS["GCS_MARS",DATUM["unnamed",ELLIPSOID["unnamed",3396036.8126024,0,LENGTHUNIT["metre",1,ID["EPSG",9001]]]],PRIMEM["Reference meridian",0,ANGLEUNIT["degree",0.0174532925199433,ID["EPSG",9122]]]],CONVERSION["unnamed",METHOD["Equidistant Cylindrical (Spherical)",ID["EPSG",1029]],PARAMETER["Latitude of 1st standard parallel",-5,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8823]],PARAMETER["Longitude of natural origin",180,ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8802]],PARAMETER["False easting",0,LENGTHUNIT["metre",1],ID["EPSG",8806]],PARAMETER["False northing",0,LENGTHUNIT["metre",1],ID["EPSG",8807]]],CS[Cartesian,2],AXIS["easting",east,ORDER[1],LENGTHUNIT["metre",1,ID["EPSG",9001]]],AXIS["northing",north,ORDER[2],LENGTHUNIT["metre",1,ID["EPSG",9001]]]]')

def get_world_file(ext):
    if ext in ['TIFF','tiff']:
        ixt = 'tiff'
        world_file = '.tfw'
    if ext in ['PNG','png']:
        ixt = 'png'
        world_file = '.pgw'
    if ext in ['JPG','jpg']:
        ixt = ' jpg'
        world_file = '.jgw'    
    return(ixt, world_file)


def getAffine(world_file):
    with open(world_file, 'r'):
        t = [line.rstrip('\n') for line in open(world_file)]
        t = [float(i) for i in t]
        gt = (t[4],t[0],t[1],t[5],t[2],t[3])
    from affine import Affine
    aff = Affine.from_gdal(*gt)
    return(aff)


def det2gdf(detections_paths, ixt, source):   
    geodataframes = []
    cols = ['Cls', 'x','y','w','h','Conf']
    for file in detections_paths:

        name= pathlib.Path(file).name.split('.txt')[0]
        basename=os.path.basename(file).split('.txt')[0]
        image = basename + '.'+ixt
        usc = [x for x in range(len(cols))]
        df = pd.read_csv(file, delimiter=' ',header=None, usecols=usc, names=cols, dtype='float64')
        df.insert(0, 'Name', basename)
        src_image = source+image
        #print(src_image)
        img = rio.open(src_image)
        aff = img.transform
        width = img.width
        height = img.height
        src_crs = img.crs.to_wkt()
        cords = []
        for i in range(df.shape[0]):
            pX=df['x'].iloc[i]
            pY=df['y'].iloc[i]
            pXw=pX*width
            pYw=pY*height
            col, row = pXw, pYw
            coord=aff*(col,row)
            df.at[i,'long']=coord[0]
            df.at[i,'lat']=coord[1]
            cords.append(Point(coord[0],coord[1]))
        df['Cls'] = df['Cls']+1
        geodataframes.append(gpd.GeoDataFrame(data=df, geometry=cords, crs=src_crs))
    return(geodataframes)

def df2shp(folder, df):
    newdata = gpd.GeoDataFrame(df, crs=EQUI, geometry=gpd.points_from_xy(df.long, df.lat))
    savename =folder+'/Inferred_detections_equi.shp'
    try:
        newdata.to_file(savename)
    except Exception as e:
        print(e)
    
def copyfiles(source, destination, ext):
    #for ext in extensions:
    files = get_paths(source, ext)
    try:
        for file in files:
            shutil.copy(file, destination)
    except Exception as e:
        print(e)