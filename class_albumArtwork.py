# # -*- coding: utf-8 -*-
import colorsys
import math
import textwrap
from random import choice, randint, random, sample, seed, uniform

import svgwrite
from tqdm import tqdm


class albumArtwork(object):
    def __init__(self, album, albumFormat):
        self.album = album
        self.albumFormat = albumFormat
        

        self.artColorOutline = self.album.artColorOutline
        self.artColorBG = self.album.artColorOutline
        self.artColorText = self.album.artColorText

        self.formatType = self.albumFormat.formatType
       # set art dimension W and H the same
        self.artDim = 210
        # add SVG symbols to
        self.makeSvgSymbols()
        # self.makeSvgLogo()
        if self.formatType == "MC":
            self.artworkCassette()  # TODO make cassettes work
        elif self.formatType == "CD":
            self.artworkCdBooklet()  # TODO make CD booklet work
            self.artworkCdTray()  # TODO make cd tray work
        elif self.formatType == "12":
            self.artwork12in()
        elif self.formatType == "PS":
            self.artworkPoster()

    def svgSymbolLogo(self):
        symbolLogo = self.svgSymbols.g(id="logo")
        svgPattern45Stripe = self.svgSymbols.pattern(
            size=(1, 1), patternUnits="userSpaceOnUse"
        )
        self.svgSymbols.defs.add(svgPattern45Stripe)
        svgPattern45Stripe.add(
            self.svgSymbols.line(
                start=(0, 1), end=(1, 0), stroke_width=0.1, stroke="white",
            )
        )
        logoDim = 10

        # main rectangle
        symbolLogo.add(
            self.svgSymbols.rect(
                size=(logoDim, logoDim),
                fill="none",
                stroke_width=f"{logoDim / 36}",
                stroke="white",
            )
        )
        # lower filled rectangle
        symbolLogo.add(
            self.svgSymbols.rect(
                insert=(0, ((logoDim / 3) * 2)),
                size=(logoDim, (logoDim / 3)),
                fill=svgPattern45Stripe.get_paint_server(),
                stroke_width="0.2",
                stroke="white",
            )
        )
        # straight lines
        symbolLogo.add(
            self.svgSymbols.path(
                d=f"M {logoDim / 2} {logoDim / 3} L {logoDim / 2} {(logoDim / 6) * 5}",
                stroke_width="0.2",
                stroke="white",
            )
        )
        # seed
        symbolLogo.add(
            self.svgSymbols.circle(
                center=((logoDim / 2), ((logoDim / 6) * 5)),
                r=(logoDim / 20),
                fill="white",
            )
        )
        # leaves
        symbolLogo.add(
            self.svgSymbols.path(
                d=f"M {logoDim / 2} {logoDim / 3} a 1 1 0 0 1 {logoDim /3} 0 z a 1 1 0 0 0 {-(logoDim /3)} 0 z ",
                stroke_width="0.2",
                stroke="white",
                fill="none",
            )
        )
        # self.svgSymbols.defs.add(symbolLogo)
        return symbolLogo

    def svgSymbolRect(self):
        symbolRect = self.svgSymbols.g(id="rect")
        symbolRect.add(self.sym.rect(size=(210, 210), fill="white"))
        symbolRect.add(self.sym.circle(center=(50, 100), r=(30), fill="red"))
        return symbolRect

    def svgSymbol3Triangles(self):
        symbolArt3Triangles = self.svgSymbols.g(id="3triangles", stroke_width="0")
        for _ in range(1, 4):
            symbolArt3Triangles.add(
                self.svgSymbols.polygon(
                    [
                        [randint(1, self.artDim), randint(1, self.artDim)],
                        [randint(1, self.artDim), randint(1, self.artDim)],
                        [randint(1, self.artDim), randint(1, self.artDim)],
                    ],
                    fill="white",
                )
            )
        return symbolArt3Triangles

    def svgSymbol4Quads(self):
        symbolArt4Quadrants = self.svgSymbols.g(
            id="4quadrants", stroke_width="0", fill="white"
        )
        dim100 = self.artDim
        dim050 = dim100 / 2
        gap = 4
        nwx = randint(gap, dim050 - gap)
        nwy = randint(gap, dim050 - gap)
        nex = randint(gap, dim050 - gap)
        ney = randint(gap, dim050 - gap)
        swx = randint(gap, dim050 - gap)
        swy = randint(gap, dim050 - gap)
        sex = randint(gap, dim050 - gap)
        sey = randint(gap, dim050 - gap)
        symbolArt4Quadrants.add(
            self.svgSymbols.path(
                d=f"M {dim050 - (gap/2)} {dim050 - (gap/2)} v {-nwy} a {nwx} {nwy} 0 0 0 {-nwx} {nwy} z ",
            )
        )
        symbolArt4Quadrants.add(
            self.svgSymbols.path(
                # M 50 40 v -25 a 30 40 0 0 1 30 25 z
                d=f"M {dim050 + (gap/2)} {dim050 - (gap/2)} v {-ney} a {nex} {ney} 0 0 1 {nex} {ney} z ",
            )
        )
        symbolArt4Quadrants.add(
            self.svgSymbols.path(
                # M 40 50 v 15 a 25 15 0 0 1 -25 -15 z
                d=f"M {dim050 - (gap/2)} {dim050 + (gap/2)} v {swy} a {swx} {swy} 0 0 1 {-swx} {-swy} z ",
            )
        )
        symbolArt4Quadrants.add(
            self.svgSymbols.path(
                # M 50 50 v 13 a 14 13 0 0 0 14 -13 z
                d=f"M {dim050 + (gap/2)} {dim050 + (gap/2)} v {sey} a {sex} {sey} 0 0 0 {sex} {-sey} z ",
            )
        )
        return symbolArt4Quadrants

    def svgSymbolCircles(self):
        symbolArtCircles = self.svgSymbols.g(id="circles")
        for _ in range(1, randint(10, 20)):
            symbolArtCircles.add(
                self.svgSymbols.circle(
                    center=((self.artDim / 2), (self.artDim / 2)),
                    r=randint(1, (self.artDim / 2)),
                    stroke_width=(uniform(0.05, 8)),
                    stroke="white",
                    fill="none",
                )
            )
        return symbolArtCircles

    def svgSymbolRays(self):
        symbolArtRays = self.svgSymbols.g(id="rays", clip_path="url(#clipSquare)")
        # for _ in range(1, randint(1, 3) + 1):
        for _ in range(1, 5):
            # angle1 = (i / (numCirclePoints/2)) * math.pi
            angle1 = uniform(0, (2 * math.pi))
            angle2 = angle1 + (uniform(-1, 1))
            # radius1 = randint(1, (self.artDim * 0.8))
            radius1 = 10
            # radius2 = randint(1, (self.artDim * 0.2))
            radius2 = 60
            r1x1 = (radius1 * math.cos(angle1)) + (self.artDim / 2)
            r1y1 = (radius1 * math.sin(angle1)) + (self.artDim / 2)
            r1x2 = (radius1 * math.cos(angle2)) + (self.artDim / 2)
            r1y2 = (radius1 * math.sin(angle2)) + (self.artDim / 2)
            r2x1 = (radius2 * math.cos(angle1)) + (self.artDim / 2)
            r2y1 = (radius2 * math.sin(angle1)) + (self.artDim / 2)
            r2x2 = (radius2 * math.cos(angle2)) + (self.artDim / 2)
            r2y2 = (radius2 * math.sin(angle2)) + (self.artDim / 2)
            symbolArtRays.add(
                self.svgSymbols.polygon(
                    [[r1x1, r1y1], [r1x2, r1y2], [r2x2, r2y2], [r2x1, r2y1]],
                    fill="white",
                )
            )
        return symbolArtRays

    def svgSymbol1Circle(self):
        symbol1Circle = self.svgSymbols.g(id="1circle")
        symbol1Circle.add(
            self.svgSymbols.circle(
                id="circle", center=(105, 105), r=(105), fill="white"
            )
        )
        return symbol1Circle

    def svgSymbolHalfCircleEmpty(self):
        symbolHalfCircleEmpty = self.sym.g(
            id="halfcircleempty", fill="none", stroke_width="5", stroke="white"
        )
        if random() > 0.5:
            symbolHalfCircleEmpty.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolHalfCircleEmpty.add(
            self.sym.path(
                d=f"M 0 0 A {self.artDim/2} {self.artDim/2} 0 0 0 {self.artDim} 0 z",
                fill="none",
            )
        )
        symbolHalfCircleEmpty.rotate(
            (randint(0, 3) * 90), center=((self.artDim / 2), (self.artDim / 2))
        )
        return symbolHalfCircleEmpty

    def svgSymbolCircleEmpty(self):
        symbolCircleEmpty = self.sym.g(
            id="circleempty", fill="none", stroke_width="5", stroke="white"
        )
        if random() > 0.5:
            symbolCircleEmpty.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolCircleEmpty.add(
            self.sym.circle(
                center=((self.artDim / 2), (self.artDim / 2)),
                r=(self.artDim * 0.45),
                fill="none",
            )
        )
        return symbolCircleEmpty

    def makeSvgSymbols(self):
        self.albumArtworkSymbolLibraryPath = (
            self.album.incarn.artist.label.scene.path + "\\symbolLibrary.svg"
        )
        # create SVG object to contain all symbols for all formats of artwork
        self.svgSymbols = svgwrite.Drawing(
            self.albumArtworkSymbolLibraryPath,
            # size=("1000mm", "1000mm"),
            # viewBox=("0 0 1000 1000"),
            profile="full",
            id="symbols",
        )
        self.sym = self.svgSymbols
        # define clip path for symbols
        clip_path = self.svgSymbols.defs.add(self.svgSymbols.clipPath(id="clipSquare"))
        clip_path.add(
            self.svgSymbols.rect(
                (0, 0),
                (self.artDim, self.artDim),
                stroke="white",
                stroke_width="0.4",
                fill="none",
            )
        )
        self.sym.defs.add(self.artworkDesign())

        # region logo pattern
        # define logo hatch pattern in defs
        # svgLogoPattern = self.sym.defs.add(
        #     self.svgSymbols.pattern(size=(1, 1), patternUnits="userSpaceOnUse")
        # )
        # # add logo hatch pattern to Pattern defs
        # svgLogoPattern.add(
        #     self.svgSymbols.line(
        #         start=(0, 1), end=(1, 0), stroke_width=0.1, stroke="white"
        #     )
        # )
        # # endregion

        # region define diagonal half fill
        # symbolArtDiagHalfFill = self.sym.g(
        #     id="diag_half_fill", clip_path="url(#clipSquare)"
        # )
        # self.sym.defs.add(
        #     self.sym.path(d=f"M 0 0 L {self.artDim} 0 {self.artDim} {self.artDim} Z")
        # )
        # endregion

        # region define angle - square with 90 degree angle
        symbolAngle = self.sym.g(
            id="angle", fill="none", stroke_width="5", stroke="white"
        )
        self.sym.defs.add(symbolAngle)
        if random() > 0.5:
            symbolAngle.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolAngle.add(
            self.sym.path(d=f"M {self.artDim/2} 0 v {self.artDim/2} h {self.artDim/2}")
        )
        symbolAngle.rotate(
            (randint(0, 3) * 90), center=((self.artDim / 2), (self.artDim / 2))
        )
        # endregion

        # region define sector - square with quarter circle
        symbolSector = self.sym.g(
            id="sector", fill="none", stroke_width="5", stroke="white"
        )
        self.sym.defs.add(symbolSector)
        if random() > 0.5:
            symbolSector.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolSector.add(
            self.sym.path(
                d=f"M {self.artDim/2} 0 A {self.artDim/2} {self.artDim/2} 0 0 0 {self.artDim} {self.artDim/2}"
            )
        )
        symbolSector.rotate(
            (randint(0, 3) * 90), center=((self.artDim / 2), (self.artDim / 2))
        )
        # endregion

        # region define halfcirclefilled
        symbolHalfCircleFilled = self.sym.g(
            id="halfcirclefilled", fill="none", stroke_width="5", stroke="white"
        )
        self.sym.defs.add(symbolHalfCircleFilled)
        if random() > 0.5:
            symbolHalfCircleFilled.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolHalfCircleFilled.add(
            self.sym.path(
                d=f"M 0 0 A {self.artDim/2} {self.artDim/2} 0 0 0 {self.artDim} 0 z",
                fill="white",
            )
        )
        symbolHalfCircleFilled.rotate(
            (randint(0, 3) * 90), center=((self.artDim / 2), (self.artDim / 2))
        )
        # endregion

        # region define diagonal

        symbolDiagonal = self.sym.g(
            id="diagonal", fill="none", stroke_width="5", stroke="white"
        )
        self.sym.defs.add(symbolDiagonal)
        if random() > 0.5:
            symbolDiagonal.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolDiagonal.add(self.sym.path(d=f"M 0 0 L {self.artDim} {self.artDim}"))
        symbolDiagonal.rotate(
            (randint(0, 1) * 90), center=((self.artDim / 2), (self.artDim / 2))
        )
        # endregion

        # region define circle filled
        symbolCircleFilled = self.sym.g(
            id="circlefilled", fill="none", stroke_width="5", stroke="white"
        )
        self.sym.defs.add(symbolCircleFilled)
        if random() > 0.5:
            symbolCircleFilled.add(self.sym.rect(size=(self.artDim, self.artDim),))
        symbolCircleFilled.add(
            self.sym.circle(
                center=((self.artDim / 2), (self.artDim / 2)),
                r=(self.artDim * 0.45),
                fill="white",
            )
        )
        # endregion

        # region define reeds
        symbolReeds = self.sym.g(
            id="reeds", fill="none", stroke_width="1", stroke="white"
        )
        self.sym.defs.add(symbolReeds)
        if random() > 0.5:
            symbolReeds.add(self.sym.rect(size=(self.artDim, self.artDim),))
        reedsNum = randint(6, 12)
        reedsSpacing = self.artDim / reedsNum

        for i in range(1, reedsNum + 1):
            symbolReeds.add(
                self.sym.path(
                    d=f"M {i * reedsSpacing} 0 v {randint((self.artDim / 3), self.artDim)}"
                )
            )

        # endregion

        self.sym.defs.add(self.svgSymbolRect())
        self.sym.defs.add(self.svgSymbol3Triangles())
        self.sym.defs.add(self.svgSymbol4Quads())
        self.sym.defs.add(self.svgSymbolCircles())
        self.sym.defs.add(self.svgSymbolRays())
        self.sym.defs.add(self.svgSymbol1Circle())
        self.sym.defs.add(self.svgSymbolHalfCircleEmpty())
        self.sym.defs.add(self.svgSymbolCircleEmpty())
        self.sym.defs.add(self.svgSymbolLogo())

    def artworkDesign(self):
        """ create artwork design as a symbol for use by all formats """
        # TODO move artwork design to here
        symbolArtworkDesign = self.sym.g(
            id="art", fill="none", stroke_width="1", stroke="white"
        )
        symbolArtworkDesign.add(self.sym.rect(size=(20,20),))
        # TODO add design to the group here

        return symbolArtworkDesign


    def artworkOutline(self, dwg, stroke, strokeWidth, fill, strokeDasharray, rectDims):
        self.group = dwg.add(
            dwg.g(
                id="outline",
                stroke=stroke,
                stroke_width="0.2",
                fill=self.artColorBG,
                stroke_dasharray=strokeDasharray,
            )
        )
        for r in rectDims:
            self.group.add(dwg.rect((r[0][0], r[0][1]), (r[1][0], r[1][1])))
        return self.group

    def artworkTextOneLine(
        self,
        dwg,
        fontSize,
        x,
        y,
        textAnchor="start",
        fontWeight="normal",
        text="Default Text",
        id="defaultId",
        fontFamily="Alte Haas Grotesk",
        rotate90=False,
    ):
        if rotate90 == True:
            transform = f"rotate(90 {x} {y})"
        else:
            transform = "rotate(0)"
        self.textGroup = dwg.add(
            dwg.g(
                id=id,
                fill=self.artColorText,
                stroke=self.artColorText,
                font_family=fontFamily,
                text_anchor=textAnchor,
                stroke_width="0",
                font_weight=fontWeight,
                font_size=fontSize,
            )
        )
        self.textGroup.add(dwg.text(text, insert=(x, y), transform=transform))
        return self.textGroup

    def artworkTextMultiTrackNames(
        self,
        dwg,
        fontSize,
        x,
        y,
        textAnchor,
        textLines,
        id,
        lineSpacing,
        fontFamily="Alte Haas Grotesk",
        rotate90=False,
        fontWeight="normal",
    ):
        if rotate90 == True:
            transform = f"rotate(90 {x} {y})"
        else:
            transform = "rotate(0)"
        self.group = dwg.add(
            dwg.g(
                id=id,
                fill=self.artColorText,
                stroke=self.artColorText,
                font_family=fontFamily,
                text_anchor=textAnchor,
                stroke_width="0",
                font_size=fontSize,
                font_weight=fontWeight,
            )
        )
        for i, t in enumerate(textLines):
            self.group.add(
                dwg.text(
                    f"{i+1}.", insert=(x, (y + (i * lineSpacing))), transform=transform,
                )
            )
            self.group.add(
                dwg.text(
                    f"{t.name}",
                    insert=((x + 10), (y + (i * lineSpacing))),
                    transform=transform,
                )
            )
        return self.group

    def svgMarkers(self, dwg, width, height, stepSize, show=False):
        markers = dwg.add(
            dwg.g(
                id="markers",
                stroke=self.artColorOutline,
                stroke_width="0",
                fill=self.artColorOutline,
                font_family="Arial Narrow",
            )
        )
        if show == True:
            for mx in tqdm(range(0, width, stepSize), desc="SVG Markers", position=7):
                for my in range(0, height, stepSize):
                    markers.add(
                        dwg.text(f"{mx},{my}", insert=(mx, my), font_size="0.5mm")
                    )
                    markers.add(dwg.circle(center=(mx, my), r=0.3))
        else:
            pass
        return markers

    def svgShapeGrid(
        self,
        id="shapegrid",
        shapeUsed=0,
        gridSize=6,
        width=1000,
        height=1000,
        fractionOfCell=0.7,
    ):
        dwg = svgwrite.Drawing(
            f"{id}.svg",
            size=(f"{width}mm", f"{height}mm"),
            viewBox=(f"0 0 {width} {height}"),
            profile="full",
        )
        seed(self.album.seed)
        cellSize = width / gridSize
        dwg.add(dwg.rect(insert=(0, 0), size=(width + 20, height + 20), fill="#545454"))
        gridShapeSymbol1 = dwg.symbol(id="gridShape1")
        gridShapeSymbol2 = dwg.symbol(id="gridShape2")
        dwg.defs.add(gridShapeSymbol1)
        dwg.defs.add(gridShapeSymbol2)
        gridShapeSymbols = [
            # dwg.line(start=(-cellSize, (cellSize/2)), end=((cellSize*2),(cellSize/2)), transform=f'rotate({randint(0,180)} {cellSize/2} {cellSize/2})'),
            dwg.path(
                d=f"M 0 {cellSize*0.2} h {cellSize} M 0 {cellSize*0.4} h {cellSize} M 0 {cellSize*0.6} h {cellSize} M 0 {cellSize*0.8} h {cellSize}",
                stroke_width="3",
            ),  # 4 stripes
            dwg.rect(
                insert=(0, 0), size=(cellSize, cellSize), fill="white", stroke_width="1"
            ),  # square
            dwg.path(
                d=f"M 0 0 L {cellSize} 0 0 {cellSize} Z", fill="white", stroke_width="1"
            ),  # corner triangle
            dwg.path(
                d=f"M -2 -2 L {cellSize+2} {cellSize+2}",
                stroke="white",
                stroke_width="1",
                stroke_linecap="butt",
            ),  # Slash
            dwg.path(
                d=f"M 1 0 A {(cellSize-2)/2} {(cellSize-2)/2} 0 0 0 {cellSize-1} 0 ",
                fill="none",
                stroke_width="1",
            ),  # empty semicircle
            dwg.path(
                d=f"M 1 0 A {(cellSize-2)/2} {(cellSize-2)/2} 0 0 0 {cellSize-1} 0 Z",
                fill="white",
                stroke_width="1",
            ),  # filled semicircle
            dwg.path(
                d=f"M {cellSize/2} 0 v {cellSize/2} h {cellSize/2}",
                fill="none",
                stroke_width="1",
            ),  # 90 angle
            dwg.path(
                d=f"M 0 {-(cellSize/2)} A {cellSize/2} {cellSize/2} 0 0 1 0 {cellSize/2}",
                fill="none",
                stroke_width="1",
            ),  # empty quarter circle
            dwg.path(
                d=f"M 0 {-(cellSize/2)} A {cellSize/2} {cellSize/2} 0 0 1 0 {cellSize/2}",
                fill="white",
                stroke_width="1",
            ),  # filled quarter circle
            dwg.circle(
                center=((cellSize / 2), (cellSize / 2)),
                r=(cellSize * 0.4),
                fill="white",
            ),  # filled circle
            dwg.circle(
                center=((cellSize / 2), (cellSize / 2)), r=(cellSize * 0.4), fill="none"
            ),  # empty circle
        ]
        shapeSample = sample(gridShapeSymbols, k=2)
        gridShapeSymbol1.add(shapeSample[0])
        gridShapeSymbol2.add(shapeSample[1])
        # gridShapeSymbol1.add(choice(gridShapeSymbols))
        # gridShapeSymbol2.add(choice(gridShapeSymbols))
        rotateAmount = randint(0, 3) * 90
        for row in range(0, gridSize):
            for column in range(0, gridSize):
                if random() > 0.5:
                    shapeUsed = gridShapeSymbol1
                else:
                    shapeUsed = gridShapeSymbol2
                dwg.add(
                    dwg.use(
                        shapeUsed,
                        insert=((column * cellSize), (row * cellSize)),
                        size=(cellSize, cellSize),
                        stroke_width="1",
                        stroke="white",
                        transform=f"rotate({rotateAmount} {(column*cellSize)+(cellSize/2)} {(row*cellSize)+(cellSize/2)})",
                    )
                )
                # dwg.add(dwg.text(f'{row}/{column}', insert=((column*cellSize), (row*cellSize)+4), font_size=3, font_family='Arial'))
        dwg.save()
        return

    def artworkCassette(self):
        width = 190
        height = 120
        svgCassette = svgwrite.Drawing(
            self.album.path + "\\Artwork_Cassette.svg",
            size=(f"{width}mm", f"{height}mm"),
            viewBox=(f"0 0 {width} {height}"),
            profile="full",
        )
        svgCassette.add(
            self.artworkOutline(
                svgCassette,
                self.artColorOutline,
                "0.2",
                self.artColorBG,
                "1",
                [
                    # background
                    [(0, 0), (26, 101)],
                    [(26, 0), (13, 101)],
                    [(39, 0), (65, 101)],
                    [(103, 0), (64, 101)],
                ],
            )
        )
        # dwg.defs.add(self.artworkLogoSymbol(svgCassette))
        # svgCassette.add(svgCassette.use(self.artworkLogoSymbol(svgCassette), insert=(28,90), size=(9,9)))
        # svgCassette.add(svgCassette.use(self.artworkLogoSymbol(svgCassette), insert=(41,90), size=(9,9)))
        # svgCassette.add(self.artworkLogo(svgCassette, 9, 9, 28, 90))
        # svgCassette.add(self.artworkLogo(svgCassette, 9, 9, 41, 90))
        # svgCassette.add(self.artworkSelect(svgCassette, 60, 60, 41, 24))
        # svgCassette.add(self.artworkSelect(svgCassette, 60, 60, 105, 38))

        for i, t in enumerate(textwrap.wrap(self.album.trackNamesText, 90)):
            fSize = 2.4
            svgCassette.add(
                self.artworkTextOneLine(
                    svgCassette,
                    str(fSize),
                    22 - ((fSize + 0.1) * i),
                    2,
                    text=t,
                    rotate90=True,
                )
            )
        for i, t in enumerate(textwrap.wrap(self.album.trackNamesText, 40)):
            svgCassette.add(
                self.artworkTextOneLine(
                    svgCassette,
                    str(fSize),
                    105,
                    4 + ((fSize + 0.1) * i),
                    text=t,
                    rotate90=False,
                )
            )
        svgCassette.add(
            self.artworkTextMultiTrackNames(
                svgCassette,
                "2.4",
                105,
                4,
                "start",
                textLines=self.album.tracks,
                id="tracklist",
                lineSpacing=2.5,
            )
        )
        # textLines = [
        # #	size, x, y, anchor, weight, text, id, font, transform,
        # 	[svgCassette, '5', 101, 6, 'end', 'bold', self.album.artist.name, 'artistNameFront', 'Alte Haas Grotesk', False],
        # 	[svgCassette, '5', 101, 12, 'end', 'normal', self.album.name, 'albumNameFront', 'Alte Haas Grotesk', False],
        # 	[svgCassette, '3.5', 34, 2, 'start', 'bold', self.album.artist.name, 'artistNameSpine', 'Alte Haas Grotesk', True],
        # 	[svgCassette, '2', 32, 89, 'end', 'normal', self.album.catNo, 'catNoSpine', 'Alte Haas Grotesk', True],
        # 	[svgCassette, '3.5', 29, 2, 'start', 'normal', self.album.name, 'albumNameSpine', 'Alte Haas Grotesk', True],
        # 	[svgCassette, '3', 51, 95.5, 'start', 'normal', self.album.artist.label.name, 'labelNameFront', 'Alte Haas Grotesk', False],
        # 	[svgCassette, '2', 0, 101, 'end', 'normal', self.album.seed, 'pixelSeed', 'SeedBinaryPixel', True],
        # 	[svgCassette, '2', 8, 2, 'start', 'normal', f'All titles written by {" / ".join([p.surname for p in self.album.people])}', 'Flapcredit', 'Alte Haas Grotesk', True],
        # 	[svgCassette, '2', 2, 2, 'start', 'normal', f'©{self.album.year}  {self.album.artist.label.name} \N{BULLET} {self.album.catNo}', 'FlapCopyright', 'Alte Haas Grotesk', True],
        # 	[svgCassette, '2', 5, 2, 'start', 'normal', self.album.svgTagline, 'tagline', 'Alte Haas Grotesk', True],
        # 	]
        # for t in textLines:
        # 	svgCassette.add(self.artworkTextOneLine(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9]))
        # 	# pass
        svgCassette.defs.add(self.svgSymbols)
        svgCassette.add(self.svgSymbols.use(href="#circle"))
        svgCassette.add(self.svgMarkers(svgCassette, 170, 110, 10, show=False))
        svgCassette.save()
        return

    def artworkCdBooklet(self):
        svgCdBooklet = svgwrite.Drawing(
            self.album.path + "\\Artwork_CD_Booklet.svg",
            size=("240mm", "120mm"),
            viewBox=("0 0 240 120"),
            profile="full",
        )
        filterBlur = svgCdBooklet.defs.add(svgCdBooklet.filter())
        filterBlur.feGaussianBlur(in_="SourceGraphic", stdDeviation=0.2)
        svgCdBooklet.add(
            self.artworkOutline(
                svgCdBooklet,
                self.artColorOutline,
                "0.2",
                self.artColorBG,
                "1",
                [[(0, 0), (120, 120)], [(120, 0), (120, 120)],],
            )
        )
        # svgCdBooklet.add(self.artworkLogo(svgCdBooklet, 10, 10, 220, 105)) TODO USE SYMBOL
        svgCdBooklet.add(
            self.artworkTextOneLine(
                svgCdBooklet, "5", 230, 17, "end", text=self.album.name, id="albumName"
            )
        )
        # svgCdBooklet.add(self.artworkSelect(svgCdBooklet, 80, 80, 150, 20))
        # svgCdBooklet.add(self.artworkSelect(svgCdBooklet, 50, 50, 60, 60))
        textLines = [
            # 	size, x, y, anchor, weight, text, id, font, transform,
            [
                svgCdBooklet,
                "5",
                230,
                10,
                "end",
                "bold",
                self.album.incarn.artist.name,
                "artistNameFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdBooklet,
                "5",
                230,
                17,
                "end",
                "normal",
                self.album.name,
                "albumNameFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdBooklet,
                "2",
                10,
                10,
                "start",
                "normal",
                self.album.svgTagline,
                "tagline",
                "Alte Haas Grotesk",
                False,
            ],
            # [svgCdBooklet, '2', 10, 15, 'start', 'normal', f'All titles written by {" / ".join([p.surname for p in self.album.people])}', 'Flapcredit', 'Alte Haas Grotesk', False],
            [
                svgCdBooklet,
                "2",
                10,
                15,
                "start",
                "normal",
                f"All titles written by {self.album.surnameCredits}",
                "Flapcredit",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdBooklet,
                "2",
                10,
                20,
                "start",
                "normal",
                f"©{self.album.year}  {self.album.incarn.artist.label.name} \N{BULLET} {self.album.catNo}",
                "FlapCopyright",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdBooklet,
                "3",
                217,
                110.5,
                "end",
                "normal",
                self.album.incarn.artist.label.name,
                "labelNameFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdBooklet,
                "3",
                118,
                0,
                "start",
                "normal",
                self.album.seed,
                "pixelSeed",
                "SeedBinaryPixel",
                True,
            ],
        ]
        for t in textLines:
            svgCdBooklet.add(
                self.artworkTextOneLine(
                    t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]
                )
            )
        svgCdBooklet.add(self.svgMarkers(svgCdBooklet, 250, 130, 10, show=False))
        svgCdBooklet.add(
            self.artworkTextMultiTrackNames(
                svgCdBooklet,
                "2",
                10,
                25,
                "start",
                textLines=self.album.tracks,
                id="tracklist",
                lineSpacing=3,
            )
        )
        svgCdBooklet.save()
        return

    def artworkCdTray(self):
        svgCdTray = svgwrite.Drawing(
            self.album.path + "\\Artwork_CD_Tray.svg",
            size=("300mm", "300mm"),
            viewBox=("0 0 300 300"),
            profile="full",
        )
        svgCdTray.add(
            self.artworkOutline(
                svgCdTray,
                self.artColorOutline,
                "0.2",
                self.artColorBG,
                "0",
                [[(0, 0), (6, 120)], [(6, 0), (120, 120)], [(126, 0), (6, 120)],],
            )
        )
        svgCdTray.add(
            self.artworkOutline(
                svgCdTray,
                self.artColorOutline,
                "0.2",
                "none",
                "1",
                [
                    # [(1  ,  1), (4,118)],
                    # [(127,  1), (4,118)],
                    # [(72, 65), (50,50)],
                ],
            )
        )
        # define values for all the texts to be used
        textLines = [
            # 	size, x, y, anchor, weight, text, id, font, transform,
            [
                svgCdTray,
                "2.5",
                2.2,
                6,
                "start",
                "normal",
                f"{self.album.incarn.artist.name} \N{NO-BREAK SPACE}\N{NO-BREAK SPACE}\N{BULLET}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE} {self.album.name}",
                "spineName",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svgCdTray,
                "2.5",
                128,
                6,
                "start",
                "normal",
                f"{self.album.incarn.artist.name} \N{NO-BREAK SPACE}\N{NO-BREAK SPACE}\N{BULLET}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE} {self.album.name}",
                "spineName",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svgCdTray,
                "2",
                2.2,
                110,
                "end",
                "normal",
                self.album.catNo,
                "catNoSpine",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svgCdTray,
                "2",
                128,
                110,
                "end",
                "normal",
                self.album.catNo,
                "catNoSpine",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svgCdTray,
                "2.5",
                21,
                111.5,
                "start",
                "normal",
                self.album.incarn.artist.label.name,
                "labelName",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdTray,
                "3",
                124,
                0,
                "start",
                "normal",
                self.album.seed,
                "pixelSeed",
                "SeedBinaryPixel",
                True,
            ],
            [
                svgCdTray,
                "2.5",
                10,
                12,
                "start",
                "normal",
                f'All titles written by {" / ".join([p.surname for p in self.album.people])}',
                "credits",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdTray,
                "2.5",
                10,
                17,
                "start",
                "normal",
                f"©{self.album.year}  {self.album.incarn.artist.label.name} \N{NO-BREAK SPACE}\N{NO-BREAK SPACE}\N{BULLET}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE} {self.album.catNo}",
                "copyright",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgCdTray,
                "2.5",
                10,
                7,
                "start",
                "normal",
                self.album.svgTagline,
                "tagline",
                "Alte Haas Grotesk",
                False,
            ],
        ]
        for t in textLines:
            svgCdTray.add(
                self.artworkTextOneLine(
                    t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]
                )
            )
        svgCdTray.add(
            self.artworkTextMultiTrackNames(
                svgCdTray,
                "2.5",
                10,
                22,
                "start",
                textLines=self.album.tracks,
                id="tracklist",
                lineSpacing=3,
            )
        )
        # svgCdTray.add(self.artworkLogo(svgCdTray, 9, 9, 10, 106)) TODO USE SYMBOL
        # svgCdTray.add(self.artworkLogo(svgCdTray, 4, 4, 1, 112)) TODO USE SYMBOL
        # svgCdTray.add(self.artworkLogo(svgCdTray, 4, 4, 127, 112)) TODO USE SYMBOL
        # svgCdTray.add(self.artworkSelect(svgCdTray, 50, 50, 72, 65))

        svgCdTray.add(self.svgMarkers(svgCdTray, 150, 130, 10, show=False))
        svgCdTray.save()
        return

    def artworkPoster(self):
        svgPath = self.album.path + "\\Artwork_A2_Poster.svg"
        svgPosterA2 = svgwrite.Drawing(
            svgPath, size=("420mm", "594mm"), viewBox=("0 0 420 594"), profile="full",
        )
        svgPosterA2.defs.add(self.svgSymbols)
        svgPosterA2.add(
            self.artworkOutline(
                svgPosterA2,
                self.artColorOutline,
                "0.2",
                self.artColorBG,
                "1",
                [[(0, 0), (420, 594)],],  # single large rectangle
            )
        )
        artIds = [
            "logo",  # 0
            "rect",
            "3triangles",
            "4quadrants",
            "circles",
            "rays",
            "angle",
            "sector",
            "halfcircleempty",  # 8
            "halfcirclefilled",
            "diagonal",
            "circlefilled",
            "circleempty",
            "reeds",  # 13
        ]
        # artChosen = "#" + artIds[randint(0, (len(artIds)))]
        artChosen1 = "#" + artIds[randint(0, (len(artIds)) - 1)]
        artChosen2 = "#" + artIds[6]
        # if choice(["grid", "single"]) == "grid":
        # if random() > 1:  # single
        if 1 == 1:  # single
            # front art
            svgPosterA2.add(
                svgPosterA2.use(
                    href=(artChosen1), transform="translate(145 70) scale(0.7)"
                )
            )
        else:  # grid
            gridDim = randint(4, 8)
            gridGap = randint(2, 6)
            gridCellDim = (self.artDim - ((gridDim - 1) * gridGap)) / gridDim
            symbolChosen1 = svgPosterA2.g(id="chosen1")
            svgPosterA2.defs.add(symbolChosen1)
            symbolChosen1.add(
                svgPosterA2.use(
                    href=(artChosen1),
                    stroke="white",
                    stroke_width="0.1",
                    fill="blue",
                    # transform="rotate(0)",
                )
            )
            symbolChosen2 = svgPosterA2.g(id="chosen2")
            svgPosterA2.defs.add(symbolChosen2)
            symbolChosen2.add(
                svgPosterA2.use(
                    href=(artChosen2),
                    stroke="white",
                    stroke_width="0.1",
                    fill="red",
                    # transform="rotate(0)",
                )
            )

            for row in range(0, gridDim):
                for column in range(0, gridDim):
                    artInsert = svgPosterA2.use(
                        href=("chosen1" if (random() > 0.5) else "chosen2"),
                    )
                    artInsert.translate(
                        400 + (column * gridCellDim) + (column * gridGap),
                        70 + (row * gridCellDim) + (row * gridGap),
                    )
                    artInsert.scale(gridCellDim / self.artDim)
                    svgPosterA2.add(artInsert)

                    # , transform=f"translate({400 + (column * gridCellDim) + (column * gridGap)} {70 + (row * gridCellDim)+(row * gridGap)}) scale({gridCellDim/(self.artDim)}) ", stroke="white", stroke_width="0.1", fill="none",)
                    # svg12in.use(href=(artChosen), transform=f"translate({400 + (column * gridCellDim) + (column * gridGap)} {70 + (row * gridCellDim)+(row * gridGap)}) scale({gridCellDim/(self.artDim)}) ", stroke="white", stroke_width="0.1", fill="none",)
        # # region add logos
        # # add logo symbol front
        # svg12in.add(
        #     svg12in.use(href=("#logo"), transform="translate(590 290) scale(2)",)
        # )
        # # add logo symbol back
        # svg12in.add(
        #     svg12in.use(href=("#logo"), transform="translate(20 270) scale(2)",)
        # )
        # # endregion

        # add outlines for layout
        svgPosterA2.add(
            self.artworkOutline(
                svgPosterA2,
                "white",
                "0.2",
                "none",
                "1",
                [
                    [(20, 20), (380, 380)],
                    # [(20, 410), (380, 164)],
                    # [(385, 559), (15, 15)],
                    # [(20, 450), (380, 10)],
                ],
            )
        )
        # add logo symbol front
        svgPosterA2.add(
            svgPosterA2.use(href=("#logo"), transform="translate(380 555) scale(2)",)
        )

        formatTexts=[
            f"Compact Cassette",
            f"12\" Vinyl",
            f"Compact Disc",
        ]
        for i, t in enumerate(formatTexts):
            svgPosterA2.add(svgPosterA2.text( f"{t}", insert=((305), (540 + (i * 5))), stroke_width="0", font_size=4, text_anchor="start", fill="white",stroke="white",font_family="Alte Haas Grotesk"))

        catNoTexts=[
            f"{self.album.incarn.artist.label.initials}.MC.{self.album.seed} {self.albumFormat.year}",
            f"{self.album.incarn.artist.label.initials}.12.{self.album.seed} {self.albumFormat.year}",
            f"{self.album.incarn.artist.label.initials}.CD.{self.album.seed} {self.albumFormat.yearCD}",
        ]
        for i, t in enumerate(catNoTexts):
            svgPosterA2.add(svgPosterA2.text( f"{t}", insert=((400), (540 + (i * 5))), stroke_width="0", font_size=4, text_anchor="end", fill="white",stroke="white",font_family="Alte Haas Grotesk"))

        
        # Single lines of text

        textLines = [
            # 	size, x, y, anchor, weight, text, id, font, transform,
            [
                svgPosterA2,
                "18",
                400,
                425,
                "end",
                "bold",
                self.album.incarn.artist.name,
                "artistFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgPosterA2,
                "18",
                400,
                450,
                "end",
                "normal",
                self.album.name,
                "albumFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgPosterA2,
                "1.5mm",
                377,
                564,
                "end",
                "normal",
                self.album.incarn.artist.label.name,
                "labelNameFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svgPosterA2,
                "1mm",
                377,
                570,
                "end",
                "normal",
                self.album.seed,
                "pixelSeed",
                "SeedBinaryPixel",
                False,
            ],
            [
                svgPosterA2,
                "1mm",
                20,
                574,
                "start",
                "normal",
                self.album.svgTagline,
                "taglineFront",
                "Alte Haas Grotesk",
                False,
            ],


            # [
            #     svgPosterA2,
            #     "1.5mm",
            #     400,
            #     470,
            #     "end",
            #     "normal",
            #     f"{self.album.seed}",
            #     "catNo",
            #     "Alte Haas Grotesk",
            #     False,
            # ],
            # [svg12in, '1mm', 20, 310, 'start', 'normal', self.album.artist.label.name, 'labelNameBack', 'Alte Haas Grotesk', False],
        ]
        for t in textLines:
            svgPosterA2.add(
                self.artworkTextOneLine(
                    t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]
                )
            )
        
        # add markers for layout
        svgPosterA2.add(self.svgMarkers(svgPosterA2, 430, 600, 10, show=False))
        svgPosterA2.save()
        return

    def artwork12in(self):
        svg12in = svgwrite.Drawing(
            self.album.path + "\\Artwork_12in_Vinyl.svg",
            size=("700mm", "400mm"),
            viewBox=("0 0 700 400"),
            profile="full",
        )
        svg12in.defs.add(self.svgSymbols)

        #  background shapes
        svg12in.add(
            self.artworkOutline(
                svg12in,
                self.artColorOutline,
                "0.2",
                self.artColorBG,
                "1",
                [
                    [(0, 13), (627, 312)],  # main large rectangle
                    [(315, 10), (312, 3)],  # top spine
                    [(312, 13), (3, 312)],  # side spine
                    [(315, 325), (312, 3)],  # bottom spine
                    [(316, 0), (310, 10)],  # top glue flap
                    [(316, 328), (310, 10)],  # bottom glue flap
                ],
            )
        )

        # TODO add all art styles
        artIds = [
            "logo",  # 0
            "rect",
            "3triangles",
            "4quadrants",
            "circles",
            "rays",
            "angle",
            "sector",
            "halfcircleempty",  # 8
            "halfcirclefilled",
            "diagonal",
            "circlefilled",
            "circleempty",
            "reeds",  # 13
        ]
        # artChosen = "#" + artIds[randint(0, (len(artIds)))]
        artChosen1 = "#" + artIds[randint(0, (len(artIds)) - 1)]
        artChosen2 = "#" + artIds[6]
        # if choice(["grid", "single"]) == "grid":
        # if random() > 1:  # single
        if 1 == 1:  # single
            # front art
            svg12in.add(
                svg12in.use(href=(artChosen1), transform="translate(145 70) scale(0.7)")
            )
            # back art
            svg12in.add(
                svg12in.use(href=(artChosen1), transform="translate(400 70) scale(1)")
            )
        else:  # grid
            gridDim = randint(4, 8)
            gridGap = randint(2, 6)
            gridCellDim = (self.artDim - ((gridDim - 1) * gridGap)) / gridDim
            symbolChosen1 = svg12in.g(id="chosen1")
            svg12in.defs.add(symbolChosen1)
            symbolChosen1.add(
                svg12in.use(
                    href=(artChosen1),
                    stroke="white",
                    stroke_width="0.1",
                    fill="blue",
                    # transform="rotate(0)",
                )
            )
            symbolChosen2 = svg12in.g(id="chosen2")
            svg12in.defs.add(symbolChosen2)
            symbolChosen2.add(
                svg12in.use(
                    href=(artChosen2),
                    stroke="white",
                    stroke_width="0.1",
                    fill="red",
                    # transform="rotate(0)",
                )
            )

            for row in range(0, gridDim):
                for column in range(0, gridDim):
                    artInsert = svg12in.use(
                        href=("chosen1" if (random() > 0.5) else "chosen2"),
                    )
                    artInsert.translate(
                        400 + (column * gridCellDim) + (column * gridGap),
                        70 + (row * gridCellDim) + (row * gridGap),
                    )
                    artInsert.scale(gridCellDim / self.artDim)
                    svg12in.add(artInsert)

                    # , transform=f"translate({400 + (column * gridCellDim) + (column * gridGap)} {70 + (row * gridCellDim)+(row * gridGap)}) scale({gridCellDim/(self.artDim)}) ", stroke="white", stroke_width="0.1", fill="none",)
                    # svg12in.use(href=(artChosen), transform=f"translate({400 + (column * gridCellDim) + (column * gridGap)} {70 + (row * gridCellDim)+(row * gridGap)}) scale({gridCellDim/(self.artDim)}) ", stroke="white", stroke_width="0.1", fill="none",)

        # region add logos
        # add logo symbol front
        svg12in.add(
            svg12in.use(href=("#logo"), transform="translate(590 290) scale(2)",)
        )
        # add logo symbol back
        svg12in.add(
            svg12in.use(href=("#logo"), transform="translate(20 270) scale(2)",)
        )
        # endregion

        # region texts
        # Single lines of text
        textLines = [
            # 	size, x, y, anchor, weight, text, id, font, transform,
            [
                svg12in,
                "2",
                312.5,
                30,
                "start",
                "normal",
                f"{self.album.incarn.artist.name} \N{NO-BREAK SPACE}\N{NO-BREAK SPACE}\N{BULLET}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE} {self.album.name}",
                "NameSpine",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svg12in,
                "2",
                312.5,
                310,
                "end",
                "normal",
                f"{self.album.incarn.artist.label.name}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE}\N{BULLET}\N{NO-BREAK SPACE}\N{NO-BREAK SPACE}{self.album.catNo}",
                "catNoSpine",
                "Alte Haas Grotesk",
                True,
            ],
            [
                svg12in,
                "14",
                610,
                37,
                "end",
                "bold",
                self.album.incarn.artist.name,
                "FrontArtist",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "14",
                610,
                55,
                "end",
                "normal",
                self.album.name,
                "FrontAlbum",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "1.5mm",
                585,
                302,
                "end",
                "normal",
                self.album.incarn.artist.label.name,
                "labelNameFront",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "1mm",
                304,
                320,
                "end",
                "normal",
                self.album.seed,
                "pixelSeed",
                "SeedBinaryPixel",
                True,
            ],
            [
                svg12in,
                "1mm",
                20,
                295,
                "start",
                "normal",
                f'All titles written by {" / ".join([p.surname for p in self.album.people])}',
                "creditsBack",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "1mm",
                20,
                300,
                "start",
                "normal",
                f"©{self.album.year}  {self.album.incarn.artist.label.name}",
                "labelNameRear",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "1mm",
                20,
                310,
                "start",
                "normal",
                self.album.svgTagline,
                "taglineBack",
                "Alte Haas Grotesk",
                False,
            ],
            [
                svg12in,
                "1mm",
                20,
                305,
                "start",
                "normal",
                f"CS{self.album.seed}",
                "catNo",
                "Alte Haas Grotesk",
                False,
            ],
            # [svg12in, '1mm', 20, 310, 'start', 'normal', self.album.artist.label.name, 'labelNameBack', 'Alte Haas Grotesk', False],
        ]
        for t in textLines:
            svg12in.add(
                self.artworkTextOneLine(
                    t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]
                )
            )

        # Multiple lines of text
        svg12in.add(
            self.artworkTextMultiTrackNames(
                svg12in,
                "1mm",
                20,
                75,
                "start",
                textLines=self.album.tracks,
                id="trackNames",
                lineSpacing=5,
            )
        )
        # endregion

        svg12in.add(self.svgMarkers(svg12in, 630, 330, 10, show=False))
        svg12in.save()
        return


