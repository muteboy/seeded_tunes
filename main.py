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
    numLabels=2,
    yearStart=1972,
    viewGv=False,
    numArtists=3,
    numIncarnations=2,
    numAlbums=2,
    numTracks=2,
    viewLog=False,
)

print("\n" * 20)

# a = track(album=Null, number=1)

