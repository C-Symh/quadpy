import sympy

from ..helpers import article, pm0, untangle
from ._helpers import S2Scheme

_source = article(
    authors=["J. Albrecht", "L. Collatz"],
    title="Zur numerischen Auswertung mehrdimensionaler Integrale",
    journal="ZAMM",
    volume="38",
    number="1-2",
    year="1958",
    pages="1–15",
    url="https://doi.org/10.1002/zamm.19580380102",
)

frac = sympy.Rational


def albrecht_collatz():
    # ERR Incorrectly stated in Stroud as sqrt(1/2) instead of 1/2
    data = [(frac(1, 4), pm0(2 * [frac(1, 2)]))]
    points, weights = untangle(data)
    return S2Scheme("Albrecht-Collatz", weights, points, 3, _source)
