# -*- coding: utf-8 -*-
"""
***************************************************************************
*   Copyright (c) 2022                                                    *
*   Shai Seger <shaise[at]gmail>                                          *
*                                                                         *
*   This file is a supplement to the FreeCAD CAx development system.      *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Lesser General Public License (LGPL)    *
*   as published by the Free Software Foundation; either version 2 of     *
*   the License, or (at your option) any later version.                   *
*   for detail see the LICENCE text file.                                 *
*                                                                         *
*   This software is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License for more details.                  *
*                                                                         *
*   You should have received a copy of the GNU Library General Public     *
*   License along with this macro; if not, write to the Free Software     *
*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
*   USA                                                                   *
*                                                                         *
***************************************************************************
"""
from screw_maker import *
import FastenerBase

# PEM Self Clinching nuts types: S/SS/CLS/CLSS/SP

def clMakeFace(do, di, a, c, e, t):
    do = do / 2
    di = di / 2
    ch1 = do - di
    ch2 = ch1 / 2
    if ch2 < 0.2:
        ch2 = 0.2
    c = c / 2
    e = e / 2
    c2 = (c + e) / 2
    sl = a / 20
    a2 = a / 2

    fm = FastenerBase.FSFaceMaker()
    fm.AddPoint(di, -a + ch1)
    fm.AddPoint(do, -a)
    fm.AddPoint(c, -a)
    fm.AddPoint(c, -a * 0.75, )
    fm.AddPoint(c - sl, -a2)
    fm.AddPoint(c2, -a2)
    fm.AddPoint(c2, 0)
    fm.AddPoint(e, 0)
    fm.AddPoint(e, t - ch2)
    fm.AddPoint(e - ch2, t)
    fm.AddPoint(do, t)
    fm.AddPoint(di, t - ch1)
    return fm.GetFace()


def makePEMPressNut(self, fa):
    diam = fa.calc_diam
    code = fa.tcode

    i = FsTitles[fa.type + "tcodes"].index(code)

    c, e, t, di = fa.dimTable
    a = FsData[fa.type + "tcodes"][diam][i]
    if a == 0:
        return None
    do = FastenerBase.MToFloat(diam)
    fFace = clMakeFace(do, di, a, c, e, t)
    fSolid = fFace.revolve(Base.Vector(0.0, 0.0, 0.0), Base.Vector(0.0, 0.0, 1.0), 360)
    if fa.thread:
        dia = self.getDia(diam, True)
        P = FsData["MetricPitchTable"][diam][0]
        H = a + t
        turns = int(H / P) + 2
        threadCutter = self.makeInnerThread_2(dia, P, turns, None, H)
        threadCutter.translate(Base.Vector(0.0, 0.0, t + P))
        # Part.show(threadCutter, 'threadCutter')
        fSolid = fSolid.cut(threadCutter)
    return fSolid
