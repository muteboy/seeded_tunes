# -*- coding: utf-8 -*-
import os
from time import strftime, gmtime
from random import choice, randint, random, sample, seed, uniform
import dominate
from dominate.tags import (caption, div, h1, h2, h3, h4, h5, style, table, tbody, td,
                           th, thead, tr)
import isobar as iso
from tqdm import tqdm

# TODO create track, timeline
# TODO create bassline
# TODO create melody 1
# TODO create melody 2
# TODO create drums - (one midi channel, uses notes for different drums)


class track(object):
    def __init__(self, album, number):
        seed(int(f"{album.seed}{number:02d}"))
        self.album = album
        self.number = number
        self.name = self.album.incarn.artist.label.scene.wordList.combineRandomLinesFromFile(
            numWords=randint(1, 2)
        )
        self.nameUnderscore = self.name.replace(" ", "_")
        # beats & steps
        self.beatsPerMinute = randint(50, 160)
        self.beatsPerSecond = self.beatsPerMinute / 60
        self.beatsPerBar = 4
        self.stepsPerBeat = 4  # gives 16 steps per bar
        self.barsPerMinute = self.beatsPerMinute / self.beatsPerBar
        self.stepsPerSecond = self.stepsPerBeat * self.beatsPerSecond
        self.stepsPerBar = self.stepsPerBeat * self.beatsPerBar
        self.barLength = 4
        # goals
        self.minutesGoal = randint(3, 5)
        self.secondsGoal = self.minutesGoal * 60
        self.beatsGoal = self.minutesGoal * self.beatsPerMinute
        self.barsGoal = self.beatsGoal / self.beatsPerBar
        self.barsGoalRound = round(self.barsGoal)
        self.beatsGoalRound = self.barsGoalRound * self.beatsPerBar
        self.stepsGoal = self.beatsGoal * self.stepsPerBeat
        self.stepsRound = self.beatsGoalRound * self.stepsPerBeat
        # calc
        self.secondsRound = self.beatsGoalRound / self.beatsPerSecond
        self.stepLength = 0.25
        self.lengthMMSS = strftime("%M:%S", gmtime(self.secondsRound))
        self.lengthSteps = self.secondsRound * self.stepsPerSecond  # NOT NEEDED TODO
        self.beatsActual = self.barsGoalRound * self.beatsPerBar  # no of bars rounded
        self.bars = round((self.beatsPerMinute * self.minutesGoal) / self.beatsPerBar)
        # isobar setup
        
        
        self.file = f"{self.number:02d}-{self.nameUnderscore}.mid"
        self.isobarOutput = iso.MidiFileOutputDevice(self.file)
        self.timeline = iso.Timeline(self.beatsPerMinute, output_device=self.isobarOutput)
        self.drumDict = {
            "Acoustic Bass Drum": 35,
            "Bass Drum 1": 36,
            "Side Stick": 37,
            "Acoustic Snare": 38,
            "Hand Clap": 39,
            "Electric Snare": 40,
            "Low Floor Tom": 41,
            "Closed Hi Hat": 42,
            "High Floor Tom": 43,
            "Pedal Hi-Hat": 44,
            "Low Tom": 45,
            "Open Hi-Hat": 46,
            "Low-Mid Tom": 47,
            "Hi-Mid Tom": 48,
            "Crash Cymbal 1": 49,
            "High Tom": 50,
            "Ride Cymbal 1": 51,
            "Chinese Cymbal": 52,
            "Ride Bell": 53,
            "Tambourine": 54,
            "Splash Cymbal": 55,
            "Cowbell": 56,
            "Crash Cymbal 2": 57,
            "Vibraslap": 58,
            "Ride Cymbal 2": 59,
            "Hi Bongo": 60,
            "Low Bongo": 61,
            "Mute Hi Conga": 62,
            "Open Hi Conga": 63,
            "Low Conga": 64,
            "High Timbale": 65,
            "Low Timbale": 66,
            "High Agogo": 67,
            "Low Agogo": 68,
            "Cabasa": 69,
            "Maracas": 70,
            "Short Whistle": 71,
            "Long Whistle": 72,
            "Short Guiro": 73,
            "Long Guiro": 74,
            "Claves": 75,
            "Hi Wood Block": 76,
            "Low Wood Block": 77,
            "Mute Cuica": 78,
            "Open Cuica": 79,
            "Mute Triangle": 80,
            "Open Triangle": 81,
        }
        # run gen
        self.drums()
        # TODO calc length
        # try:
        #     self.timeline.run()
        # except:
        #     KeyboardInterrupt
        

    def __str__(self, numTabs=5):
        out = f"{numTabs * chr(9)}Track {self.number:02d}. {self.name}. {self.beatsPerMinute:03d}bpm"
        # out += 
        out += str(vars(self))
        return out

    def binaryPattern(self, numBits=16, threshold=0.5):
        """ return a list of 1s and 0s, with weighting. Used to generate drum patterns """
        return [(1 if random() < threshold else 0) for i in range(1, numBits+1)]

    def drumPattern(self, rest=34, drum=35, threshold=0.5, numBits=16):
        """ return a list of [drum note] or [rest] based on the binary input """
        out = []
        for b in tqdm(self.binaryPattern(numBits, threshold), desc="18 Drum Bits".ljust(18), position=18):
            out.append(drum) if b==1 else out.append(rest)
        return out

    def drums(self):
        kick = choice([35, 36])
        snare = choice([38, 40])
        hho = choice([46, 55])
        hhc = choice([42])
        rest = 34
        self.seqKick = iso.PChoice([kick, rest],[4,8]).nextn(16)
        self.seqSnare = iso.PChoice([snare, rest],[6,10]).nextn(16)
        self.seqHho = iso.PChoice([hho, rest],[4,8]).nextn(16)
        self.seqHhc = iso.PChoice([hhc, rest],[10,6]).nextn(16)
        # self.timeline.schedule({ "note": self.seqKick, "duration": .25, "channel": 9 })
        # self.timeline.schedule({ "note": self.seqSnare, "duration": .25, "channel": 9 })
        # self.timeline.schedule({ "note": self.seqHhc, "duration": .25, "channel": 9 })
        # self.timeline.schedule({ "note": self.seqHho, "duration": .25, "channel": 9 })
        return

    def html(self):
        _tbody = tbody()
        _tbody += tr(
            td(f"{self.number:02d}."),
            td(self.name),
            td(f"{self.beatsPerMinute}bpm"),
            td(self.lengthMMSS),
            td(self.barsPerMinute),
            td(self.stepsPerSecond),
            td(self.stepsPerBar),
            # td(self.minutesGoal),
            td(self.secondsGoal),
            td(self.beatsGoal),
            td(self.barsGoal),
            td(self.barsGoalRound),
            td(self.beatsGoalRound),
            td(self.stepsGoal),
            td(self.stepsRound),
            td(self.secondsRound),
            td(self.stepLength),
            td(self.lengthSteps),
            td(self.beatsActual),
            td(self.bars),
            # td(self.file),
            td(str(self.seqKick)),
            td(str(self.seqSnare)),
            td(str(self.seqHhc)),
            td(str(self.seqHho)),
            )
        return _tbody

    def trackBar(
        self,
        bar,
        patternLength,
        midChan,
        noteLengths,
        notePitches,
        amplitude,
    ):
        bc = []
        # # noteLengths=(genNoteLengths(patternLength=patternLength,patternScale=4))
        # bc.append(";bar " + str(bar))
        # # for step, nl in enumerate(noteLengths, start=0):
        # #     bcLine = []
        # #     # bcLine.append('i "'+instrument+'" '+('0' if (step==0 and bar==0) else '+')+' '+str(nl)+' 4000 '+notePitches[step])
        # #     bcLine.append("0" if (step == 0 and bar == 0) else "+")  # p2 start
        # bc.append(" ".join(bcLine))
        return bc

