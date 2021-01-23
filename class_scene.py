# -*- coding: utf-8 -*-

import os
import shutil
import webbrowser
from collections import defaultdict
from datetime import datetime
from random import choice, randint, random, sample, seed, uniform
import pdfkit

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
    link,
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
from graphviz import Digraph, nohtml
from tqdm import tqdm

from class_label import label
from class_person import person
from class_wordList import wordList

yearNow = datetime.today().year


class scene(object):
    def __init__(
        self,
        seedInt,
        numLabels,
        yearStart,
        viewGv,
        numArtists,
        numIncarnations,
        numAlbums,
        numTracks,
    ):
        self.seed = seedInt
        seed(self.seed)
        self.yearNow = datetime.today().year
        self.years = []
        self.labels = []
        self.yearStart = yearStart
        self.labelPeople = []  # people collected from the labels
        self.wordList = wordList()
        self.numLabels = randint(1, 6) if numLabels == 0 else numLabels
        self.numArtists = numArtists
        self.numAlbums = numAlbums
        self.numTracks = numTracks
        self.numIncarnations = numIncarnations
        self.people = self.scenePeople(randint(40, 100))
        self.pathName = f"Scene_{self.seed}"
        self.path = "..\\seeded_tunes_output\\" + self.pathName.replace(" ", "_")
        if os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)
        os.mkdir(self.path)
        # shutil.rmtree(self.path, ignore_errors=True)
        self.initGraph()
        for num in tqdm(
            range(1, self.numLabels + 1), desc="02 Labels".ljust(18), position=2
        ):
            self.labels.append(label(self, num))
            self.labelPeople += self.labels[num - 1].people
        self.yearFirst = min(a.yearFirst for a in self.labels)
        self.yearLast = max(a.yearLast for a in self.labels)
        self.people = list(set(self.labelPeople))
        if self.yearFirst == self.yearLast:
            self.name = f'The "{self.seed}" Music Scene of {self.yearFirst} CE'
        else:
            self.name = f'The "{self.seed}" Music Scene of {self.yearFirst} to {self.yearLast} CE'
        self.initHTML()
        self.logScene()
        self.graphScene()
        self.graphPeopleLinks()
        # os.rename(self.path + "_NEW", self.path)
        self.gvGraph.render(
            self.gvGraph.filename, view=True
        ) if viewGv else self.gvGraph.render(self.gvGraph.filename, view=False)

    def scenePeople(self, numPeople):
        """ Returns list of people """
        p = []
        for _ in tqdm(range(numPeople), desc="01 Scene People".ljust(18), position=1):
            p.append(person())
        return p

    def __str__(self):
        """ prints Scene info """
        return f"Scene: {self.name}\n # of Labels: {self.numLabels}"

    def initGraph(self):
        """ Initialise GraphViz graph """
        # gvFont = "Oswald"
        gvFont = "Arial"
        self.gvGraph = Digraph(
            name=self.pathName,
            filename=f"{self.path}\\{self.seed}_{self.pathName}_Family_Tree.gv",
            format="svg",
        )
        self.gvGraph.graph_attr.update(
            # fontname=gvFont,
            fontname=gvFont,
            fontsize="14",
            nodesep="0",
            splines="ortho",
            rankdir="TB",
            compound="true",
            labelloc="top",
            forcelabels="true",
        )
        self.gvGraph.node_attr.update(
            margin="0",
            # height="0.3",
            fontname=gvFont,
            style="filled",
            color="black",
            fillcolor="grey95",
            shape="plaintext",
            fontsize="10",
            # labeljust="l",
        )
        self.gvGraph.edge_attr.update(arrowhead="none", fontname=gvFont, fontsize="6")

    def initHTML(self):
        self.doc = dominate.document(title=f"Scene Log for {self.name}")
        self.docFileBase = f"Scene_{self.seed}_Log"
        self.docPathHtml = f"{self.path}\\{self.docFileBase}.html"
        self.docPathPdf =  f"{self.path}\\{self.docFileBase}.pdf"
        with self.doc.head:
            style(
                """
                body { font-family: Arial Nova Condensed, FreeSans, sans-serif; margin: 3em 1em; }
                p { font-size: 1em; }
                div#label { margin-left: 2%;}
                div#artist { margin-left: 4%; }
                div#incarn { margin-left: 6%; }
                div#album { margin-left: 8%; }
                div#format { margin-left: 10%; }
                h1 { font-size: 3em; font-weight: bold; }
                h2 { font-size: 2.6em; font-weight: bold; }
                h3 { font-size: 2.2em; font-weight: bold; }
                h4 { font-size: 1.8em; font-weight: bold; }
                h5 { font-size: 1.4em; font-weight: bold; }
                h6 { font-size: 1em;   font-weight: bold; }
                table { border-collapse: collapse; }
                th { border-bottom: 1px solid black; }
            """
            )

    def graphPeopleLinks(self):
        for p in self.people:
            for _ in p.incarnList:
                return
                # return

    def logScene(self):
        strWidth = 18
        d = self.doc
        d += h1(self.name)
        for label in tqdm(
            self.labels, desc="12 Log Labels".ljust(strWidth), position=12
        ):
            d += label.html()
            # loop through artists
            for artist in tqdm(
                label.artists, desc="13 Log Artists".ljust(strWidth), position=13
            ):
                d += artist.html()
                # loop through incarnations
                for incarn in tqdm(
                    artist.incarnations,
                    desc="14 Log Incarns".ljust(strWidth),
                    position=14,
                ):
                    d += incarn.html()
                    # loop through albums
                    # TODO include artwork in log
                    # TODO include catalogue numbers 
                    for album in tqdm(
                        incarn.albums, desc="15 Log Albums".ljust(strWidth), position=15
                    ):
                        d += album.html()
        with open(self.docPathHtml, "w", encoding="utf8") as file:
            file.write(self.doc.render())
        os.startfile(self.docPathHtml)
        pdfkit.from_file(self.docPathHtml,self.docPathPdf) 
        # os.startfile(self.docPathPdf)

    def graphScene(self):
        """ Scene GraphViz, including artists and albums """
        self.gvGraph.attr(
            label=self.name,
            labelloc="top",
            # fontsize="16",
            # fontweight="bold",
            # compound="true",
        )
        # self.gvGraph.subgraph(graph_attr['rank']='same')
        self.albums = []
        self.incarnsAll = []
        for (
            l
        ) in (
            self.labels
        ):  # assemble list of release years across all labels. AND list of incarnations
            for ar in l.artists:
                self.incarnsAll += ar.incarnations
                for incarn in ar.incarnations:
                    self.albums += incarn.albums
                    for al in incarn.albums:
                        self.years.append(al.year)
        self.years = list(dict.fromkeys(self.years))
        yearGroups = defaultdict(list)
        for obj in self.incarnsAll:
            yearGroups[obj.yearFirst].append(obj)
        # new_list = groups.values()
        self.incarnsAllGroupedByYear = sorted(
            yearGroups.values(), key=lambda i: i[0].yearFirst
        )
        # TODO rank same incarns by year in subgraphs.
        # for yearGroup in self.incarnsAllGroupedByYear:
        #     sg = Digraph(name=yearGroup[0].yearFirst)
        #     sg.attr(kw="graph", rank="same")
        #     for incarn in yearGroup:
        #         incarn.graphIncarnation(sg)
        #     self.gvGraph.subgraph(sg)

        # link people who joined new group
        for p in self.people:
            p.incarnList = sorted(p.incarnList, key=lambda i: i.yearFirst)
            for i, j in zip(p.incarnList, p.incarnList[1:]):
                if i.artist == j.artist:
                    pass
                else:
                    self.gvGraph.edge(
                        tail_name=i.name,
                        head_name=j.name,
                        xlabel=f"{p.fullname} joined",
                    )

