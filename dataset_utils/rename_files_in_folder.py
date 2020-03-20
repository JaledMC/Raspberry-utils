'''
Script to rename all files in a specific folder
It is set to output:
0.jpg
1.jpg
.
.
.
'''
import os
path = '/home/pi/Desktop/fotos_bsh'
i = 0
for filename in os.listdir(path):
    os.rename(os.path.join(path,filename), os.path.join(path,str(i)+'.jpg'))
    i = i +1