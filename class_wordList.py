# -*- coding: utf-8 -*-
import linecache
import os

from random import choice, randint, random, sample, seed, uniform


class wordList(object):
    def __init__(self, sourceFolder="input\\words_names\\wordsSources\\"):
        self.sourceFolder = sourceFolder
        self.wordList = self.concatSourceWordLists()
        # self.prepositionList =
        return

    def concatSourceWordLists(self, destFile="input\\words_names\\words.txt"):
        """ find all the word lists and concat them """
        if os.path.exists(destFile):
            os.remove(destFile)
        sourceFiles = os.listdir(self.sourceFolder)
        with open(destFile, "w") as outfile:
            for filename in sourceFiles:
                with open(self.sourceFolder + filename) as infile:
                    outfile.write(infile.read())
        return destFile

    def combineRandomLinesFromFile(self, numWords=3):
        """ return a number of random words joined into a sentence """
        w = []
        wordListLength = len(open(self.wordList).readlines())
        # w = sample()
        for _ in range(1, numWords + 1):
            numRandomWord = randint(1, wordListLength)
            w.append(
                linecache.getline(self.wordList, numRandomWord)
                .rstrip("\n\r")
                .capitalize()
            )
        outputs = [
            " ".join(w),
        ]
        return choice(outputs)

    def wordsWithPreposition2(
        self, prepositionsListFile="input\\words_names\\wordsSources\\prepositions.txt"
    ):
        """ return 2 word title starting with preposition """
        # TODO words with prepoision check this works
        w = []
        prepositionsListFileLength = len(open(prepositionsListFile).readlines())
        numRandomPreposition = randint(1, prepositionsListFileLength)
        w.append(
            linecache.getline(prepositionsListFile, numRandomPreposition)
            .rstrip("\n\r")
            .capitalize()
        )
        w.append(self.combineRandomLinesFromFile(1))
        for _ in range(1, 10):
            print(" ".join(w))
        return " ".join(w)
