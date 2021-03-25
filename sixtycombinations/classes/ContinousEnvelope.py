import abc
import itertools
import math
import typing

import expenvelope

from mu.utils import infit

from mutwo.utilities import decorators
from mutwo.utilities import tools

from mutwo.events import basic


__all__ = ("Sine", "Saw", "Triangle", "ContinousEnvelope")


class PeriodicFunction(abc.ABC):
    def __init__(self, minima: float = 0, maxima: float = 1):
        self.set_boundaries(minima, maxima)

    def __repr__(self) -> str:
        return "{}(minima = {}, maxima = {})".format(
            type(self).__name__, self.minima, self.maxima
        )

    @property
    def minima(self) -> float:
        return self._minima

    @minima.setter
    def minima(self, new_minima: float) -> float:
        try:
            assert new_minima < self.maxima
        except AssertionError:
            message = "Minima has to be smaller than maxima!"
            raise ValueError(message)

        self._minima = new_minima

    @property
    def maxima(self) -> float:
        return self._maxima

    @maxima.setter
    def maxima(self, new_maxima: float) -> float:
        try:
            assert new_maxima > self.minima
        except AssertionError:
            message = "Maxima has to be bigger than minima!"
            raise ValueError(message)

        self._maxima = new_maxima

    @property
    @abc.abstractclassmethod
    def _function_minima(self) -> float:
        raise NotImplementedError

    @property
    @abc.abstractclassmethod
    def _function_maxima(self) -> float:
        raise NotImplementedError

    @abc.abstractstaticmethod
    def _function(x: float) -> float:
        raise NotImplementedError

    def __call__(self, x: float) -> float:
        try:
            assert x >= 0 and x <= 1
        except AssertionError:
            message = "PeriodicFunction can only handle 'x' values from 0 to 1!"
            raise ValueError(message)

        return tools.scale(
            self._function(x),
            self._function_minima,
            self._function_maxima,
            self.minima,
            self.maxima,
        )

    @decorators.add_return_option
    def set_boundaries(
        self, minima: float, maxima: float
    ) -> typing.Optional["PeriodicFunction"]:
        self._minima, self.maxima = minima, maxima


class Sine(PeriodicFunction):
    _function_minima = -1
    _function_maxima = 1

    @staticmethod
    def _function(x: float) -> float:
        return math.sin(math.pi * x * 2)


class Triangle(PeriodicFunction):
    _function_minima = 0
    _function_maxima = 1

    @staticmethod
    def _function(x: float) -> float:
        if x > 0.5:
            x = abs(((x - 0.5) * 2) - 1)
        else:
            x *= 2

        return x * 1


class Saw(PeriodicFunction):
    _function_minima = 0
    _function_maxima = 1

    @staticmethod
    def _function(x: float) -> float:
        return x * 1


SegmentStart = typing.NewType("SegmentStart", float)
SegmentEnd = typing.NewType("SegmentEnd", float)
SegmentDuration = typing.NewType("SegmentDuration", float)


class ContinousEnvelopeSegment(basic.SimpleEvent):
    def __init__(self, duration: float, periodic_function: PeriodicFunction):
        super().__init__(duration)
        self.periodic_function = periodic_function


class ContinousEnvelope(object):
    def __init__(
        self,
        domain_start: float,
        domain_end: float,
        period_function: typing.Union[PeriodicFunction, infit.InfIt],
        period_size: typing.Union[float, infit.InfIt],
    ):
        if not isinstance(period_function, infit.InfIt):
            period_function = itertools.cycle((period_function,))

        if not isinstance(period_size, infit.InfIt):
            period_size = itertools.cycle((period_size,))

        self._segments = self._build_segments(
            domain_start, domain_end, period_size, period_function
        )
        self._domain_start, self._domain_end = domain_start, domain_end

    @staticmethod
    def _build_segments(
        domain_start: float,
        domain_end: float,
        period_size_maker: typing.Iterator,
        period_function_maker: typing.Iterator,
    ) -> basic.SequentialEvent[ContinousEnvelopeSegment]:
        domain_duration = domain_end - domain_start

        collected_duration = 0
        segments = basic.SequentialEvent([])

        while collected_duration < domain_duration:
            period_size = next(period_size_maker)
            period_function = next(period_function_maker)
            segment = ContinousEnvelopeSegment(period_size, period_function)
            segments.append(segment)
            collected_duration += period_size

        segments[-1].duration = segments.duration - domain_duration
        return segments

    @property
    def segments(self,) -> basic.SequentialEvent[ContinousEnvelopeSegment]:
        return self._segments

    @property
    def function(self) -> typing.Callable[[float], float]:
        return lambda x: self.value_at(x)

    @property
    def domain_start(self) -> float:
        return self._domain_start

    @domain_start.setter
    def domain_start(self, domain_start: float):
        self.scale(domain_start, self.domain_end)

    @property
    def domain_end(self) -> float:
        return self._domain_end

    @domain_end.setter
    def domain_end(self, domain_end: float):
        self.scale(self.domain_start, domain_end)

    def value_at(self, x: int) -> float:
        try:
            assert x >= self.domain_start and x <= self.domain_end
        except AssertionError:
            raise ValueError()

        adjusted_absolute_position = x - self.domain_start
        absolute_times = self.segments.absolute_times
        responsible_segment_index = self.segments.get_event_index_at(
            adjusted_absolute_position
        )
        responsible_segment = self.segments[responsible_segment_index]
        start = absolute_times[responsible_segment_index]
        try:
            end = absolute_times[responsible_segment_index + 1]
        except IndexError:
            end = self.segments.duration
        position_for_periodic_function = tools.scale(
            adjusted_absolute_position, start, end, 0, 1
        )
        return responsible_segment.periodic_function(position_for_periodic_function)

    @decorators.add_return_option
    def scale(
        self, new_domain_start: float, new_domain_end: float
    ) -> typing.Optional["ContinousEnvelope"]:
        self._segments.duration = new_domain_end - new_domain_start
        self._domain_start, self._domain_end = new_domain_start, new_domain_end

    def to_discrete_envelope(
        self,
        domain_start: float = 0,
        domain_end: float = 1,
        resolution_multiple: int = 2,
        key_point_precision: int = 2000,
        key_point_iterations: int = 5,
    ) -> expenvelope.Envelope:
        return expenvelope.Envelope.from_function(
            self.function,
            domain_start=domain_start,
            domain_end=domain_end,
            resolution_multiple=resolution_multiple,
            key_point_precision=key_point_precision,
            key_point_iterations=key_point_iterations,
        )
