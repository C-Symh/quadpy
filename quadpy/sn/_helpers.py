import numpy
import sympy

from ..helpers import QuadratureScheme


class SnScheme(QuadratureScheme):
    def __init__(self, name, dim, weights, points, degree, source, tol=1.0e-14):
        super().__init__(name, weights, points, degree, source, tol)
        self.domain = f"Sn (n={dim})"
        self.dim = dim

    def points_inside(self):
        return numpy.einsum("ij,ij->i", self.points, self.points) < 1

    def points_inside_or_boundary(self):
        return numpy.einsum("ij,ij->i", self.points, self.points) <= 1

    def integrate(self, f, center, radius, dot=numpy.dot):
        center = numpy.array(center)
        rr = numpy.multiply.outer(radius, self.points)
        rr = numpy.swapaxes(rr, 0, -2)
        ff = numpy.array(f((rr + center).T))
        ref_vol = volume_nball(self.dim, r=numpy.asarray(radius), symbolic=False)
        return ref_vol * dot(ff, self.weights)


def volume_nball(n, symbolic, r=1):
    pi = sympy.pi if symbolic else numpy.pi

    if n == 0:
        return 1
    elif n == 1:
        return 2 * r
    return volume_nball(n - 2, symbolic, r=r) * 2 * pi / n * r ** 2


# The article
#
#     Gerald B. Folland,
#     How to Integrate a Polynomial over a Sphere,
#     The American Mathematical Monthly,
#     Vol. 108, No. 5 (May, 2001), pp. 446-448,
#     <https://doi.org/10.2307/2695802>
#
# gives the formula
#
#    (
#        radius ** (n + sum(exponents))
#        * integrate_monomial_over_unit_nsphere(exponents, symbolic=symbolic)
#        / (n + sum(exponents))
#    )
#
# More explicit is a direct recurrence.
def integrate_monomial_over_nball(k, symbolic=False, r=1):
    frac = sympy.Rational if symbolic else lambda a, b: a / b
    if any(a % 2 == 1 for a in k):
        return 0

    n = len(k)
    if all(a == 0 for a in k):
        return volume_nball(n, symbolic, r=r)

    # find first nonzero
    idx = next(i for i, j in enumerate(k) if j > 0)
    alpha = frac((k[idx] - 1) * r ** 2, sum(k) + n)
    k2 = k.copy()
    k2[idx] -= 2
    return integrate_monomial_over_nball(k2, symbolic, r=r) * alpha
