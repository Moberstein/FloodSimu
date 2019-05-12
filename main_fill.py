#%%
import time
import geopandas
import pandas
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt

#%%
building = geopandas.read_file("./gis_osm_buildings.shp");
xyzdata = pandas.read_csv("./smallxyz2.csv", header=None);
#print(building.head())
#print(xyzdata.head())

#%%
xyzdata['coordinates'] = list(zip(xyzdata[0], xyzdata[1]))
xyzdata.coordinates = xyzdata.coordinates.apply(Point)
xyzdata['height'] = list(xyzdata[2])
xyzdata['x'] = list(xyzdata[0])
xyzdata['y'] = list(xyzdata[1])
#print(xyzdata)

#%%y
points = geopandas.GeoDataFrame(xyzdata, geometry='coordinates')
points.crs = building.crs
#print(points.head())
#print(building.head())

#sjoin = geopandas.sjoin(points, building, how='inner')
#print(sjoin.head())
#print(building.head());
#building = building.loc[building['type'] == 'church'];
#%%

#sjoin.plot(column='height', legend=True)
threshold = 0
ax = building.plot(color='red');

drawpoints = points.loc[(points['height']<threshold)]
# find lowest points
while drawpoints.empty:
    drawpoints = points.loc[(points['height']<threshold)]
    threshold = threshold + 1

drawpoints.plot(ax=ax, color='blue', alpha=0.2, markersize=6)

while threshold < 200:  
    
    threshold = threshold + 1
    print(threshold)

    plt.pause(1)

    drawpoints_new = points.loc[(points['height']<threshold) & (points['height'] >= threshold - 1)]
    drawpoints_new.plot(ax=ax, column="height", alpha=0.15, markersize=6)

plt.show()
