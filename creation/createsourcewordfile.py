#creation of sourcewords.txt file
def createsourcewordfile():

    file = open("dict/words.txt", 'r')
    sourcefile = open("dict/sourcewords.txt", 'w')

    for line in file:
        if(len(line) >= 8):
            if line.find("'") == -1:
                sourcefile.write(line)

createsourcewordfile()
