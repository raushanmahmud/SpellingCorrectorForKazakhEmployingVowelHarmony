#!/usr/bin/python
# coding=utf-8
import sys
import re
from collections import Counter

def isSoft(word):
    soft = False
    # non-replacable letters = ы, е , я
    # if we have more than 1 а we know for sure it is not soft
    occurencesOfA = word.count('а')
    if (occurencesOfA<1):
        soft = True
    #if there is ы, ка, га я we know it is not soft
    if (word.count('х')>0) or (word.count('о')>0) or  (word.count('ы')>0) or (word.count('га')>0) or (word.count('го')>0) or (word.count('ка')>0):
        soft = False
    # if there is и, е, і we know it is soft
    if ((word.count('и')>0) or (word.count('е')>0) or (word.count('і')>0) or (word.count('ә')>0)) and (soft != False):
        soft = True
    # two roots word forms

    return soft # if we are not clear, we are gonna go and ckeck it in the dictionary

def indexOfSubstr(word, substr):
    return word.find(substr)

def isAVowel(word):
    vowel = False
    if (vowel=="а" or vowel=="ә" or vowel=="е" or vowel=="и" or vowel=="о" or vowel=="ө" or vowel=="і" or vowel=="ы"):
        vowel = True
    return vowel


def checkForVowelHarmony(word):
    # change к - қ
    # change и - і, except ия
    # change н - ң
    # change г - ғ
    # change у - ү
    # change о - ө, except ов
    # change а - ә
    softWord = isSoft(word)
    if (not softWord) and (word.count('е')<1):
        word = word.replace("к","қ") # if its is not soft
    if (softWord):
        word = word.replace("и","і") # if it is soft
    word = word.replace("ыныз","ыңыз") # in the end of the string
    word = word.replace("ініз","іңіз") # in the end of the string
    word = word.replace("нын","ның") # in the end of the string
    word = word.replace("нін","нің") # in the end of the string
    word = word.replace("дын","дың") # in the end of the string
    word = word.replace("дін","дің") # in the end of the string
    if (indexOfSubstr(word,"тын")>0 and not isAVowel(word[indexOfSubstr(word,"тын")-1])):
        word = word.replace("тын","тың") # in the end of the string
    if (indexOfSubstr(word,"тін")>0 and not isAVowel(word[indexOfSubstr(word,"тін")-1])):
        word = word.replace("тін","тің") # in the end of the string
    if softWord:
        word = word.replace("о","ө") # if is it soft
    if softWord:
        word = word.replace("а","ә") # if it is soft
    if not softWord or word.count("о")>0:
        word = word.replace("г","ғ") # if it is not soft
    if softWord:
        word = word.replace("ы","і") # if is it soft
    if (indexOfSubstr(word,"у")!=len(word)-1):
        if softWord:
            word = word.replace("у","ү")
        elif not softWord:
            word = word.replace("у","ұ") # unless it is at the end of the word, then (if it is soft change it ti ү, otherwise change it to ұ)
      
    return word

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'аәбвгғдежзийкқлмнңыіоөпрстуүұфхһцшщчъьэяю'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
#evaluation
def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        wrongV = checkForVowelHarmony(wrong)
        w = correction(wrongV)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]
# uncomment lines below to evaluate the accuracy
#evaluating
#print("Evaluating accuracy...")
#spelltest(Testset(open('spell-testset.txt'))) # Development set

#example
s = raw_input('-->')

input_text = s.split()
corrected = ""
for word in input_text:
    wordV = checkForVowelHarmony(word.lower())
    corrected += correction(wordV) + " "
print(corrected)

#suggestions
#suggestions = set(known([word.lower()]) or known(edits1(word.lower())) or known(edits2(word.lower())))

#if (len(suggestions)>1):
#	print("Suggestions:")
#	print(suggestions)

#print(max(WORDS, key=P))
