import numbers
import typing


class EqualRangeDistribution(object):
    def __init__(self, minima: numbers.Number, maxima: numbers.Number, n_fields: int):
        self._minima = minima
        self._maxima = maxima
        self._n_fields = n_fields
        self._initialise_information_per_field(minima, maxima, n_fields)

    def _initialise_information_per_field(
        self, minima: numbers.Number, maxima: numbers.Number, n_fields: int
    ):
        area_range = maxima - minima
        equal_area_size_per_field = area_range / n_fields
        information_per_field = []
        for nth_field in range(n_fields):
            lower_border = minima + (equal_area_size_per_field * nth_field)
            upper_border = lower_border + equal_area_size_per_field
            from_lower_border_to_minima = lower_border - minima
            from_upper_border_to_maxima = maxima - upper_border
            information_per_field.append(
                (
                    lower_border,
                    upper_border,
                    from_lower_border_to_minima,
                    from_upper_border_to_maxima,
                )
            )

        self._information_per_field = tuple(information_per_field)

    def __repr__(self) -> str:
        return "{}(minima = {}, maxima = {}, n_fields = {})".format(
            type(self).__name__, self._minima, self._maxima, self._n_fields
        )

    def __call__(self, overlap: float) -> typing.Tuple[typing.Tuple[float]]:
        """Find min/max area for each field according to the entered overlap.

        :param overlap: value from 0 to 1 where 1 represents maximum overlap
            (each field share the same range) and 0 represents minimal overlap
            (no field shares any value with any other field).
        """

        area_per_field = []

        for (
            lower_border,
            upper_border,
            from_lower_border_to_minima,
            from_upper_border_to_maxima,
        ) in self._information_per_field:
            area_per_field.append(
                (
                    lower_border - from_lower_border_to_minima * overlap,
                    upper_border + from_upper_border_to_maxima * overlap,
                )
            )

        return tuple(area_per_field)
