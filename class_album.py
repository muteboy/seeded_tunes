# -*- coding: utf-8 -*-
import datetime
import os
import textwrap
from random import choice, randint, random, sample, seed, uniform
import colorsys
import dominate
from dominate.tags import (
    caption,
    div,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    span,
    style,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
)
from tqdm import tqdm
import svgwrite
from class_albumArtwork import albumArtwork
from class_albumFormat import albumFormat
from class_track import track


class album(object):
    def __init__(self, incarnation, number):
        """ Init album object """
        self.incarn = incarnation
        self.seed = int(str(self.incarn.seed) + format(number, "02d"))
        self.number = number
        self.albumID = f"{self.incarn.artist.artistID}.R{number}"
        self.formatTypes = ["CD", "MC", "12", "PS"]
        self.formats = []
        self.catNo = f"{self.incarn.artist.label.initials}.{self.seed}"
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
            self.numTracks = randint(1, self.incarn.artist.label.scene.numTracks)
        if self.numTracks < 5:
            self.name += " EP"
        self.svgTagline = "ELECTRONIC MUSIC AND ART GENERATED AND RECORDED DIGITALLY BY SEED"
        nbsp = "\N{NO-BREAK SPACE}"
        self.surnameCredits = "\N{NO-BREAK SPACE}/\N{NO-BREAK SPACE}".join(
            [p.surname for p in self.people]
        )
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
        # choose colors for artwork

        hue = random()
        self.artColorOutline = self.albumArtBG(hue, 0.15, 0.2)
        self.artColorBG = self.albumArtBG(hue, 0.3, 0.2)
        self.artColorText = "white"

        for formatType in self.formatTypes:
            self.formats.append(albumFormat(self, formatType))
        # albumArtwork(self, )
        # self.albumArtwork = albumArtwork(self)

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
        # _div = div(id=self.name)
        _div = div(id="album")
        _div += h5(
            span(self.name, style="font-style:italic;"),
            (", " + str(self.year)),
            id="albumName",
        )
        # tbl = table(id=self.name, caption=self.name, style="font-size:80%")
        tbl = table(id="albumTrackTable", caption=self.name, style="font-size:80%")
        tbl += thead(tr(th(tableHead) for tableHead in albumTableHeaders), style="",)
        # tbl += 
        _tbody = tbody()
        for tk in tqdm(self.tracks, desc="16 Log Tracks".ljust(18), position=16,):
            _tbody += tk.html()
        tbl += _tbody
        ftbl = table(id="albumFormatTable", caption=self.name, style="font-size:100%")
        ftbl += thead(
            tr(th(tableHead) for tableHead in ["Format", "Cat No", "Year of Release"]),
            style="",
        )
        for f in self.formats:
            ftbl += tr(td(f.formatNames[f.formatType]), td(f.catNo), td(f.year))
        _div += ftbl
        _div += p()
        _div += tbl
        return _div

    def albumArtBG(self, hue, lightness, saturation):
        """ Choose colour, based on seed, Hue, Saturation, Lightness """
        # hlsList=(random(),0.3,0.2)
        rgbList = colorsys.hls_to_rgb(hue, lightness, saturation)
        # rgbList = colorsys.hsv_to_rgb(hue, saturation, lightness)
        svgCol = svgwrite.utils.rgb(
            rgbList[0] * 255, rgbList[1] * 255, rgbList[2] * 255
        )
        return svgCol
