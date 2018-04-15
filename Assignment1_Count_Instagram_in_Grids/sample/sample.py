from mpi4py import MPI
import json
import numpy as np

comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

comm.Barrier()

FINAL_RESULT =[]

#Parent process
if (comm_rank == 0):
    print "There are %d cores" % comm_size
    with open('tinyTwitter.json','r') as f:
        coor = json.load(f)

    with open('melbGrid.json','r') as g:
        grid = json.load(g)


    ## Broadcast the coordinate
    Coordinate = []
    ## Loop through each item
    n = len(coor)
    for i in range(0,n):
        ##Determine which grid the item is sent from
        y = coor[i]['json']['geo']['coordinates'][0] ## latitude
        x = coor[i]['json']['geo']['coordinates'][1] ## longtitude
        Coordinate.append([x,y])
    local_Coordinate = np.array(Coordinate)



    local_Grid_Info = [] ## A List to store the grid information

    ##Extrating the boundary coordinates of each grid
    size = len(grid['features'])
    for i in range(0,size):
        Grid_dict = {}
        Grid_id = grid['features'][i]['properties']['id']
        xmin = grid['features'][i]['properties']['xmin']
        xmax = grid['features'][i]['properties']['xmax']
        ymin = grid['features'][i]['properties']['ymin']
        ymax = grid['features'][i]['properties']['ymax']
        Grid_dict[Grid_id]={'xmin': xmin ,'xmax' : xmax , 'ymin': ymin , 'ymax' : ymax} ## [ {A1:{'xmin':...}},A2:{'xmin'},...]
        local_Grid_Info.append(Grid_dict)
    local_Grid_Info = np.array(local_Grid_Info)


#Broadcast the data to slaves
local_Coordinate = comm.bcast(local_Coordinate if comm_rank ==0 else None,root = 0)
local_grid = comm.bcast(local_Grid_Info if comm_rank == 0 else None,root = 0)



#child process
if(comm_rank > 0):
#print local_Coordinate
    ## The result table
    local_Result = {}

    ## Initialize the result dictionary
    for i in local_grid:
        for grid_id in i:
            local_Result[grid_id] = 0
    local_Result['A-Row'] = 0
    local_Result['B-Row'] = 0
    local_Result['C-Row'] = 0
    local_Result['D-Row'] = 0
    local_Result['Col-1'] = 0
    local_Result['Col-2'] = 0
    local_Result['Col-3'] = 0
    local_Result['Col-4'] = 0
    local_Result['Col-5'] = 0

##    print local_Result

    #Evenly split the input coordinate to different processes based on their rank
    start = (comm_rank - 1)*len(local_Coordinate)/(comm_size-1)
    end = (comm_rank)*len(local_Coordinate)/(comm_size-1)



    for i in range(start,end):
        x = local_Coordinate[i][0]
        y = local_Coordinate[i][1]

        #Determine the location of the point
        for one_grid in local_grid:  #index in a list to fetch a dic
            for (k,v) in one_grid.items(): # a dictionary
            # Single  Grid Calculation
                if(y >= v['ymin'] and y <= v['ymax'] and
                   x >= v['xmin'] and x <= v['xmax']):
                    ## Append to the local_Result dictionary
                    local_Result[k] = local_Result[k] + 1
                    break;

    local_Result['A-Row'] = local_Result['A1']+local_Result['A2']+local_Result['A3']+local_Result['A4']
    local_Result['B-Row'] = local_Result['B1']+local_Result['B2']+local_Result['B3']+local_Result['B4']
    local_Result['C-Row'] = local_Result['C1']+local_Result['C2']+local_Result['C3']+local_Result['C4']+local_Result['C4']
    local_Result['D-Row'] = local_Result['D3']+local_Result['D4']+ local_Result['D5']
    local_Result['Col-1'] = local_Result['A1'] + local_Result['B1'] + local_Result['C1']
    local_Result['Col-2'] = local_Result['A2'] + local_Result['B2'] + local_Result['C2']
    local_Result['Col-3'] = local_Result['A3'] + local_Result['B3'] + local_Result['C3'] + local_Result['D3']
    local_Result['Col-4'] = local_Result['A4'] + local_Result['B4'] + local_Result['C4'] + local_Result['D4']
    local_Result['Col-5'] = local_Result['C5'] + local_Result['D5']
    print local_Result
    r = [k for (v,k) in local_Result.items()]
    r = np.asarray(r)
    print r
    comm.Reduce(r, FINAL_RESULT, op=MPI.SUM, root = 0)

comm.Barrier()
print FINAL_RESULT




##
##for key in Result:
##    print key +":" + str(Result[key])
##
##if (comm_rank == 0):
##    exit(0)
