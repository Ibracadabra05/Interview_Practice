#quicksort algorithm

def swap(x, y):
    return y, x

def partition(A, start, end):
    partition_index = start 
    pivot = A[end]
    
    for i in range(start, end):
        if A[i] <= pivot:
            A[i], A[partition_index] = swap(A[i], A[partition_index])
            partition_index += 1
    
    A[end], A[partition_index] = swap(A[end], A[partition_index])
    return partition_index

def quicksort(A, start, end):
    if start >= end:
        return
    
    partition_index = partition(A, start, end)
    quicksort(A, start, partition_index - 1)
    quicksort(A, partition_index + 1, end)

#test
testcase = [2, 4, 1, 6, 8, 5, 3, 7]

quicksort(testcase, 0, len(testcase) - 1)

if testcase == [1, 2, 3, 4, 5, 6, 7, 8]:
    print "test passed"
else:
    print testcase
    print "test failed"