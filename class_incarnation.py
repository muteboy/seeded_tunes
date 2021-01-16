# -*- coding: utf-8 -*-
import os
import textwrap
from random import choice, randint, random, sample, seed, uniform

from tqdm import tqdm
import dominate
from dominate.tags import (
    caption,
    div,
    h1,
    h2,
    h3,
    h4,
    h5,
    style,
    span,
    table,
    tbody,
    td,
    p,
    th,
    thead,
    tr,
)
from class_album import album


class incarnation(object):
    """ An incarnation of an artist, with a subset of the artist pool of people. """

    def __init__(self, artist, incarnNumber, yearFirst, yearLast):
        self.artist = artist
        self.artistName = self.artist.name
        self.number = incarnNumber
        self.seed = int(str(artist.seed) + format(self.number, "02d"))
        if self.artist.numIncarnations == 1:
            self.name = self.artist.name
        else:
            self.name = f"{self.artist.name} #{self.number}"
        self.yearFirst = yearFirst
        self.yearLast = yearLast
        self.incarnID = f"{self.artist.artistID}.I{self.number}"
        # make sure people in different incarns are different. Loop through until peoples are different.
        while True:
            self.people = sample(
                self.artist.people, randint(2, min(len(self.artist.people), 6))
            )
            self.people.sort(key=lambda x: x.fullname)
            if (self.artist.numIncarnations) == 1 or (self.number == 1):
                break
            else:
                if self.people != self.artist.incarnations[self.number - 2].people:
                    break
        self.path = f'{self.artist.path}\\{self.name.replace(" ","_")}'
        os.mkdir(self.path)
        self.albums = []
        self.years = []
        self.numAlbums = (
            randint(1, 3)
            if self.artist.label.scene.numAlbums == 0
            else self.artist.label.scene.numAlbums
        )
        for num in tqdm(
            range(1, self.numAlbums + 1), desc="05 Albums".ljust(18), position=5
        ):  # generate num albums
            self.albums.append(album(self, num))
        self.albums.sort(key=lambda a: a.year)
        self.albumPeople = []
        for a in self.albums:
            self.years.append(a.year)
            self.albumPeople.extend(a.people)
        self.people = self.albumPeople  # replace pool with actual people used on albums
        self.people = list(dict.fromkeys(self.people))
        self.years = list(dict.fromkeys(self.years))
        self.yearFirst = min(self.years)
        self.yearLast = max(self.years)
        for p in self.people:
            p.incarnList.append(self)
        self.graphIncarnation()

    def __str__(self, numTabs=3):
        return f'{numTabs * chr(9)}Incarnation: {self.artist.name} #{self.number} ({", ".join([p.fullname for p in self.people])})\n {numTabs * chr(9)} Incarnation active: {self.yearFirst} to {self.yearLast}\n {numTabs * chr(9)} # of Albums: {self.numAlbums}'

    def __repr__(self):
        return f'Incarnation: {self.artist.name} #{self.number} ({", ".join([p.fullname for p in self.people])})'

    def incarnHistory(self):
        if self.numAlbums == 1:
            history = (
                f"Released 1 album on {self.artist.label.name} in {self.yearFirst}. "
            )
        else:
            history = f"Released {len(self.albums)} albums on {self.artist.label.name}, from {self.yearFirst} to {self.yearLast}. "
        return history

    def graphIncarnation(self):
        g = self.artist.label.scene.gvGraph
        # artistBiog = self.artist.biography().replace("'", " <I>", 1).replace("'","</I>  ",2).replace("'"," <I>  ",3).replace("'","</I>  ",4) if self.number == 1 else ""
        artistBiog = self.artist.biographyGen if self.number == 1 else ""
        numIncarnPeople = len(self.people)
        numIP2 = numIncarnPeople * 2
        incarnLabel = f'<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="4">'
        # incarnLabel += f'<TR><TD COLSPAN="{numIncarnPeople*2}" BORDER="0" SIDES="B"><B><FONT POINT-SIZE="12">{incarnName}</FONT></B></TD></TR>'
        incarnLabel += f'<TR><TD COLSPAN="{numIncarnPeople}" BORDER="0"><B><FONT POINT-SIZE="12">{self.name}</FONT></B></TD>'
        incarnLabel += f'<TD COLSPAN="{numIncarnPeople}"><FONT POINT-SIZE="6">{"<BR/>".join(textwrap.wrap(artistBiog + self.incarnHistory(),width=30))}</FONT></TD></TR>'
        incarnLabel += "<TR>"
        cellNone = 'BORDER="0"'
        cellTL = 'BORDER="1" SIDES="TL"'
        # cellTR = 'BORDER="1" SIDES="TR"'
        cellT = 'BORDER="1" SIDES="T"'
        # cellR = 'BORDER="1" SIDES="R"'
        cellL = 'BORDER="1" SIDES="L"'
        # cellB = 'BORDER="1" SIDES="B"'
        for p2 in range(1, numIP2 + 1):
            incarnLabel += f'<TD CELLPADDING="1" {cellNone if p2 == 1 else cellL if p2 == numIP2 else cellTL if (p2 % 2 == 0) else cellT}></TD>'
        incarnLabel += "</TR>"
        incarnLabel += "<TR>"
        for p in self.people:
            incarnLabel += (
                f'<TD COLSPAN="2"><FONT POINT-SIZE="7">{p.fullname}</FONT></TD>'
            )
            # incarnLabel += f'<TD COLSPAN="2">{p.fullname}<BR/><FONT POINT-SIZE="9">{"bass/voc"}</FONT></TD>'
        incarnLabel += "</TR></TABLE>>"
        g.node(name=self.name, label=incarnLabel)

    def html(self):
        _div = div(id=self.name)
        _div += h4(self.name)
        _div += p(f'Personnel: {", ".join([p.fullname for p in self.people])}.')
        _div += p(self.incarnHistory())
        return _div
