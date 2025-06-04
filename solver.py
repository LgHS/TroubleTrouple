import os.path
from pathlib import Path
from itertools import groupby

script_path = Path(__file__).parent.absolute()
dict_path = os.path.join(script_path, "dic.txt")
arraySize = 4

def countLetters(flatArray):
    ret = {}
    for key, group in groupby(flatArray, lambda x: x):
        ret[key] = len(list(group))
    return ret


def haveTheRightLetters(availableLettersCount, word):
    count = countLetters(word)
    for letter, c in count.items():
        if (availableLettersCount.get(letter, 0) < c):
            return False
    return True


def findPath(lettersFlatArray, remainingWord, path):

    if(len(remainingWord) == 0):
        return path

    nextLetter=remainingWord[0]
    nextPathAvailable = range(len(lettersFlatArray)) if len(path) == 0 else possibleTransitionFrom(path[len(path)-1])
    candidates=list(filter(lambda i : lettersFlatArray[i] == nextLetter and (i not in path) and (i in nextPathAvailable),
                           range(len(lettersFlatArray))))

    if(len(candidates) == 0):
        return None

    l = list(filter(lambda x: x != None,
               map(lambda c: findPath(lettersFlatArray, remainingWord[1:], path + [c]), candidates)))
    if(len(l)==0):
        return None
    else:
        return l[0]



def rowCol(i):
    return int(i / arraySize), int(i % arraySize)


def index(row, col):
    return int(row * arraySize + col)


def possibleTransitionFrom(i):
    row, col = rowCol(i)
    transitions = []
    for ca in [-1, 0, +1]:
        for ra in [-1, 0, +1]:
            rac = row + ra
            cac = col + ca
            if (rac < 0 or rac == arraySize or cac < 0 or cac == arraySize):
                pass
            else:
                transitions.append(index(rac, cac))

    return transitions

def flatten(letterArray):
    return [x for xs in letterArray for x in xs]

def solve(letterArray):
    flatArray = flatten(letterArray)
    letterCount = countLetters(flatArray)
    print("count:" + str(letterCount))

    with open(dict_path, 'r') as file:
        candidates = list(
            filter(lambda w: haveTheRightLetters(letterCount, w), map(lambda l: l.replace("\n", ""), file)))
        print("candidates : " + str(len(candidates)))
        candidates.sort(key=lambda w: len(w), reverse=True)

        for w in candidates:
            result = findPath(flatArray, w, [])
            if(result != None):
                print("%s, %s" % (w, result))
