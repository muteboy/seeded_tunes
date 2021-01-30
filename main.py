# -*- coding: utf-8 -*-

import sys
from random import choice, randint, random, sample, seed, uniform

import re
from class_scene import scene
from class_track import track

from inspect import getmembers, isfunction 

from class_albumArtwork import albumArtwork

# funclist = getmembers(albumArtwork,isfunction)
# funclist = [f for f in getmembers(albumArtwork,isfunction) if (re.match(r'svgSymbol*',f[0]))]

# for f in funclist:
#     print(f[1].__defaults__[0])
#     print(str(x[1] for x in f[1].__defaults__))

defaultSeed = 100672
# inputSeed = int(input(f"Enter seed number, or hit Enter for default ({defaultSeed}): ") or defaultSeed)
inputSeed = defaultSeed

print("\n" * 20)

stopppp=False
if stopppp==True:
    pass
else:
    if (len(sys.argv)==1) or (sys.argv[1] != "0"):
        sceneCurrent = scene(
            seedInt=inputSeed,
            # seedInt=sys.argv[1],
            numLabels=0,
            yearStart=1972,
            viewGv=True,
            numArtists=0,
            numIncarnations=0,
            numAlbums=0,
            numTracks=0,
            viewLog=True,
        )
    else:
        sceneCurrent = scene(
            seedInt=inputSeed,
            numLabels=1,
            yearStart=1972,
            viewGv=False,
            numArtists=1,
            numIncarnations=1,
            numAlbums=1,
            numTracks=1,
            viewLog=False,
        )

print("\n" * 20)

# a = track(album=Null, number=1)

