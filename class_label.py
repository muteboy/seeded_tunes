# -*- coding: utf-8 -*-
from random import randint, random, sample, seed, choice
from datetime import datetime
import os
from tqdm import tqdm
from class_artist import artist
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


class label(object):
    def __init__(self, scene, number):
        self.scene = scene
        self.number = number
        self.labelID = f"{self.scene.seed}.L{number}"
        # yearStart = self.scene.yearStart
        self.yearFirst = randint(
            self.scene.yearStart,
            self.scene.yearStart
            + round((self.scene.yearNow - self.scene.yearStart) / 2),
        )
        self.yearLast = randint(self.yearFirst, self.scene.yearNow)
        self.years = []
        self.numArtists = (
            randint(1, 6) if self.scene.numArtists == 0 else self.scene.numArtists
        )
        self.seed = int(str(scene.seed) + format(self.number, "02d"))
        seed(self.seed)
        self.nameSuffixes = ["Recordings", "Records", "", "Group", "Committee", "Music"]
        self.name = f"{self.scene.wordList.combineRandomLinesFromFile(numWords=1)} {choice(self.nameSuffixes)}"

        #         keepCharacters = (' ','.','_')
        #         "".join(ch for ch in filename if ch.isalnum() or ch in keepCharacters).rstrip()

        self.initials = "".join([word[0] for word in self.name.split()])
        self.path = "\\".join([self.scene.path, self.name.replace(" ", "_")])
        os.mkdir(self.path)
        self.people = sample(self.scene.people, self.numArtists * 6)
        self.artistPeople = []
        self.artists = []
        self.albumCatalog = []
        for num in tqdm(
            range(1, self.numArtists + 1), desc="03 Artists".ljust(18), position=3
        ):
            self.artists.append(artist(self, num))
        for a in self.artists:
            self.artistPeople.extend(a.people)
            for y in [a.yearFirst, a.yearLast]:
                self.years.append(y)
            for i in a.incarnations:
                self.albumCatalog += i.albums
        self.artistPeople = list(set(self.artistPeople))
        self.people = self.artistPeople
        self.albumCatalog = sorted(self.albumCatalog, key=lambda a: a.year)
        self.years = list(dict.fromkeys(self.years))
        self.yearFirst = min(self.years)
        self.yearLast = max(self.years)
        for idx, alb in enumerate(self.albumCatalog):
            alb.catNo = f"{self.initials}{self.seed}A{format(idx+1, '02d')}"
        # self.graph()

    def comment(self):
        comment = f'Roster of {self.numArtists} {"artist" if self.numArtists==1 else "artists"}. '
        if self.yearFirst == self.yearLast:
            comment += f"Active in {self.yearFirst}. "
        else:
            comment += f"Active from {self.yearFirst} to {self.yearLast}. "
        return comment

    def personnel(self):
        return f'Personnel: {", ".join([p.fullname for p in self.people])}. '

    def __str__(self, numTabs=1):
        return f"{numTabs * chr(9)}Label: {self.name}\n{numTabs * chr(9)} Label active {sorted(self.years)}\n{numTabs * chr(9)} # Artists: {self.numArtists}"

    def graph(self):
        nl = '<<table cellspacing="0" cellpadding="2">'
        nl += f'<tr><td sides="b" align="left" border="1"><font point-size="10"><b>{self.name} Personnel</b></font></td></tr>'
        for p in self.people:
            nl += (
                '<tr><td align="left" border="0"><font point-size="9">'
                + p.fullname
                + "</font></td></tr>"
            )
        nl += "</table>>"
        self.scene.gvGraph.node(name=self.name, label=nl, shape="plaintext", margin="0")

    def html(self):
        # _div = div(id=self.name)
        _div = div(id="label")
        _div += h2(f"Label: {self.name}", id="labelName")
        _div += p(self.personnel(), id="labelPersonnel")
        _div += p(self.comment(), id="labelComment")
        return _div
