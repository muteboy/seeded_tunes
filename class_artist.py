# -*- coding: utf-8 -*-
from random import choice, randint, random, sample, seed, uniform, choices
from tqdm import tqdm
import os
from class_incarnation import incarnation
from class_album import album
import textwrap
import dominate
from dominate.tags import (
    caption,
    div,
    h1,
    h2,
    h3,
    h4,
    h5,
    p,
    style,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
)


class artist(object):
    def __init__(self, label, number):
        self.label = label
        self.number = number
        self.artistID = f"{self.label.labelID}.A{number}"
        self.people = sample(self.label.people, randint(2, len(self.label.people)))
        # self.people = []
        self.incarnPeople = []
        self.seed = int(str(label.seed) + format(number, "02d"))
        self.yearFirst = randint(
            self.label.yearFirst,
            self.label.yearFirst
            + round((self.label.scene.yearNow - self.label.yearFirst) / 2),
        )
        self.yearLast = randint(self.yearFirst, self.label.scene.yearNow)
        self.incarnations = []

        # while True:
        #     self.people = sample(
        #         self.artist.people, randint(2, min(len(self.artist.people), 6))
        #     )
        #     self.people.sort(key=lambda x: x.fullname)
        #     if (self.artist.numIncarnations) == 1 or (self.number == 1):
        #         break
        #     else:
        #         if self.people != self.artist.incarnations[self.number - 2].people:
        #             break

        # ensure artist name is not the same as the label
        while True:
            self.name = self.label.scene.wordList.combineRandomLinesFromFile(
                numWords=randint(1, 2)
            )
            if self.name != self.label.name:
                break

        # sometimes add "The" to name
        self.name = ("The " + self.name) if random() < 0.2 else self.name
        self.path = "\\".join([self.label.path, self.name.replace(" ", "_")])
        os.mkdir(self.path)
        self.numIncarnations = (
            randint(1, 4)
            if self.label.scene.numIncarnations == 0
            else randint(1, self.label.scene.numIncarnations)
        )
        self.biographyGen = self.biography()
        yearPeriod = round((self.yearLast - self.yearFirst) / self.numIncarnations)
        for numIncarn in tqdm(
            range(1, self.numIncarnations + 1), desc="04 Incarns".ljust(18), position=4
        ):
            # os.mkdir(f'{label.path}\\{self.name.replace(" ", "_")}\\{self.name.replace(" ", "_")}_{numIncarn}')
            incarnYearFirst = self.yearFirst + ((numIncarn - 1) * yearPeriod)
            incarnYearLast = self.yearFirst + (numIncarn * yearPeriod)
            self.incarnations.append(
                incarnation(self, numIncarn, incarnYearFirst, incarnYearLast)
            )
        self.albums = []
        self.years = []

        for i in self.incarnations:
            self.albums.append(i.albums)
            for y in [i.yearFirst, i.yearLast]:
                self.years.append(y)
            self.incarnPeople.extend(i.people)
        self.incarnPeople = list(dict.fromkeys(self.incarnPeople))
        self.people = self.incarnPeople
        self.yearFirst = min(self.years)
        self.yearLast = max(self.years)
        # self.albums.sort(key=lambda a: a.year)
        self.graphIncarnationLinks()

    def __str__(self, numTabs=2):
        return f'{numTabs * chr(9)}Artist: {self.name} ({", ".join([p.fullname for p in self.people])})\n{numTabs * chr(9)} Artist active: {self.yearFirst} to {self.yearLast}\n{numTabs * chr(9)} # of Incarnations: {self.numIncarnations}'

    def biography(self):
        media = open("input\\words_names\\words_media.txt").readlines()
        features = open("input\\words_names\\words_features.txt").readlines()
        otherBands = open("input\\words_names\\names_band_real.txt").readlines()
        comparatives = open("input\\words_names\\words_comparatives.txt").readlines()
        qualifiers = ["","(incorrectly)","(allegedly)","(controversially)","(amusingly)"]
        biogMedias = sample(media,2)
        biogDescriptions = [
            f'"{choice(otherBands).strip()} with {choice(comparatives).strip()} {choice(features).strip()}"',
            f'"{choice(comparatives).strip()} than {choice(otherBands).strip()}"',
            f'"the bastard child of {choice(otherBands).strip()} and {choice(otherBands).strip()}"',
            f'"like {choice(otherBands).strip()} and {choice(otherBands).strip()} had hate sex"',
        ]
        biogDescSample = sample(biogDescriptions,2)
        biogFull = f'Described by \'{biogMedias[0].strip()}\' {choices(population=qualifiers,weights=[10,1,1,1,1],k=1)[0]} as {biogDescSample[0]} and by \'{biogMedias[1].strip()}\' as {biogDescSample[1]}. '
        # TODO create history. make series of statements about who joined, who left etc
        return biogFull

    def graphIncarnationLinks(self):
        if self.numIncarnations == 1:
            pass
        else:
            for i in self.incarnations:
                if i.number == self.numIncarnations:
                    pass
                else:
                    self.label.scene.gvGraph.edge(
                        # from each incarnation to the next unless last one
                        tail_name=f"{self.name} #{i.number}",
                        head_name=f"{self.name} #{i.number + 1}",
                    )

    def html(self):
        # _div = div(id=self.name)
        _div = div(id="artist")
        _div += h3(f"Artist: {self.name}",id="artistName")
        _p = f'{self.biographyGen} '
        if self.yearFirst == self.yearLast:
            _p += f'Active in {self.yearFirst}. '
        else:
            _p += f'Active from {self.yearFirst} to {self.yearLast}. '
        self.numAlbums = sum(map(lambda i: len(i.albums) , self.incarnations))
        _p += f'Released {self.numAlbums} album{"" if self.numAlbums == 1 else "s"}{" over " + str(self.numIncarnations) + " incarnations." if self.numIncarnations > 1 else "."}'
        _div += p(_p, id="artistBiog")
        return _div

