#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as cl
import time

#%% Sample river data
river_points = pd.DataFrame()
river_points = river_points.append([[0,0,0],[1,0,1],[0,1,1],[1,1,1]])

#%% Sample data
data_points = pd.DataFrame()
data_points = data_points.append([[0,0,0],[1,0,1],[2,0,2],[3,0,3]])
data_points = data_points.append([[0,1,1],[1,1,1],[2,1,2],[3,1,4]])
data_points = data_points.append([[0,2,0],[1,2,1],[2,2,1],[3,2,4]])
data_points = data_points.append([[0,3,0],[1,3,1],[2,3,2],[3,3,7]])

#%%
def findNeighbours(current_data_point, leveled_data_points):
    current_data_point_x = current_data_point[1]
    current_data_point_y = current_data_point[2]

    #print(current_data_point)
    #print(current_data_point_x)
    #print(current_data_point_y)
    #print(leveled_data_points.dtypes)

    return leveled_data_points[(leveled_data_points[0] <= current_data_point_x + 6) & (leveled_data_points[0] >= current_data_point_x - 6) & (leveled_data_points[1] <= current_data_point_y + 6) & (leveled_data_points[1] >= current_data_point_y - 6)]

#%%
def step(current_data_points, data_points, height):
    next_data_points = pd.DataFrame()

    for current_data_point in current_data_points.itertuples():

        #print("-> Neighours for %s:" % str(current_data_point))
        neighbours = findNeighbours(current_data_point, data_points)
        flooded_neighbours = neighbours[neighbours[2] <= height]
        neighbours_flooded = len(neighbours) == len(flooded_neighbours)

        if(neighbours_flooded):
            #print("!> Dropping from data")
            #print('!> %d before drop' % len(data_points))
            data_points = data_points.loc[~((data_points[0] == current_data_point[1]) & (data_points[1] == current_data_point[2]))]
            #print('!> %d left' % len(data_points))

            #print("!> Dropping from neighbours")
            #print('!> %d before drop' % len(neighbours))
            neighbours = neighbours.loc[~((neighbours[0] == current_data_point[1]) & (neighbours[1] == current_data_point[2]))]
            #print('!> %d left' % len(neighbours))

        for leveled_data_point in neighbours.itertuples():
            #print(leveled_data_point)
            next_data_points = next_data_points.append([[leveled_data_point[1], leveled_data_point[2], leveled_data_point[3], leveled_data_point[3] <= height]])

        #print("--> %d Neighbours" % len(neighbours))
        #print("    %s" % neighbours)
        #print('-----   -----')

    if len(next_data_points) > 1:
        next_data_points = next_data_points.drop_duplicates()
    print("> %d Unique neighbours" % len(next_data_points))


    return (next_data_points, data_points)

#%%
def scatterplot(data_points):
    for d in data_points.itertuples():
        plt.scatter(d[1], d[2], c=d[3], norm=cl.Normalize(min_height, max_height))
    plt.show()

#%% Config  for sample data
#current_data_points = river_points
#available_data_points = data_points
#color_data_points = river_points
#min_height = data_points.min()[2]
#print(min_height)
#max_height = data_points.max()[2]
#print(max_height)

#%% Config for real data
available_data_points = pd.read_csv('dom1l-fp_32356_5645_1_nw_reduced.xyz', header=None)
river_points = pd.read_csv('river_cleansed.csv', header=None)
current_data_points = river_points
color_data_points = river_points

min_height = int(available_data_points.min()[2])
print(min_height)
max_height = int(available_data_points.max()[2])
print(max_height)


#%%

for i in range(min_height + 2, max_height + 1, 5):
    scatterplot(color_data_points)
    for j in range(0, 1, 1):
        print('+> %d' % len(color_data_points))

        #print(available_data_points)
        print('#############')
        print('Iteration %d/%d' % (i,j))
        current_data_points, available_data_points = step(current_data_points, available_data_points, i)

        if len(current_data_points) > 0:
            color_data_points = color_data_points.append([current_data_points])
            color_data_points = color_data_points.drop_duplicates()
            #print(current_data_points)

scatterplot(color_data_points)

#%%
#step(current_data_points, available_data_points, min_height)

#%%
