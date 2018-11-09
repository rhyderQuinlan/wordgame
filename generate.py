import random

#Generate source word
def sourceword():
    sourcewordslist = []
    with open("dict/sourcewords.txt") as sourcewordfile:
        for line in sourcewordfile:
            sourcewordslist.append(line.strip())

    word = sourcewordslist[random.randint(0, len(sourcewordslist))]

    return word

def leaderboard():
    file = open('leaderboard.txt', 'r')
    lines = file.readlines()


    leaderboardlist = []

    for line in lines:
        line = line.split(',')
        for i in range(0, len(line)):
            line[i] = line[i].strip()
        leaderboardlist.append(line)

    return leaderboardlist
