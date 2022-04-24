def selectionSort(board):
    for i in range(board.length):
        min = i
        for j in range(i+1,board.length):  
            if board.columns[j]<board.columns[min]:
                min = j
        board.swap(i,min)
        yield True 