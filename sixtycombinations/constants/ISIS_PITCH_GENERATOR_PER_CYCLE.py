"""Definition of class and objects to find pitches for ISiS rendering."""

import operator
import typing

import expenvelope
from mutwo.parameters import pitches
from mutwo.utilities import tools

from sixtycombinations.constants import Group
from sixtycombinations.constants import GROUPS

from sixtycombinations.constants import ABSOLUTE_START_TIME_PER_GROUP
from sixtycombinations.constants import DURATION


class IsisPitchGenerator(object):
    def __init__(self, nth_cycle: int, groups: typing.Tuple[Group]):
        self._pitch_and_envelope_pairs = IsisPitchGenerator._extract_pitch_and_envelope_pairs_from_groups(
            nth_cycle, groups
        )

    # ######################################################## #
    #                   static methods                         #
    # ######################################################## #

    @staticmethod
    def _make_points_for_group(
        nth_cycle: int, group: Group,
    ) -> typing.Tuple[typing.Tuple[float, float]]:
        absolute_start_time_of_group = (
            group.relative_start_time + ABSOLUTE_START_TIME_PER_GROUP[nth_cycle]
        )
        period_duration = 1 / group.fundamental.frequency
        points = []
        for n_periods, weight in zip(
            tools.accumulate_from_zero((group.attack, group.sustain, group.release)),
            (0, 1, 1, 0),
        ):
            absolute_start_time_of_state = (
                absolute_start_time_of_group + (n_periods * period_duration)
            ) % DURATION
            absolute_position_on_timeline = absolute_start_time_of_state / DURATION
            points.append((absolute_position_on_timeline, weight))

        return tuple(points)

    @staticmethod
    def _extract_pitch_and_envelope_pairs_from_groups(
        nth_cycle: int, groups: typing.Tuple[Group],
    ) -> typing.Tuple[typing.Tuple[pitches.JustIntonationPitch, expenvelope.Envelope]]:
        pitch_and_points_pairs = dict([])
        for group in groups:
            points = IsisPitchGenerator._make_points_for_group(nth_cycle, group)
            for pitch in group.harmony:
                pitch = pitch.normalize(mutate=False)
                if not (pitch.exponents in pitch_and_points_pairs):
                    pitch_and_points_pairs.update({pitch.exponents: (pitch, [])})

                pitch_and_points_pairs[pitch.exponents][1].extend(points)

        pitch_and_points_pairs = tuple(
            (pitch, sorted(points, key=operator.itemgetter(0)))
            for pitch, points in pitch_and_points_pairs.values()
        )

        return tuple(
            (pitch, expenvelope.Envelope.from_points(*points))
            for pitch, points in pitch_and_points_pairs
        )

    # ######################################################## #
    #                   public methods                         #
    # ######################################################## #

    def __call__(
        self, absolute_position_on_timeline: float
    ) -> typing.Tuple[typing.Tuple[pitches.JustIntonationPitch, float]]:
        pitch_and_weight_pairs = []
        for pitch, envelope in self._pitch_and_envelope_pairs:
            weight = envelope.value_at(absolute_position_on_timeline)
            if weight > 0:
                pitch_and_weight_pairs.append((pitch, weight))
        return tuple(pitch_and_weight_pairs)


ISIS_PITCH_GENERATOR_PER_CYCLE = tuple(
    IsisPitchGenerator(nth_cycle, groups) for nth_cycle, groups in enumerate(GROUPS)
)
