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
    leaderboardlist = []
    with open("leaderboard.txt") as leaderboardfile:
        for line in leaderboardfile:
            leaderboardlist.append(line.split(','))

    print(leaderboardlist)
    return leaderboardlist
