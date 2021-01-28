# -*- coding: utf-8 -*-

import sys
from random import choice, randint, random, sample, seed, uniform


from class_scene import scene
from class_track import track

defaultSeed=100672
# inputSeed = int(input(f"Enter seed number, or hit Enter for default ({defaultSeed}): ") or defaultSeed)
inputSeed = defaultSeed

print("\n" * 20)

sceneCurrent = scene(
    seedInt=inputSeed,
    # seedInt=sys.argv[1],
    numLabels=1,
    yearStart=1972,
    viewGv=False,
    numArtists=1,
    numIncarnations=1,
    numAlbums=1,
    numTracks=2,
    viewLog=False,
)

print("\n" * 20)

# a = track(album=Null, number=1)

