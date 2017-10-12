# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 18:32:07 2017

@author: kkrao
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dirs import Dir_CA
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
from sklearn import tree
def rf_assemble(year_range,*dfs):
    if len(dfs)==1:
        dfs=[dfs]
#    df=store['cwd']
#    dfs[0]=df
    out=pd.DataFrame(index=range(dfs[0].shape[1]*(year_range[-1]-year_range[0]+1)))
    for df in dfs:                    
        df=df[(df.index.year>=year_range[0]) &\
                  (df.index.year<=year_range[-1])].T
        array=pd.Series(df.values.flatten(),name=df.columns.name)
        out[array.name]=array
    return(out)

def rf_fill(df):
    df.fillna(method='ffill',inplace=True)
    df.fillna(method='bfill',inplace=True)
    return df

input_sources=['mortality_025_grid','BPH_025_grid','LAI_025_grid_sum',\
'LAI_025_grid_win','RWC', 'aspect_mean', 'aspect_std', 'canopy_height',\
 'cwd','dominant_leaf_habit','elevation_mean','elevation_std',\
 'forest_cover','ppt_sum','ppt_win','tmax_sum','tmax_win',\
 'tmean_sum','tmean_win','vpdmax_sum','vpdmax_win','EVP_sum',\
'PEVAP_sum','EVP_win','PEVAP_win','vsm_sum','vsm_win']
year_range=range(2009,2016)
#input_sources=['mortality_025_grid','LAI_025_grid_sum',\
#'LAI_025_grid_win','RWC', 'aspect_mean', 'aspect_std', 'canopy_height',\
# 'dominant_leaf_habit','elevation_mean','elevation_std',\
# 'forest_cover','ppt_sum','ppt_win','tmax_sum','tmax_win',\
# 'tmean_sum','tmean_win','vpdmax_sum','vpdmax_win','EVP_sum',\
#'PEVAP_sum','EVP_win','PEVAP_win','vsm_sum','vsm_win']
#year_range=range(2005,2016)

os.chdir(Dir_CA)
store=pd.HDFStore(Dir_CA+'/data.h5')
inputs=range(len(input_sources))
for i in range(len(input_sources)):
    inputs[i]=store[input_sources[i]]
Df=rf_assemble(year_range,*inputs)
Df['missing_data']=Df.T.isnull().sum()
Df.loc[Df['missing_data']>=1,'missing_data']='yes'
#Df.loc[Df['missing_data']==1,'missing_data']='yes'
Df.loc[Df['missing_data']==0,'missing_data']='no'
#-----------------------------------------------------------------------------
Null=Df[['RWC','cwd','vsm_sum','vsm_win']]
Null=Null.isnull()
Null.replace(True,np.nan,inplace=True)
for column in Null.columns:
    Null[column].replace(0.0,Null.columns.get_loc(column),inplace=True)
Null['union']=Null.notnull().T.sum()
Null.union[Null.overall!=4]=np.nan
Null.union[Null.overall==4]=4
fig,ax=plt.subplots(figsize=(6,3))
Null.plot(linestyle='',marker='|',mew='0.1',markersize=10,ax=ax,legend=False,color='darkblue')
#plt.tick_params(axis='y', which='major', labelsize=7)
#ax.set_xlabel('Fraction of Nulls')
ax.set_ylabel('Features')
ax.set_title('Data Availability')
plt.yticks(range(len(Null.columns)),Null.columns)
labels=range(2009,2016)
plt.xticks(np.linspace(0,len(Null.index),len(labels),endpoint=False),labels)


Null.overall.replace(False,np.nan,inplace=True)
Null_frac=(Null.missing_data==0).astype(int).mean()
print('Union of Nulls = %0.2f'%Null_frac)
#-----------------------------------------------------------------------------
#Df=rf_fill(Df)
#Df.to_csv('D:/Krishna/Project/data/rf_data.csv')
