# import glob
import os

class worm():

    def __init__(self):

        # list of directories
        self.dirs = []
        # list of paths
        self.paths = []

        # the initial path that we are searching along
        self.path = '/Library/Python/3.7/lib/python/site-packages'

        for root, directories, files in os.walk(self.path):
            self.dirs.append(directories)

        # we only want the first element
        self.dirs = self.dirs[0]

        # find every python file that is not a cache file
        for dir in self.dirs:
            for root, directories, files in os.walk('/'.join([self.path,dir])):
                for file in files:
                    # filters out the cache file
                    if '.py' in file and '.pyc' not in file:
                        self.paths.append('/'.join([self.path,dir,file]))

if __name__ =='__main__':
    # make a worm instance
    worm = worm()

    for path in worm.paths:
        with open(path, 'r') as file:
            print(file)
