import json
import re
import time
from pprint import pprint
from mpi4py import MPI


start_time =  time.time()

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


# post count of each gird, row, and column
coords_list = []
melbGrid_list = []
row_list = [{'id':"A_Row",'count':0},{'id':"B_Row",'count':0},{'id':"C_Row",'count':0},{'id':"D_Row",'count':0}]
column_list = [{'id':"column_1",'count':0},{'id':"column_2",'count':0},{'id':"column_3",'count':0},{'id':"column_4",'count':0},{'id':"column_5",'count':0}]


#def split(list, count):
#    return [list[i::count] for i in range(count)]


# get grids' coordinate information into the list melbGrid_list

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
    if rank == 0:
        with open(ins_json_address) as f:
            coords = []
            for line in f:
                try:
                    coord_one = {}
                    line_new = json.loads(line[0:len(line)-2])
                    coord_one['x'] = line_new['doc']['coordinates']['coordinates'][1]
                    coord_one['y'] = line_new['doc']['coordinates']['coordinates'][0]
                    coords.append(coord_one)
                except:
                    continue
#            chunks = [coords_list_output[i::size] for i in range(size)]

    else:
        coords = None
#    return chunks
    return(coords)



def getchunks(big_chunk,count):
    chunks = [big_chunk[i::size] for i in range(count)]
    return chunks


# funciton of count_coords_grids
def count_coords_grids(grid_list, coord_one):
#    for coord in coordinator_list:

        coord_x = coord_one['x']
        coord_y = coord_one['y']
        for grid in grid_list:
            if (grid['xmin'] <= coord_x < grid['xmax'] and grid['ymin'] <= coord_y <  grid['ymax']):
                grid['count'] += 1
#        return grid_list
#    print str(rank) + ':' + grid_list+ '\n'
#    result = comm.gather(grid_list)




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



# call function

#print('after scatter: chunk --------')
#print(chunk)
#print(len(chunk))

    #    for data in chunk:
    #        count_coords_grids(melbGrid_list,data)
#    print('get coords---------')
#    print(coords_list)

#result.append(melbGrid_list)
#    print('result count----')
#    print(len(result))

#print('result------')

#print(result)
#    print(rank, chunk_one)

#    print('this is rank',rank)
#    print('chunk_one ------')
#    print(chunk_one)

#print('after gather: chunks --------')
#print(results)
#print('this is from rank',rank)

# get big chunk
if rank==0:
    get_grids_list('melbGrid.json')

    coords_list = get_coords_list('tinyInstagram1.json')

    chunks = getchunks(coords_list,size)
else:
    chunks = None

# scatter chunk
chunk = comm.scatter(chunks,root=0)
print 'rank',rank,':after_scatter_has data:',chunk

# compute

#for chunk_one in chunk:
#    count_coords_grids(melbGrid_list,chunk_one)
#print('this is from rank',rank,':',melbGrid_list)
# gather chunk

#results = comm.gather(melbGrid_list,root = 0)
gather_chunk = comm.gather(chunk,root=0)

if rank==0:
    result = []
    print('type of newdata:',type(gather_chunk))
    print('len of newdata:',len(gather_chunk))
    for i in gather_chunk:
        for j in i:
            result.append(j)
    print 'master:',gather_chunk
    print 'result:',result



    count_rows(melbGrid_list,row_list)
    count_columns(melbGrid_list,column_list)

    rank_grid()
    rank_row()
    rank_column()


#total_minutes = time.time() - start_time
#minutes, seconds = divmod(total_minutes, 60)
#print' Total time used for execution is {} minutes and {} seconds'.format(minutes, seconds)
