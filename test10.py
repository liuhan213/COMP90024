
import json
import re
import time
from pprint import pprint
from mpi4py import MPI
import numpy as np




comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()



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



#  get_coords_list into the list coords_list
def get_coords_list(ins_json_address):
    with open(ins_json_address) as f:
        coords_list = []
        for line in f:
            try:
                coord_one = {}
                line_new = json.loads(line[0:len(line)-2])
                coord_one['x'] = line_new['doc']['coordinates']['coordinates'][1]
                coord_one['y'] = line_new['doc']['coordinates']['coordinates'][0]
                coords_list.append(coord_one)
            except:
                continue
    return(coords_list)


def get_chunks(big_chunk,count):
    small_chunks = [big_chunk[i::size] for i in range(count)]

    return small_chunks




def count_coords_grids(melb_grid, coord):
    x = coord['x']
    y = coord['y']
    for grid_data in melb_grid:
        if (y >= grid_data["ymin"] and y <= grid_data["ymax"]) and (x >= grid_data["xmin"] and x <= grid_data["xmax"]):
            grid_data["count"] = grid_data["count"] + 1



# function count_rows
def count_rows(grid_list,row_list):
    for grid in grid_list:
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
def count_columns(grid_list,column_list):
# melbGrid_list
    for grid in grid_list:
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



if rank==0:
    start_time = time.time()
    print('start_time:',start_time)
    coord_list = []
    row_list = [{'id':"A_Row",'count':0},{'id':"B_Row",'count':0},{'id':"C_Row",'count':0},{'id':"D_Row",'count':0}]
    column_list = [{'id':"column_1",'count':0},{'id':"column_2",'count':0},{'id':"column_3",'count':0},{'id':"column_4",'count':0},{'id':"column_5",'count':0}]

    # post count of each gird, row, and column

    # get big chunk

    coord_list = get_coords_list('tinyInstagram1.json')
#    coord_list_in_chunks = get_chunks(coord_list,size)
    coord_list_in_chunk = np.array_split(coord_list, size)


else:
    coord_list_in_chunk = None

melbGrid_list = []
melbGrid_list = get_grids_list('melbGrid.json')
coord_list_in_chunk = comm.scatter(coord_list_in_chunk, root=0)

#for coord in coord_list_in_chunk:
#    count_coords_grids(melbGrid_list,coord)

for coord in coord_list_in_chunk:
    count_coords_grids(melbGrid_list, coord)

# Gather all of results from child process
result = comm.gather(melbGrid_list)

#print('result--------')
#print('rank :',rank, ':', result,'type:',type(result),'length:',len(result))





if rank== 0:
#    print('result--------')
#    print(result)

    for grid in melbGrid_list:
        for chunk in result:
            for coord in chunk:
               if coord['id'] == grid['id']:
                   grid['count'] = grid['count']+coord['count']
    print(melbGrid_list)

    count_rows(melbGrid_list,row_list)
    count_columns(melbGrid_list,column_list)

    rank_grid()
    rank_row()
    rank_column()

    print('endtime:',time.time())
    total_minutes = time.time() - start_time
    minutes, seconds = divmod(total_minutes, 60)
    print("\nTotal time used for execution is %02d minutes and %02d seconds" %
          (minutes, seconds))
