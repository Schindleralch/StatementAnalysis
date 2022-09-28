testlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
x = 61



def BinarySearch(arr, x):
    low = 0
    high = len(arr)-1
    
    while low <= high:
        mid = (low + high) // 2  #int division, no floats
        if arr[mid] == x:
            return True

        elif arr[mid] > x:
            high = (mid - 1)

        elif arr[mid] < x:
            low = mid + 1

      
    return False 

result = BinarySearch(testlist, x)

if (not(result)):
   print(f"{x} not found in list")
else: 
    print(f"{x} found in list")