# def artwork(
#     self, artFileName, width="248", height="248", colorFg="black", pixels="50"
# ):
#     # artTypeList = ["4arcs", "stripes", "depolar", "rays", "roundel", "gridpolar", "spikes", "blockgrid"]
#     artTypeList = [
#         "stripes",
#         "rays",
#         "roundel",
#         "depolar",
#         "gridpolar",
#         "blockgrid",
#     ]
#     #  leave out "corner" and landscape for now
#     #  add square with just a line across. X=0, Y=random, X=width, Y=random.
#     #  put corner back. Just white.
#     artType = artTypeList[randint(0, len(artTypeList) - 1)]
#     # artType = "gridpolar"
#     artPath = self.path + "\\" + artFileName
#     c = []
#     if artType in ["rays", "roundel", "stripes", "depolar"]:
#         with Image(width=int(pixels), height=1) as stripes:
#             stripes.format = "png"
#             stripes.seed = self.seed
#             stripes.noise("random")
#             stripes.channel_images["green"]
#             stripes.resize(width=int(width), height=int(height))
#             stripes.threshold()
#             stripes.opaque_paint(target="White", fill="Black")
#             stripes.opaque_paint(
#                 target="Black", fill=self.albumArtwork.artColorBG, invert=True
#             )
#             if artType == "rays":
#                 stripes.distort(
#                     "polar",
#                     [
#                         (int(width) / 2),
#                         0,
#                         (int(width) / 2),
#                         (int(height) / 2),
#                         0,
#                         0,
#                     ],
#                 )
#             elif artType == "depolar":
#                 stripes.distort(
#                     "depolar",
#                     [
#                         (int(width) / 2),
#                         0,
#                         (int(width) / 2),
#                         (int(height) / 2),
#                         0,
#                         0,
#                     ],
#                 )
#             elif artType == "roundel":
#                 stripes.rotate(90)
#                 stripes.distort(
#                     "polar",
#                     [
#                         (int(width) / 2),
#                         0,
#                         (int(width) / 2),
#                         (int(height) / 2),
#                         0,
#                         0,
#                     ],
#                 )
#             stripes.save(filename=artPath)
#     elif artType == "corner":
#         widthM1 = int(width) - 1
#         heightM1 = int(height) - 1
#         xMid = randint(int(widthM1 * 0.2), int(widthM1 * 0.8))
#         yMid = randint(int(heightM1 * 0.5), int(heightM1 * 0.8))
#         xy = [
#             ["0,0 ", str(xMid) + ",0 ", str(widthM1) + ",0 "],
#             [0, str(xMid) + "," + str(yMid) + " ", 0],
#             [
#                 "0," + str(randint(yMid, heightM1)) + " ",
#                 0,
#                 str(widthM1) + "," + str(randint(yMid, heightM1)) + " ",
#             ],
#             [
#                 "0," + str(heightM1) + " ",
#                 0,
#                 str(widthM1) + "," + str(heightM1) + " ",
#             ],
#         ]
#         c.append(
#             "convert -size " + width + "x" + height + " xc:yellow -stroke black "
#         )
#         c.append(
#             f"-fill #eee -strokewidth 2 -draw \"path 'M 0,0 L {xy[0][0]}{xy[0][1]}{xy[1][1]}{xy[2][0]} z'\""
#         )
#         c.append(
#             f"-fill #ddd -strokewidth 2 -draw \"path 'M {xy[0][1]} L {xy[0][2]}{xy[2][2]}{xy[1][1]} z'\""
#         )
#         c.append(
#             f"-fill #ccc -strokewidth 2 -draw \"path 'M {xy[2][0]} L {xy[1][1]}{xy[2][2]}{xy[3][2]}{xy[3][0]} z'\""
#         )
#     elif artType == "landscape":
#         yTopLine = 0.5 * int(height)
#         lines = 5
#         steps = 20
#         change = 5
#         c.append("convert -size " + width + "x" + height + " xc:black ")
#         for l in tqdm(range(0, lines), desc="Draw Landscape Lines", position=5):
#             fillColour = f"rgb({l*(255/lines)},{l*(255/lines)},{l*(255/lines)})"
#             c.append(
#                 f"-fill {fillColour} -strokewidth 0 -draw \"path 'M0,{yTopLine+(l*((int(height)-yTopLine)/lines))}"
#             )
#         for _ in range(0, steps):
#             c.append(f"l {int(width)/steps},{randint(-change, change)}")
#             c.append(f"L {width},{height} L 0,{height} Z'\"")
#     elif artType == "spikes":
#         dim50 = int(0.5 * int(width))

