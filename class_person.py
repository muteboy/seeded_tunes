# -*- coding: utf-8 -*-
from random import choice, randint, random, sample, seed, uniform

from tqdm import tqdm

from class_wordList import wordList
import dominate
from dominate.tags import (caption, div, h1, h2, h3, h4, h5, style, table, tbody, td,
                           th, thead, tr)

class person(object):
    def __init__(self):
        self.incarnList = []
        # fileFirstNames = open("input\\words_names\\names_first.txt")
        # fileSurnames = open("input\\words_names\\names_surnames.txt")
        linesFirstNames = open("input\\words_names\\names_first.txt").readlines()
        linesSurnames = open("input\\words_names\\names_surnames.txt").readlines()
        self.firstName = choice(linesFirstNames).rstrip("\n\r")
        self.surname = choice(linesSurnames).rstrip("\n\r")
        self.personID = f"{self.firstName}_{self.surname}"
        self.fullname = f"{self.firstName} {self.surname}"

    def __hash__(self):
        return hash(self.fullname)

    def __eq__(self, other):
        return self.fullname == other.fullname

    def __str__(self, numTabs=1):
        out = f"{numTabs * chr(9)}Person : {self.firstName} {self.surname}\n"
        for i in self.incarnList:
            out += f"{(numTabs+1) * chr(9)}Incarnation: {i.incarnID} {i.name}\n"
        return out
