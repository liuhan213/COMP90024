
import json
import re
import time
from pprint import pprint
from mpi4py import MPI
import numpy as np

start_time =  time.time()


size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()


# post count of each gird, row, and column
coords_list = []
melbGrid_list = []
row_list = [{'id':"A_Row",'count':0},{'id':"B_Row",'count':0},{'id':"C_Row",'count':0},{'id':"D_Row",'count':0}]
column_list = [{'id':"column_1",'count':0},{'id':"column_2",'count':0},{'id':"column_3",'count':0},{'id':"column_4",'count':0},{'id':"column_5",'count':0}]


# function  get_grids_list
def get_grids_list(grid_file_address):
    with open(grid_file_address) as f:
        files_grid = json.load(f)
        for feature in files_grid['features']:
            grid_one = {}
            grid_one['id'] = str(feature['properties']['id'])
            grid_one['xmin']  = feature['properties']['xmin']
            grid_one['xmax'] = feature['properties']['xmax']
            grid_one['ymin'] = feature['properties']['ymin']
            grid_one['ymax']  = feature['properties']['ymax']
            grid_one['count'] = 0
            melbGrid_list.append(grid_one)
    return melbGrid_list

#  get_coords_list
def get_coords_list(ins_json_address):
#    files_ins = json.load(open(ins_json_address))
    if size < 2 and rank == 0:
        with open(ins_json_address) as f:

            for line in f:
                try:
                    coord_one = {}
                    line_new = json.loads(line[0:len(line)-2])
                    coord_one['x'] = line_new['doc']['coordinates']['coordinates'][1]
                    coord_one['y'] = line_new['doc']['coordinates']['coordinates'][0]
                    coords_list.append(coord_one)
                except:
                    continue
#        return coords_list

    elif rank==0:
        with open(ins_json_address) as f:
            for line in f:
                try:
                    coord_one = {}
                    line_new = json.loads(line[0:len(line)-2])
                    coord_one['x'] = line_new['doc']['coordinates']['coordinates'][1]
                    coord_one['y'] = line_new['doc']['coordinates']['coordinates'][0]
                    coords_list.append(coord_one)
                except:
                    continue
#        return coords_list
        coords_list = np.array_split(coords_list, size)

    else:
        coords_list = None





# funciton of count_coords_grids
def count_coords_grids(grid_list,coord_list):
    if size < 2 and rank == 0:
        for coord in coord_list:
            coord_x = coord['x']
            coord_y = coord['y']
            for grid in grid_list:
                if (grid['xmin'] <= coord_x < grid['xmax'] and grid['ymin'] <= coord_y <  grid['ymax']):
                    grid['count'] += 1
        return grid_list
    else:
        coords_list = comm.scatter(coords, root = 0)

        for coord in coords_list:
            coord_x = coord['x']
            coord_y = coord['y']
            for grid in grid_list:
                if (grid['xmin'] <= coord_x < grid['xmax'] and grid['ymin'] <= coord_y <  grid['ymax']):
                    grid['count'] += 1
        return grid_list




# function count_rows
def count_rows():
    for grid in melbGrid_list:
        if grid['id'].startswith('A'):
#        if re.match('A\d',grid['id']):
            row_list[0]['count'] += grid['count']
#        elif re.match('B\d',grid['id']):
        elif grid['id'].startswith('B'):
            row_list[1]['count'] += grid['count']
#        elif re.match('C\d',grid['id']):
        elif grid['id'].startswith('C'):
            row_list[2]['count'] += grid['count']
        else:
            row_list[3]['count'] += grid['count']

    return row_list


# function count_columns
def count_columns():

    for grid in melbGrid_list:
        if grid['id'].endswith('1'):
#        if re.match('\w1',grid['id']):
            column_list[0]['count'] += grid['count']
#        elif re.match('\w2',grid['id']):
        elif grid['id'].endswith('2'):
            column_list[1]['count'] += grid['count']
#        elif re.match('\w3',grid['id']):
        elif grid['id'].endswith('3'):
            column_list[2]['count'] += grid['count']
#        elif re.match('\w4',grid['id']):
        elif grid['id'].endswith('4'):
            column_list[3]['count'] += grid['count']
        else:
            column_list[4]['count'] += grid['count']

    return column_list


# function rank_by_count
def rank_by_count(elem):
    return elem['count']


def rank_grid():

    melbGrid_list.sort(key = rank_by_count,reverse = True)
    print('posts per grid: ------------------------------ ')
    for i in melbGrid_list:
        pprint('{}: {} posts'.format(i['id'],i['count']))



def rank_row():

    row_list.sort(key = rank_by_count, reverse = True)

    print('posts per row: ------------------------------ ')
    for i in row_list:
        pprint('{}: {} posts'.format(i['id'],i['count']))



def rank_column():

    column_list.sort(key = rank_by_count,reverse = True)

    print('posts per column: ------------------------------ ')
    for i in column_list:
        pprint('{}: {} posts'.format(i['id'],i['count']))



# call function
get_grids_list('melbGrid.json')
get_coords_list('tinyInstagram1.json')
count_coords_grids(melbGrid_list,coords_list)
count_rows()
count_columns()
rank_grid()
rank_row()
rank_column()



# print the total time it takes
total_minutes = time.time() - start_time
minutes, seconds = divmod(total_minutes, 60)
print("\n Total time used for execution is %02d minutes and %02d seconds" %(minutes, seconds))
