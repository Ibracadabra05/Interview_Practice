#quicksort algorithm

def partition(A, start, end):
    partition_index = start 
    pivot = A[end]
    
    for i in range(start, end):
        if A[i] <= pivot:
            temp = A[i]
            A[i] = A[partition_index]
            A[partition_index] = temp
            partition_index += 1
    
    temp = A[end]
    A[end] = A[partition_index]
    A[partition_index] = temp
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