#         def rs(a):
#             return str(randint(1, int(a)))

#         c.append(
#             f"convert -size {width}x{height} xc:{self.albumArtwork.artColorBG} -fill {colorFg} -draw \"fill-rule evenodd path 'M {dim50},{dim50}"
#         )
#         for _ in range(1, 6):
#             c.append(f"L{rs(width)},{rs(width)} L{rs(width)},{rs(width)} ")
#         c.append("Z'\"")
#     elif artType in ["blockgrid", "gridpolar"]:
#         with Image(width=10, height=10) as blockgrid:
#             blockgrid.format = "png"
#             blockgrid.seed = self.seed
#             blockgrid.channel_images["green"]
#             blockgrid.noise("random")
#             blockgrid.threshold()
#             blockgrid.resize(
#                 width=int(width), height=int(height), blur=0, filter="point"
#             )
#             blockgrid.opaque_paint(target="White", fill="Black")
#             blockgrid.opaque_paint(
#                 target="Black", fill=self.albumArtwork.artColorBG, invert=True
#             )
#             # display(blockgrid)
#             if artType == "gridpolar":
#                 blockgrid.distort(
#                     "polar",
#                     [
#                         (int(width) / 2),
#                         0,
#                         (int(width) / 2),
#                         (int(height) / 2),
#                         0,
#                         0,
#                     ],
#                 )
#             blockgrid.save(filename=artPath)
#     elif artType == "4arcs":
#         dim = int(width)
#         dimHalf = dim / 2
#         randRange = round(dimHalf)
#         # randRange=round(0.8*dimHalf)
#         midGapHalf = 5
#         nwx = randint(1, randRange)
#         nwy = randint(1, randRange)
#         nwc = str(dimHalf - midGapHalf) + " " + str(dimHalf - midGapHalf)
#         nex = randint(1, randRange)
#         ney = randint(1, randRange)
#         nec = str(dimHalf + midGapHalf) + " " + str(dimHalf - midGapHalf)
#         swx = randint(1, randRange)
#         swy = randint(1, randRange)
#         swc = str(dimHalf - midGapHalf) + " " + str(dimHalf + midGapHalf)
#         sex = randint(1, randRange)
#         sey = randint(1, randRange)
#         sec = str(dimHalf + midGapHalf) + " " + str(dimHalf + midGapHalf)
#         c.append(
#             f"convert -size {dim}x{dim} xc:{self.albumArtwork.artColorBG} -fill {colorFg}"
#         )
#         # TODO delete this? c.append('-draw "path \'M' + nwc + 'l 0 ' + str(-nwy) + ' a ' + str(nwx) + ' ' + str(nwy) + ' 0 0 0 ')
#         c.append("-draw \"path '")
#         c.append(f"M {nwc} l 0 {-nwy} a {nwx} {nwy} 0 0 0 {-nwx} {nwy} l {nwx} 0")
#         c.append(f"M {nec} l 0 {-ney} a {nex} {ney} 0 0 1 {nex} {ney} l {-nex} 0")
#         c.append(f"M {swc} l 0 {swy} a {swx} {swy} 0 0 1 {-swx} {-swy} l {swx} 0")
#         c.append(f"M {sec} l 0 {sey} a {sex} {sey} 0 0 0 {sex} {-sey} l {-sex} 0")
#         c.append("'\"")
#     # c.append(artPath)
#     # command = ' '.join(c)
#     # print(command)
#     # subprocess.call(command, shell=True)
#     return artPath
