def shellSort(board):
    h = 1
    while h < board.length/9:
        h = 3*h+1
    while h>0:
        for i in range(h,board.length):
            v = board.columns[i]
            j = i
            while j>=h and board.columns[j-h]>v:
                board.swap(j,j-h)
                j -= h
                yield True
        h //= 3