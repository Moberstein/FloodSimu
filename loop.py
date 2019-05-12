#%% imports
import pandas as pd

#%% Sample river data
river_points = pd.DataFrame()
river_points = river_points.append([[0,0,0],[1,0,1],[0,1,1],[1,1,1]])

#%% Sample data
data_points = pd.DataFrame()
data_points = data_points.append([[0,0,0],[1,0,1],[2,0,2],[3,0,3]])
data_points = data_points.append([[0,1,1],[1,1,1],[2,1,2],[3,1,4]])
data_points = data_points.append([[0,2,0],[1,2,1],[2,2,1],[3,2,4]])
data_points = data_points.append([[0,3,0],[1,3,1],[2,3,2],[3,3,7]])

#%% Initial minimum height
min_height = data_points.min()[2]
print(min_height)
max_height = data_points.max()[2]
print(max_height)

#%%
def findNeighbours(current_data_point, leveled_data_points):
    current_data_point_x = current_data_point[1]
    current_data_point_y = current_data_point[2]

    return leveled_data_points[(leveled_data_points[0] <= current_data_point_x + 1) & (leveled_data_points[0] >= current_data_point_x - 1) & (leveled_data_points[1] <= current_data_point_y + 1) & (leveled_data_points[1] >= current_data_point_y - 1)]

#%%
def step(current_data_points, data_points, height):
    next_data_points = pd.DataFrame()

    for current_data_point in current_data_points.itertuples():

        neighbours = findNeighbours(current_data_point, data_points)
        neighbours = neighbours[neighbours[2] <= height]
        neighbours_flooded = len(neighbours) == len(neighbours)

        print("-> Neighours for %s:" % str(current_data_point))
        if(neighbours_flooded):
            #print("!> Dropping from data")
            #print('!> %d before drop' % len(data_points))
            data_points = data_points.loc[~((data_points[0] == current_data_point[1]) & (data_points[1] == current_data_point[2]))]
            print('!> %d left' % len(data_points))

            #print("!> Dropping from neighbours")
            #print('!> %d before drop' % len(neighbours))
            neighbours = neighbours.loc[~((neighbours[0] == current_data_point[1]) & (neighbours[1] == current_data_point[2]))]
            #print('!> %d left' % len(neighbours))

        for leveled_data_point in neighbours.itertuples():
            #print(leveled_data_point)
            next_data_points = next_data_points.append([[leveled_data_point[1], leveled_data_point[2], leveled_data_point[3]]])

        #print("--> %d Neighbours" % len(neighbours))
        #print("    %s" % neighbours)
        #print('-----   -----')

    if len(next_data_points) > 1:
        next_data_points = next_data_points.drop_duplicates()
    print("> %d Unique neighbours" % len(next_data_points))


    return (next_data_points, data_points)

#%%
current_data_points = river_points
available_data_points = data_points

for i in range(min_height + 1, max_height + 1):
    #print(available_data_points)
    print('#############')
    print('Iteration %d' % i)
    current_data_points, available_data_points = step(current_data_points, available_data_points, i)


#%%
#step(current_data_points, data_points, 1)

#%%
