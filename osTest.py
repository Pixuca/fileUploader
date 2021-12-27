import os

path = 'C:/Users/marce/Documents/uploads' 
array = os.listdir(path)
extArray = []
for item in array:
    ext = item.split('.')
    extArray.append(ext[-1])

# print(extArray)
# print(array)
for item in range(len(array)):
    print(array[item], extArray[item])