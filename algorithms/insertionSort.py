def insertionSort(board):
    for i in range(1,board.length):
        j = i
        while j>=1 and board.columns[j-1]>board.columns[j]:
            board.swap(j-1,j)
            j -= 1
            yield True
