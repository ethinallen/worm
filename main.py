# import glob
import os

class worm():

    def __init__(self):
        # counting a lot of things
        count = 0

        # the initial path that we are searching along
        path = '/Library/Python/2.7/site-packages'

        # list of directories
        dirs = []

        for root, directories, files in os.walk(path):
            dirs.append(directories)

        # we only want the first element
        dirs = dirs[0]

        # find every python file that is not a cache file
        for dir in dirs:
            for root, directories, files in os.walk('/'.join([path,dir])):
                for file in files:
                    # filters out the cache file
                    if '.py' in file and '.pyc' not in file:
                        count += 1
                        print('/'.join([path,dir,file]))
        print(count)

if __name__ =='__main__':
    worm = worm()
