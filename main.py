# -*- coding: utf-8 -*-

import sys
from random import choice, randint, random, sample, seed, uniform


from class_scene import scene
from class_track import track


sceneCurrent = scene(
    # seedInt=100672,
    seedInt=sys.argv[1],
    numLabels=1,
    yearStart=1972,
    viewGv=True,
    numArtists=1,
    numIncarnations=1,
    numAlbums=1,
    numTracks=2,
)
print("\n" * 20)

# a = track(album=Null, number=1)

