import numpy as np

#inp = [5,3,0,0,7,0,0,0,0,6,0,0,1,9,5,0,0,0,0,9,8,0,0,0,0,6,0,8,0,0,0,6,0,0,0,3,4,0,0,8,0,3,0,0,1,7,0,0,0,2,0,0,0,6,0,6,0,0,0,0,2,8,0,0,0,0,4,1,9,0,0,5,0,0,0,0,8,0,0,7,9]
#inp = [3, 0, 2, 0, 7, 1, 0, 0, 5, 8, 0, 6, 0, 3, 0, 2, 0, 0, 7, 5, 0, 0, 4, 0, 0, 0, 0, 0, 7, 0, 4, 0, 8, 0, 0, 2, 0, 0, 3, 7, 0, 2, 8, 0, 0, 2, 0, 0, 6, 0, 3, 0, 4, 0, 0, 0, 0, 0, 8, 0, 0, 6, 7, 0, 0, 8, 0, 2, 0, 4, 0, 1, 1, 0, 0, 5, 6, 0, 9, 0, 8]
def which_box(row_ind, column_ind):
    if row_ind == 0 or row_ind == 1 or row_ind == 2:
        if column_ind == 0 or column_ind == 1 or column_ind == 2:
            return 'box1'
        elif column_ind == 3 or column_ind == 4 or column_ind == 5:
            return 'box2'
        elif column_ind == 6 or column_ind == 7 or column_ind == 8:
            return 'box3'

    elif row_ind == 3 or row_ind == 4 or row_ind == 5:
        if column_ind == 0 or column_ind == 1 or column_ind == 2:
            return 'box4'
        elif column_ind == 3 or column_ind == 4 or column_ind == 5:
            return 'box5'
        elif column_ind == 6 or column_ind == 7 or column_ind == 8:
            return 'box6'

    elif row_ind == 6 or row_ind == 7 or row_ind == 8:
        if column_ind == 0 or column_ind == 1 or column_ind == 2:
            return 'box7'
        elif column_ind == 3 or column_ind == 4 or column_ind == 5:
            return 'box8'
        elif column_ind == 6 or column_ind == 7 or column_ind == 8:
            return 'box9'

def check_in_box(a,b,c,d,elem):
    for i in range(a,b):
        for j in range(c,d):
            if elem == inp[i,j]:
                temp = True
                return temp
            else:
                temp = False
    return temp

def check_box(box,elem):
    if box == 'box1':
        return check_in_box(0,3,0,3,elem)
    if box == 'box2':
        return check_in_box(0,3,3,6,elem)
    if box == 'box3':
        return check_in_box(0,3,6,9,elem)
    if box == 'box4':
        return check_in_box(3,6,0,3,elem)
    if box == 'box5':
        return check_in_box(3,6,3,6,elem)
    if box == 'box6':
        return check_in_box(3,6,6,9,elem)
    if box == 'box7':
        return check_in_box(6,9,0,3,elem)
    if box == 'box8':
        return check_in_box(6,9,3,6,elem)
    if box == 'box9':
        return check_in_box(6,9,6,9,elem)


def search_and_update(row,index,label):
    missing = []
    update = False
    for i in range(1,10):
        if i not in row:
            missing.append(i)
    for i in missing:
        Possible_indices = [h for h,e in enumerate(row) if e == 0]
        iterate = Possible_indices[:]
        pop_count = 0
        for ind, j in enumerate(iterate):
            if label == 'row':
                box = which_box(index,j)
            if label == 'col':
                box = which_box(j,index)
            in_box = check_box(box,i)
            if in_box:
                Possible_indices.pop(ind - pop_count)
                pop_count = pop_count+1
                continue
            if label == 'row':
                if i in inp[:,j]:
                    Possible_indices.pop(ind - pop_count)
                    pop_count = pop_count+1
                    continue
            if label == 'col':
                if i in inp[j,:]:
                    Possible_indices.pop(ind - pop_count)
                    pop_count = pop_count+1
                    continue
        if len(Possible_indices) == 1:
            if label == 'row':
                inp[index,Possible_indices[0]] = i
            if label == 'col':
                inp[Possible_indices[0],index] = i
            update = True
    return update

def sudoku_solve(inpu):

    global inp
    inp=inpu

    if len(inp) != 81:
        exit(0)

    inp = np.reshape(inp,(9,9))
    #print inp
    done = 0
    condition = 0
    update = False
    first = True

    for m in range(0,100):
    #while not(done):
        row_count = []
        column_count = []
        for i in range(0,9):
            row_count.append(np.count_nonzero(inp[i,:]))
            column_count.append(np.count_nonzero(inp[:,i]))
        #print row_count
        #print column_count

        if update or first:
            row_max = max(row_count)
            col_max = max(column_count)
            if row_max >= col_max:
                index = row_count.index(row_max)
                row = inp[index,:]
                update = search_and_update(row,index,'row')
            else:
                index = column_count.index(col_max)
                col = inp[:,index]
                update = search_and_update(col,index,'col')

        if not(update or first):
            for index, i in enumerate(row_count):
                row = inp[index,:]
                update = search_and_update(row,index,'row')
                if update:
                    break

        if not(update or first):
            for index, i in enumerate(column_count):
                col = inp[:,index]
                update = search_and_update(col,index,'col')
                if update:
                    break

        if np.count_nonzero(inp) == 81:
            done = 1

        check = True
        for i in range(0,9):
            for j in range(1,10):
                if j not in inp[i,:]:
                    check = True and False

        condition = check
        #print condition

        first = False

    print inp
    print done
    print condition
    out=[val for sublist in inp for val in sublist]
    return out
