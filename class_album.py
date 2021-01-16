# -*- coding: utf-8 -*-
from random import choice, randint, random, sample, seed, uniform
import datetime
import os
import textwrap
from tqdm import tqdm
from class_albumArtwork import albumArtwork
from class_track import track
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
    table,
    span,
    tbody,
    td,
    th,
    thead,
    tr,
)


class album(object):
    def __init__(self, incarnation, number):
        """ Init album object """
        self.incarn = incarnation
        self.seed = int(str(self.incarn.seed) + format(number, "02d"))
        self.number = number
        self.albumID = f"{self.incarn.artist.artistID}.R{number}"
        self.catNo = f"{self.incarn.artist.label.initials}{self.seed}"
        # TODO LATER make catNo sequential across whole label, not within artist. Hard
        self.name = self.incarn.artist.label.scene.wordList.combineRandomLinesFromFile(
            numWords=randint(1, 3)
        )
        self.path = "\\".join([self.incarn.path, self.name.replace(" ", "_")])
        os.mkdir(self.path)
        self.year = randint(self.incarn.yearFirst, self.incarn.yearLast)
        self.incarn.artist.label.years.append(self.year)
        self.people = sample(self.incarn.people, randint(2, len(self.incarn.people)))
        self.tracks = []
        if self.incarn.artist.label.scene.numTracks == 0:
            self.numTracks = randint(1, 10)
        else:
            self.numTracks = self.incarn.artist.label.scene.numTracks
        if self.numTracks < 5:
            self.name += " EP"
        self.svgTagline = "ELECTRONIC MUSIC GENERATED AND RECORDED DIGITALLY BY SEED"
        self.surnameCredits = "\N{NO-BREAK SPACE}/\N{NO-BREAK SPACE}".join(
            [p.surname for p in self.people]
        )
        nbsp = "\N{NO-BREAK SPACE}"
        self.trackNamesText = "     ".join(
            [
                f'{i+1}.\N{NO-BREAK SPACE}{t.name.replace(" ",nbsp)}'
                for i, t in enumerate(self.tracks)
            ]
        )
        self.trackNamesTextLineBreak = "\n".join(
            [
                f'{i+1}.\N{NO-BREAK SPACE}{t.name.replace(" ",nbsp)}'
                for i, t in enumerate(self.tracks)
            ]
        )
        self.trackNamesTextWrapped = textwrap.wrap(self.trackNamesText, 140)
        # create num number of tracks
        for num in tqdm(
            range(1, self.numTracks + 1), desc="06 Tracks".ljust(18), position=6
        ):
            self.tracks.append(track(self, num))
        # self.textCopyright = f'All titles written by {self.surnameCredits}. \N{COPYRIGHT SIGN} {self.year} {self.artist.label.name}'
        self.albumArtwork = albumArtwork(self)

    def __str__(self, numTabs=4):
        return f'{numTabs * chr(9)}Album {self.seed}: "{self.name}", {self.year}\n{numTabs * chr(9)} Personnel: {", ".join([p.fullname for p in self.people])}\n{numTabs * chr(9)}# of Tracks: {self.numTracks}'

    def html(self):
        albumTableHeaders = [
            "Num",
            "Track Name",
            "bpm",
            "len MMSS",
            "bars pm",
            "steps ps",
            "steps pb",
            "secs goal",
            "beats goal",
            "bars goal",
            "bars goal rd",
            "beats goal rd",
            "steps goal",
            "steps rd",
            "secs rd",
            "step len",
            "len steps",
            "beats act",
            "bars",
            "kick",
            "snare",
            "hhc",
            "hho",
        ]
        _div = div(id=self.name)
        _div += h5(
            span(self.name, style="font-style:italic;"), (", " + str(self.year)),
        )
        tbl = table(id=self.name, caption=self.name, style="font-size:80%")
        tbl += thead(tr(th(tableHead) for tableHead in albumTableHeaders), style="",)
        for tk in tqdm(self.tracks, desc="16 Log Tracks".ljust(18), position=16,):
            tbl += tk.html()
        _div += tbl
        return _div

