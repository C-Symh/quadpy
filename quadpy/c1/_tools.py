import numpy

from ._gauss_kronrod import _gauss_kronrod_integrate


def _numpy_all_except_last(a):
    return numpy.all(a, axis=tuple(range(len(a.shape) - 1)))


class IntegrationError(Exception):
    pass


def integrate_adaptive(
    f,
    intervals,
    eps_abs=1.0e-10,
    eps_rel=1.0e-10,
    criteria_connection=numpy.logical_and,
    # Use 21-point Gauss-Kronrod like QUADPACK
    # <https://en.wikipedia.org/wiki/QUADPACK#General-purpose_routines>
    kronrod_degree=10,
    minimum_interval_length=0.0,
    max_num_subintervals=numpy.inf,
    dot=numpy.dot,
    domain_shape=None,
    range_shape=None,
):
    intervals = numpy.asarray(intervals)
    assert intervals.shape[0] == 2

    assert (
        eps_abs is not None or eps_rel is not None
    ), "One of eps_abs, eps_rel must be specified."

    # Use Gauss-Kronrod scheme for error estimation and adaptivity.
    # The method also returns guesses for the domain_shape and range_shape (if any of
    # them is None).
    out = _gauss_kronrod_integrate(
        kronrod_degree,
        f,
        intervals,
        dot=dot,
        domain_shape=domain_shape,
        range_shape=range_shape,
    )
    value_estimates = out.val_gauss_legendre
    interval_lengths = out.interval_lengths
    error_estimates = out.error_estimate
    domain_shape = out.domain_shape
    range_shape = out.range_shape

    # Flatten the list of intervals so we can do good-bad bookkeeping via a list.
    intervals = intervals.reshape((2,) + domain_shape + (-1,))
    num_subintervals = 1
    orig_shape = value_estimates.shape
    value_estimates = value_estimates.reshape(range_shape + (-1,))
    error_estimates = error_estimates.reshape(range_shape + (-1,))

    # Mark intervals with acceptable approximations. For this, take all() across every
    # dimension except the last one (which is the interval index).
    criteria = []
    if eps_abs is not None:
        is_okay = error_estimates < eps_abs
        criteria.append(_numpy_all_except_last(is_okay))
    if eps_rel is not None:
        is_okay = error_estimates < eps_rel * numpy.abs(value_estimates)
        criteria.append(_numpy_all_except_last(is_okay))
    is_good = criteria_connection(*criteria)

    good_values_sum = numpy.sum(value_estimates[..., is_good], axis=-1)
    good_errors_sum = numpy.sum(error_estimates[..., is_good], axis=-1)

    while numpy.any(~is_good):
        # split the bad intervals in half
        bad_intervals = intervals[..., ~is_good]
        midpoints = 0.5 * (bad_intervals[0] + bad_intervals[1])
        intervals = numpy.array(
            [
                numpy.concatenate([bad_intervals[0], midpoints], axis=-1),
                numpy.concatenate([midpoints, bad_intervals[1]], axis=-1),
            ]
        )
        # idx = numpy.concatenate([idx[~is_good], idx[~is_good]])
        num_subintervals += numpy.sum(is_good)

        if num_subintervals > max_num_subintervals:
            raise IntegrationError(
                f"Tolerances (abs: {eps_abs}, rel: {eps_rel}) could not be reached "
                f"with the given max_num_subintervals (= {max_num_subintervals})."
            )

        # compute values and error estimates for the new intervals
        out = _gauss_kronrod_integrate(
            kronrod_degree,
            f,
            intervals,
            dot=dot,
            domain_shape=domain_shape,
            range_shape=range_shape,
        )
        value_estimates = out.val_gauss_legendre
        interval_lengths = out.interval_lengths
        error_estimates = out.error_estimate

        # mark good intervals, gather values and error estimates
        if numpy.any(interval_lengths < minimum_interval_length):
            raise IntegrationError(
                f"Tolerances (abs: {eps_abs}, rel: {eps_rel}) could not be reached "
                f"with the given minimum_interval_length (= {minimum_interval_length})."
            )

        # tentative total value (as if all intervals were good)
        ttv = good_values_sum + numpy.sum(value_estimates, axis=-1)

        # distribute the remaining allowances according to the interval lengths
        tau = interval_lengths / numpy.sum(interval_lengths)

        criteria = []
        if eps_abs is not None:
            allowance_abs = eps_abs - good_errors_sum
            is_okay = error_estimates < numpy.multiply.outer(allowance_abs, tau)
            criteria.append(_numpy_all_except_last(is_okay))
        if eps_rel is not None:
            # allowance_rel = eps_rel - good_errors_sum / numpy.abs(ttv)
            # is_okay = error_estimates < tau * allowance_rel * numpy.abs(ttv)
            allowance_rel_ttv = eps_rel * numpy.abs(ttv) - good_errors_sum
            is_okay = error_estimates < numpy.multiply.outer(allowance_rel_ttv, tau)
            criteria.append(_numpy_all_except_last(is_okay))
        is_good = criteria_connection(*criteria)

        good_values_sum += numpy.sum(value_estimates[..., is_good], axis=-1)
        good_errors_sum += numpy.sum(error_estimates[..., is_good], axis=-1)

    good_values_sum = good_values_sum.reshape(orig_shape)
    good_errors_sum = good_errors_sum.reshape(orig_shape)
    return good_values_sum, good_errors_sum
