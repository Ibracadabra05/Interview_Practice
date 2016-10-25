#Insertion sort 

def insertion_sort(A):
    n = len(A)
    for i in range(n):
        hole = i
        value = A[i]
        while hole > 0 and A[hole - 1] > value:
            A[hole] = A[hole - 1]
            hole -= 1 
        A[hole] = value 

testarray = [7, 2, 4, 1, 5, 3]

insertion_sort(testarray)

if testarray == [1, 2, 3, 4, 5, 7]:
    print "test passes"
else:
    print "test failed"