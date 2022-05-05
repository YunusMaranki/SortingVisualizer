def partition(board,l,r):
    pivot = board.columns[r]
    i = l-1
    j = r
    while 1:
        i += 1
        while board.columns[i]<pivot:
            i += 1
        j -=1
        while board.columns[j]>pivot:
            j -= 1
        if i>=j:
            break
        board.swap(i,j)
        yield i
    board.swap(i,r)
    yield i

def quickSort(board,l=0,r=None): 
    stack = []
    stack.append(0)
    stack.append(board.length-1)
    while stack:  
        r = stack.pop()
        l = stack.pop()
        for i in partition(board,l,r):
            yield True
        if i-1>l:
            stack.append(l)
            stack.append(i-1)
        if i+1<r:
            stack.append(i+1)
            stack.append(r)
