# -*- coding: utf-8 -*-
###############################################################################################################
# IMPORT MODULES
###############################################################################################################

import os
import shutil
import webbrowser
from datetime import datetime
from random import choice, randint, random, sample, seed, uniform

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
    link,
    style,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
    span,
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
        self.path = "..\\output\\" + self.pathName.replace(" ", "_")
        if os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)
        os.mkdir(self.path)
        # shutil.rmtree(self.path, ignore_errors=True)
        self.initGraph()
        self.initHTML()
        for num in tqdm(
            range(1, self.numLabels + 1), desc="02 Labels".ljust(18), position=2
        ):
            self.labels.append(label(self, num))
            self.labelPeople += self.labels[num - 1].people
        self.yearFirst = min(a.yearFirst for a in self.labels)
        self.yearLast = max(a.yearLast for a in self.labels)
        self.people = list(set(self.labelPeople))
        if (self.yearFirst == self.yearLast):
            self.name = f"The \"{self.seed}\" Music Scene of {self.yearFirst} CE"
        else:
            self.name = f"The \"{self.seed}\" Music Scene of {self.yearFirst} to {self.yearLast} CE"
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
        self.doc = dominate.document(title="Example HTML")
        self.docPath = f"{self.path}\\Scene_{self.seed}_Log.html"
        # self.docPath = "index.html"
        # f="..\output\Scene_1\..\..\Seeded_Tunes\input\log_styles.css"
        # cssPath = f"{self.path}\\..\\..\\Seeded_Tunes\\input\\log_styles.css"
        # TODO fix styles path
        with self.doc.head:
            # link(rel='stylesheet', href=cssPath)
            style(
                """
                body { font-family: Arial Nova Condensed, FreeSans, sans-serif; margin: 3em 1em; }
                p { font-size: 1em; }
                h1 { font-size: 3em; font-weight: bold; }
                h2 { font-size: 2.6em; font-weight: bold; }
                h3 { font-size: 2.2em; font-weight: bold; }
                h4 { font-size: 1.8em; font-weight: bold; }
                h5 { font-size: 1.4em; font-weight: bold; }
                h6 { font-size: 1em; font-weight: bold; }
                th { border-bottom: 1px solid black; border-collapse: collapse;}
            """
            )

    def graphPeopleLinks(self):
        for p in self.people:
            for _ in p.incarnList:
                # print(i.name)
                return
                # return
                # out += f'{(numTabs+1) * chr(9)}Incarnation: {i.incarnID} {i.name}\n'

    def logScene(self):
        strWidth = 18
        # self.doc += h1(self.name)
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
                    for album in tqdm(
                        incarn.albums, desc="15 Log Albums".ljust(strWidth), position=15
                    ):
                        d += album.html()

        # for person in tqdm(self.people, desc="Log People".ljust(strWidth), position=17):
        # lf.write(str(person) + "\n")
        # lf.close()

        with open(self.docPath, "w") as file:
            file.write(self.doc.render())
        os.startfile(self.docPath)

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
        self.years = []
        for l in self.labels:  # assemble list of release years across all labels.
            for ar in l.artists:
                for incarn in ar.incarnations:
                    self.albums += incarn.albums
                    for al in incarn.albums:
                        self.years.append(al.year)
        self.years = list(dict.fromkeys(self.years))
        # TODO for each year, find all the incarnations with yearfirst the same
        # with self.gvGraph.subgraph(name='hello') as gvs:
        # self.gvGraph.subgraph(name='hello').attr(kw='graph',rank='same')
        # for y in self.years:
        #     yearIncarns=[]
        #     for l in self.labels:
        #         for ar in l.artists:
        #             for inc in ar.incarnations:
        #                 if inc.yearFirst == y:
        #                     yearIncarns.append(inc.name)
        #     with self.gvGraph.subgraph(name=y) as gvs:
        #         gvs.graph_attr['rank']='same'
        #         for yi in yearIncarns:
        #             gvs.node(name=yi)
        # print(dir(self.people))
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

