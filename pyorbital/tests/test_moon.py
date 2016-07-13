#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Adam.Dybbroe

# Author(s):

#   Adam.Dybbroe <adam.dybbroe@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit testing the moon phase and moon position/angles calculations
"""

import unittest
import numpy as np
from datetime import datetime, timedelta
from pyorbital.moon_phase import moon_phase
from pyorbital import planets

LAT, LON = 58.5875, 16.1875

MOON_PHASE = np.array(
    [0.409753,  0.458902,  0.507830,  0.556157,  0.603532,
     0.649628,  0.694135,  0.736750,  0.777180,  0.815135,
     0.850327,  0.882472,  0.911289,  0.936505,  0.957855,
     0.975088,  0.987971,  0.996291,  0.999865,  0.998545,
     0.992221,  0.980826,  0.964349,  0.942831,  0.916374,
     0.885145,  0.849373,  0.809354,  0.765447,  0.718071,
     0.667707,  0.614887,  0.560201,  0.504283,  0.447817,
     0.391531,  0.336191,  0.282592,  0.231546,  0.183869,
     0.140348,  0.101725,  0.068656,  0.041694,  0.021252,
     0.007593,  0.000819,  0.000868,  0.007533,  0.020473,
     0.039247,  0.063336,  0.092173,  0.125171,  0.161743,
     0.201318,  0.243355,  0.287348,  0.332827,  0.379362,
     0.426553,  0.474030,  0.521443,  0.568459,  0.614757,
     0.660015,  0.703914,  0.746129,  0.786327,  0.824166,
     0.859293,  0.891348,  0.919965,  0.944774,  0.965412,
     0.981527,  0.992790,  0.998906,  0.999623,  0.994750,
     0.984166,  0.967833,  0.945803,  0.918221,  0.885333,
     0.847479,  0.805085,  0.758660,  0.708778,  0.656070,
     0.601211,  0.544909,  0.487898,  0.430928,  0.374757,
     0.320146,  0.267844,  0.218581,  0.173048,  0.131881])

LONARR = np.array([10.000, 11.000, 12.000, 13.000, 14.000, 14.989])
LATARR = np.array([50.000, 51.000, 52.000, 53.000, 54.000, 54.989])
RESULT1_ALT = np.array([6.46076487,  6.65664799,  6.82103169,
                        6.95359249,  7.05405387, 7.12161456])
RESULT1_AZI = np.array([112.50462386,  113.42950322,  114.3687665,
                        115.32140457, 116.28639318,  117.25189999])


class TestMoon(unittest.TestCase):

    """Unit testing the moon calculations"""

    def assertNumpyArraysEqual(self, this, that, ndigits=7, msg=''):
        """
        modified from http://stackoverflow.com/a/15399475/5459638
        """
        atol = 1. / (10.**ndigits)

        if this.shape != that.shape:
            raise AssertionError("Shapes don't match")
        if not np.allclose(this, that, atol=atol, rtol=0):
            raise AssertionError("Elements don't match!")

    def setUp(self):
        """Set up"""

        self.start_time = datetime(2011, 12, 1, hour=12)
        self.delta_t = timedelta(hours=12)
        return

    def tearDown(self):
        """Clean up"""
        return

    def test_moon_phase(self):

        time_t = self.start_time
        phase = moon_phase(time_t)
        self.assertAlmostEqual(phase, 0.409753, 5)

        # Should eventually be possible to take an aray of datetimes!
        phase = []
        for i in range(100):
            phase.append(moon_phase(time_t))
            time_t = time_t + self.delta_t

        phase = np.array(phase)

        self.assertNumpyArraysEqual(phase, MOON_PHASE, 6)

    def test_moon_position(self):

        moon = planets.Moon(self.start_time)
        rasc, decl, alt, azi = moon.topocentric_position(LON, LAT)

        self.assertAlmostEqual(alt, 6.01043303, 5)
        self.assertAlmostEqual(azi, 118.7126239, 5)
        self.assertAlmostEqual(rasc, -32.800324, 5)
        self.assertAlmostEqual(decl, -9.183704, 5)

        moon = planets.Moon(self.start_time + self.delta_t * 10)
        rasc, decl, alt, azi = moon.topocentric_position(LON, LAT)

        self.assertAlmostEqual(alt, -0.8814571, 5)
        self.assertAlmostEqual(azi, 62.974637, 5)
        self.assertAlmostEqual(rasc, 24.15641340, 5)
        self.assertAlmostEqual(decl, 12.9278790, 5)

    def test_moon_positions(self):

        moon = planets.Moon(self.start_time)
        rasc, decl, alt, azi = moon.topocentric_position(LONARR, LATARR)

        self.assertNumpyArraysEqual(alt, RESULT1_ALT, 6)
        self.assertNumpyArraysEqual(azi, RESULT1_AZI, 6)


def suite():
    """The suite for moon phase and angles testing"""
    loader = unittest.TestLoader()
    mysuite = unittest.TestSuite()
    mysuite.addTest(loader.loadTestsFromTestCase(TestMoon))

    return mysuite