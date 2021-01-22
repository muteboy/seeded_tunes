# -*- coding: utf-8 -*-

import sys
from random import choice, randint, random, sample, seed, uniform


from class_scene import scene
from class_track import track

defaultSeed=100672
inputSeed = int(input(f"Enter seed number, or hit Enter for default ({defaultSeed}): ") or defaultSeed)


sceneCurrent = scene(
    seedInt=inputSeed,
    # seedInt=sys.argv[1],
    numLabels=2,
    yearStart=1972,
    viewGv=True,
    numArtists=3,
    numIncarnations=2,
    numAlbums=2,
    numTracks=2,
)
# TODO make num incarns, albums, tracks all MAX these options, random in the range

print("\n" * 20)

# a = track(album=Null, number=1)

