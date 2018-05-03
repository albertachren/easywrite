import numpy as np

UNSURE_WORD = '½'
UNFINISHED = '§'


def loadEssay():
    essay = []
    wordEdits = []
    bigEdits = []
    paragraph = []
    sentence = []
    with open("document.txt", mode='r', encoding='utf-8') as f:
        words = f.read().replace('\n', '\n ').split(" ")
    for word in words:
        sentence.append(word)
        if ('.' in word) or ('?\n' in word) or ('!\n' in word): # If the sentence ends
            paragraph.append(sentence[:])
            sentence.clear()
        if '\n' in word: # If the paragraph ends
            essay.append(paragraph[:])
            paragraph.clear()
    return essay


def indexEdits(essay):
    global UNSURE_WORD
    global UNFINISHED
    wordEdits, bigEdits = ([] for i in range(2))
    for i, paragraph in enumerate(essay):
        for j, sentence in enumerate(paragraph):
            for k, word in enumerate(sentence):
                if UNSURE_WORD in word:
                    wordEdits.append([i,j,k])
                if UNFINISHED in word:
                    bigEdits.append([i,j])
    return wordEdits, bigEdits


def getSentence(essay, index):
    sentence = " ".join(essay[index[0]][index[1]]).replace('\n', '')
    return sentence


def editWords(essay, wordEdits):
    print("correct words - " + str(len(wordEdits)))
    print("--------------------------------------")
    for i, wordEdit in enumerate(wordEdits):
        print(getSentence(essay, wordEdit))
        print("--------------------------------------")
        if input("correct? y/n") == 'y':
            correction = input("Correction: ")
            if " ".join(essay[wordEdit[0]][wordEdit[1]]).count('\n')>0:
                correction += '\n'
            essay[wordEdit[0]][wordEdit[1]] = correction.split(" ")
            print(correction.replace('\n', ''))
        print("--------------------------------------")
    print("######################################")

def editPar(essay, parEdits):
    print("######################################")
    print("correct blocks - " + str(len(parEdits)))
    print("--------------------------------------")
    for i, parEdit in enumerate(parEdits):
        try:
            if (parEdit[1] -1) > 0:
                pro = parEdit[:]
                pro[1] -= 1
                print(getSentence(essay, pro) + '\n')
            print(getSentence(essay, parEdit) + '\n')
            if (parEdit[1] + 1)<len(essay[parEdit[0]][parEdit[1]]):
                post = parEdit[:]
                post[1] += 1
                print(getSentence(essay, post))
        except IndexError as e:
            pass
        print("--------------------------------------")
        if input("correct? y/n") == 'y':
            correction = input("Correction: ")
            essay[parEdit[0]][parEdit[1]] = correction.split(" ")
            print(correction)
        print("--------------------------------------")
    print("######################################")


if __name__ == "__main__":
    essay = loadEssay()
    wordEdits, bigEdits = indexEdits(essay)
    while(True):
        print("easywrite\n0. save\n1. unsure words\n2. unfinished blocks\n3. crowded sentences\n4. repeating words")
        user_input = input()
        if user_input == str(0):
            with open("wipdocument.txt", mode='w', encoding='utf-8') as f:
                for paragraph in essay:
                    for sentence in paragraph:
                        f.write(" ".join(sentence))
                f.close()
            print("saved\n")
        if user_input == str(1):
            editWords(essay, wordEdits)
        if user_input == str(2):
            editPar(essay, bigEdits)
