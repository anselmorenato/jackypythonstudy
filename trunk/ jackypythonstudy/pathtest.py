import os
import sys
#try:
dirName = os.path.dirname(os.path.abspath(__file__))
#except:
    #dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'images')

print dirName
print bitmapDir
