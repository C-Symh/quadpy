import json
import os

import numpy

from ...helpers import article
from .._helpers import T3Scheme

source = article(
    authors=["Jan Jaśkowiec", "N. Sukumar"],
    title="High-order cubature rules for tetrahedra",
    journal="Numerical Methods in Engineering",
    volume="121",
    number="11",
    year="2020",
    pages="2418-2436",
    url="https://doi.org/10.1002/nme.6313",
)
# Data from
# https://onlinelibrary.wiley.com/doi/abs/10.1002/nme.6313


def _read(string, tol=1.0e-14):
    this_dir = os.path.dirname(os.path.realpath(__file__))
    filename = f"js{string}.json"
    with open(os.path.join(this_dir, filename), "r") as f:
        data = json.load(f)

    degree = data.pop("degree")

    points = numpy.array(data["points"])
    points = numpy.column_stack([points, 1.0 - numpy.sum(points, axis=1)])
    weights = numpy.array(data["weights"])

    return T3Scheme(f"Jaśkowiec-Sukumar {string}", weights, points, degree, source, tol)


def jaskowiec_sukumar_02():
    return _read("02")


def jaskowiec_sukumar_03():
    return _read("03")


def jaskowiec_sukumar_04():
    return _read("04")


def jaskowiec_sukumar_05():
    return _read("05")


def jaskowiec_sukumar_06():
    return _read("06")


def jaskowiec_sukumar_07():
    return _read("07")


def jaskowiec_sukumar_08():
    return _read("08")


def jaskowiec_sukumar_09():
    return _read("09")


def jaskowiec_sukumar_10():
    return _read("10")


def jaskowiec_sukumar_11():
    return _read("11")


def jaskowiec_sukumar_12():
    return _read("12")


def jaskowiec_sukumar_13():
    return _read("13")


def jaskowiec_sukumar_14():
    return _read("14")


def jaskowiec_sukumar_15():
    return _read("15", 3.687e-11)


def jaskowiec_sukumar_16():
    return _read("16", 2.653e-11)


def jaskowiec_sukumar_17():
    return _read("17", 3.831e-11)


def jaskowiec_sukumar_18():
    return _read("18", 3.470e-11)


def jaskowiec_sukumar_19a():
    return _read("19a", 4.679e-11)


def jaskowiec_sukumar_19b():
    return _read("19b", 4.580e-11)


def jaskowiec_sukumar_20():
    return _read("20", 2.315e-11)
