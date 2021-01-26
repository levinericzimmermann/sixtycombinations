import typing

import expenvelope


class Tendency(object):
    """Tendency offers an interface for dynamically changing min/max areas.

    The class is based on Gottfried Michael Koenigs algorithm of "Tendenz-Masken" in
    his program "Projekt 2" where those min/max areas represent probability fields.

    :param minima_curve:
    :param maxima_curve:
    """

    def __init__(
        self, minima_curve: expenvelope.Envelope, maxima_curve: expenvelope.Envelope
    ):
        self._assert_curves_are_valid(minima_curve, maxima_curve)
        self._minima_curve = minima_curve
        self._maxima_curve = maxima_curve

    def __repr__(self) -> str:
        return "{}({}, {})".format(
            type(self).__name__, self.minima_curve, self.maxima_curve
        )

    @staticmethod
    def _assert_curves_are_valid(
        minima_curve: expenvelope.Envelope, maxima_curve: expenvelope.Envelope
    ):
        """Helper method that asserts the curves are a valid min/max pair."""

        # make sure both curves have equal duration
        try:
            assert minima_curve.end_time() == maxima_curve.end_time()
        except AssertionError:
            message = (
                "Found unequal duration when comparing 'minima_curve' (with end_time ="
                " '{}') and 'maxima_curve' (with end_time = '{}').".format(
                    minima_curve.end_time(), maxima_curve.end_time()
                )
            )
            message += " Make sure both curves have equal duration."
            raise ValueError(message)

        # compare all local extrema to make sure that at any time
        # point minima_curve < maxima_curve
        points_to_compare = (
            minima_curve.local_extrema(include_saddle_points=True)
            + maxima_curve.local_extrema(include_saddle_points=True)
            + [0, minima_curve.end_time()]
        )
        for time in points_to_compare:
            try:
                assert minima_curve.value_at(time) < maxima_curve.value_at(time)
            except AssertionError:
                message = (
                    "At time '{}' 'minima_curve' isn't smaller than 'maxima_curve'!"
                    .format(time)
                )
                raise ValueError(message)

    @property
    def minima_curve(self) -> expenvelope.Envelope:
        return self._minima_curve

    @minima_curve.setter
    def minima_curve(self, minima_curve: expenvelope.Envelope) -> expenvelope.Envelope:
        self._assert_curves_are_valid(minima_curve, self.maxima_curve)
        self._minima_curve = minima_curve

    @property
    def maxima_curve(self) -> expenvelope.Envelope:
        return self._maxima_curve

    @maxima_curve.setter
    def maxima_curve(self, maxima_curve: expenvelope.Envelope) -> expenvelope.Envelope:
        self._assert_curves_are_valid(self.minima_curve, maxima_curve)
        self._maxima_curve = maxima_curve

    def range_at(self, time: float) -> typing.Tuple[float]:
        return (self.minima_curve.value_at(time), self.maxima_curve.value_at(time))
