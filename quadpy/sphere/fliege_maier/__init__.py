# -*- coding: utf-8 -*-
#
import json
import os
import re
import warnings

import numpy

from ..helpers import cartesian_to_spherical


class FliegeMaier(object):
    """
    """

    def __init__(self, index):
        warnings.warn("The Fliege-Maier schemes are only single-precision.")

        self.name = "FliegeMaier({})".format(index)

        this_dir = os.path.dirname(os.path.realpath(__file__))

        m = re.match("([0-9]+)([a-z]*)", index)
        filename = "fliege_maier_{:03d}{}.json".format(int(m.group(1)), m.group(2))
        with open(os.path.join(this_dir, filename), "r") as f:
            data = json.load(f)

        self.degree = data.pop("degree")

        data = numpy.array(data["data"])
        self.points = data[:, :3]
        self.weights = data[:, 3] / 4 / numpy.pi

        self.azimuthal_polar = cartesian_to_spherical(self.points)
        return
