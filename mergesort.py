# mergesort algorithm

def merge(left, right, A):
    l = 0
    r = 0
    i = 0
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            A[i] = left[l]
            l += 1
        else:
            A[i] = right[r]
            r += 1
        i += 1
    
    while l < len(left):
        A[i] = left[l]
        l += 1
        i += 1
    
    while r < len(right):
        A[i] = right[r]
        r += 1
        i += 1


def mergesort(A):
    if len(A) < 2:
        return 
    
    mid = len(A) / 2
    
    left = []
    right = []
    
    for i in range(0, mid):
        left.append(A[i])
    
    for j in range(mid, len(A)):
        right.append(A[j])
    
    mergesort(left)
    mergesort(right)
    
    merge(left, right, A)
    
    
testcase = [2, 4, 1, 6, 8, 5, 3, 7]

mergesort(testcase)

if testcase == [1, 2, 3, 4, 5, 6, 7, 8]:
    print "test passed"
else:
    print testcase
    print "test failed"