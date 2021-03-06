from sympy import Rational as frac
from sympy import sqrt

from ..helpers import article
from ._helpers import C2Scheme, concat, symm_r0, symm_s

source = article(
    authors=["W. Burnside"],
    title="An approximate quadrature formula",
    journal="Messenger of Math.",
    volume="37",
    year="1908",
    pages="166-167",
)


def burnside():
    r = sqrt(frac(7, 15))
    s = sqrt(frac(7, 9))
    weights, points = concat(symm_r0([frac(10, 49), r]), symm_s([frac(9, 196), s]))
    return C2Scheme("Burnside", weights, points, 5, source)
