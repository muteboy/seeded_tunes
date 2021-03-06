# -*- coding: utf-8 -*-
from random import choice, randint, random, sample, seed, uniform
# import datetime
# import os
# import textwrap
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
    h6,
    style,
    table,
    span,
    tbody,
    td,
    p,
    th,
    thead,
    tr,
)

# -*- coding: utf-8 -*-
from random import choice, randint, random, sample, seed, uniform
from class_albumArtwork import albumArtwork
# from class_album import album

class albumFormat(object):
    def __init__(self, album, formatType):
        self.album = album
        self.formatType = formatType
        self.formatNames = {
            "CD": "Compact Disc",
            "MC": "Cassette",
            "12": "12 inch Vinyl",
            "PS": "A2 Poster"
        }
        self.year = self.album.year
        if (self.album.year <= 1983):
            self.yearCD = randint(1983, self.album.incarn.yearLast)
        else:
            self.yearCD = self.album.year
        self.catNo = f"{self.album.incarn.artist.label.initials}.{self.formatType}.{self.album.seed}"
        self.textCopyright = f'All titles written by {self.album.surnameCredits}.'
        self.textCopyright += f' \N{COPYRIGHT SIGN} {self.album.year}'
        if self.year != self.album.year:
            self.textCopyright += f'/{self.year}'
        self.textCopyright += f' {self.album.incarn.artist.label.name}'
 
        self.albumArtwork = albumArtwork(self.album, self)

    def __str__(self, numTabs=5):
        return f'{numTabs * chr(9)}{self.formatNames[self.formatType]}, {self.year}'
