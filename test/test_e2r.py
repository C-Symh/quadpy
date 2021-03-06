import accupy
import numpy
import pytest

import quadpy
from helpers import check_degree
from quadpy.enr._helpers import integrate_monomial_over_enr

schemes = [
    quadpy.e2r.haegemans_piessens_a(),
    quadpy.e2r.haegemans_piessens_b(),
    quadpy.e2r.rabinowitz_richter_1(),
    quadpy.e2r.rabinowitz_richter_2(),
    quadpy.e2r.rabinowitz_richter_3(),
    # quadpy.e2r.rabinowitz_richter_4(),
    quadpy.e2r.rabinowitz_richter_5(),
    quadpy.e2r.stroud_4_1(),
    quadpy.e2r.stroud_5_1(),
    quadpy.e2r.stroud_7_1(),
    quadpy.e2r.stroud_9_1(),
    quadpy.e2r.stroud_11_1(),
    quadpy.e2r.stroud_11_2(),
    quadpy.e2r.stroud_15_1(),
    quadpy.e2r.stroud_secrest_5(),
    quadpy.e2r.stroud_secrest_6(),
]


@pytest.mark.parametrize("scheme", schemes)
def test_scheme(scheme):
    assert scheme.points.dtype == numpy.float64, scheme.name
    assert scheme.weights.dtype == numpy.float64, scheme.name

    print(scheme)

    degree, err = check_degree(
        lambda poly: scheme.integrate(poly, dot=accupy.fdot),
        integrate_monomial_over_enr,
        2,
        scheme.degree + 1,
        tol=scheme.test_tolerance,
    )
    assert (
        degree >= scheme.degree
    ), "{} -- observed: {}, expected: {} (max err: {:.3e})".format(
        scheme.name, degree, scheme.degree, err
    )


@pytest.mark.parametrize("scheme", [quadpy.e2r.rabinowitz_richter_1()])
def test_show(scheme):
    scheme.show()


if __name__ == "__main__":
    # scheme_ = quadpy.e2r.RabinowitzRichter(5)
    # test_scheme(scheme_, 1.0e-14)
    # test_show(scheme_)
    from helpers import find_equal

    find_equal(schemes)
