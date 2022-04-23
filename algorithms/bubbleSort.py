def bubbleSort(board):
    for i in range(board.length-1,0,-1):
        for j in range(1,i+1):
            if board.columns[j]<board.columns[j-1]:
                board.swap(j,j-1)
            yield True