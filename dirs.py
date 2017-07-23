# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:50:05 2017

@author: kkrao
"""

from __future__ import division
#from IPython import get_ipython
#get_ipython().magic('reset -sf') 

import numpy as np
import pandas as pd
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy.ma as ma
import scipy.io
import os
import arcpy
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
from arcpy.sa import *
import pylab
import h5py
import urllib
import urllib2
from ftplib import FTP 
from subprocess import Popen, PIPE
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pylab
from matplotlib.patches import Rectangle  
import seaborn as sns
from sklearn import datasets, linear_model


    
MyDir = 'D:/Krishna/Project/data/RS_data'  #Type the path to your data
Dir_CA='D:/Krishna/Project/data/Mort_Data/CA'
Dir_fig='D:/Krishna/Project/figures'
Dir_mort='D:/Krishna/Project/data/Mort_Data/CA_Mortality_Data'
Dir_NLDAS=MyDir+'/NLDAS'

def ind(thresh,mort):
    ind=[l for l in mort.columns if mort.loc['2016-01-01',l] >=thresh]
    return ind

def box_equal_nos(x,y,boxes):
    x=x.values.flatten()
    y=y.values.flatten()
    inds=x.argsort()
    x=x[inds]
    y=y[inds]
    inds=np.argwhere(~np.isnan(x))
    x=x[inds]
    y=y[inds]
    count=len(x)/boxes
    count=np.ceil(count).astype(int)
    yb=pd.DataFrame()
    for i in range(boxes):
        data=y[i*count:(i+1)*count]
        name=np.mean(x[i*count:(i+1)*count]).round(2)
        data=pd.DataFrame(data,columns=[name])
        yb=pd.concat([yb,data],axis=1)
    return yb

def min_anomaly(Df):
    mean=Df.groupby(Df.index.dayofyear).mean()
    sd=Df.groupby(Df.index.dayofyear).std()
    Df_min_anomaly=pd.DataFrame()
    for year in np.unique(Df.index.year):
        a=Df[Df.index.year==year]
        a.index=a.index.dayofyear
        min_anomaly=((a-mean)/sd).min()
        min_anomaly.name=pd.Timestamp(year,1,1)
        Df_min_anomaly=pd.concat([Df_min_anomaly,min_anomaly],1)
    Df_min_anomaly=Df_min_anomaly.T
    return Df_min_anomaly

def add_squares(axes, x_array, y_array, size=0.5, **kwargs):
    size = float(size)
    for x, y in zip(x_array, y_array):
        square = pylab.Rectangle((x-size/2,y-size/2), size, size, **kwargs)
        axes.add_patch(square)
    return True

def get_marker_size(ax,fig,loncorners,grid_size,marker_factor):
    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    width, height = bbox.width, bbox.height
    width *= fig.dpi
    marker_size=width*grid_size/100/np.diff(loncorners)[0]/4*marker_factor
    return marker_size


def median_anomaly(Df):
    mean=Df.groupby(Df.index.dayofyear).mean()
    sd=Df.groupby(Df.index.dayofyear).std()
    Df_anomaly=pd.DataFrame()
    for year in np.unique(Df.index.year):
        a=Df[Df.index.year==year]
        a.index=a.index.dayofyear
        anomaly=((a-mean)/sd).median()
        anomaly.name=pd.Timestamp(year,1,1)
        Df_anomaly=pd.concat([Df_anomaly,anomaly],1)
    Df_anomaly=Df_anomaly.T
    return Df_anomaly    



