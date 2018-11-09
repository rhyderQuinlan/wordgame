import enchant
from flask import Flask, session


def checkword(word, sourcewordlist, sourceword, errors, tempwords):
    # check letters
    letterfrequency = sourcewordlist.copy()
    for x in range(len(word)):
        if word[x] in letterfrequency:
            letterfrequency[word[x]] = letterfrequency[word[x]] - 1
            if letterfrequency[word[x]] < 0:
                errors.append(word + " uses to many " + word[x] + "'s.")
                return False
        else:
            errors.append(word + " does not use letters from the sourceword.")
            return False

    # check word is 3 letters
    if not (len(word) >= 3):
        errors.append(word + " is less than 3 letters.")
        return False

    # check valid dictionary word
    if not enchant.Dict("en_US").check(word):
        errors.append(word + " is not in the dictionary.")
        return False

    # check duplicate
    if word in tempwords:
        errors.append(word + " is used more than once.")
        return False
    tempwords.append(word)

    # check word is not sourceword
    if word == sourceword:
        errors.append(word + " is equal to the sourceword")
        return False

    session["errors"] = errors
    return True
