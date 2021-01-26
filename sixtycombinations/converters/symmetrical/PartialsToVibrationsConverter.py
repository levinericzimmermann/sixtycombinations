import math
import numbers

# import numpy as np
import random
import typing

from mutwo import converters
from mutwo.events import basic
from mutwo.parameters import pitches
from mutwo.utilities import tools

from sixtycombinations import classes
from sixtycombinations import constants as sc_constants

ConvertableEvent = basic.SequentialEvent[classes.Partial]

random.seed(sc_constants.RANDOM_SEED)


class PartialsToVibrationsConverter(converters.abc.Converter):

    # ######################################################## #
    #           calculation of loudness / amplitude            #
    # ######################################################## #

    @staticmethod
    def _find_loudness_range_depending_on_spectrality(
        partial: classes.Partial, absolute_position_on_timeline: float
    ) -> typing.Tuple[float]:
        current_spectrality = sc_constants.SPECTRALITY.value_at(
            absolute_position_on_timeline
        )
        loudness_range = sc_constants.LOUDNESS_TENDENCY.range_at(
            absolute_position_on_timeline
        )
        equal_range_distribution = classes.EqualRangeDistribution(
            *loudness_range,
            len(sc_constants.RING_POSITION_TO_LOUDSPEAKER[partial.nth_cycle])
        )
        return tuple(reversed(equal_range_distribution(current_spectrality)))[
            partial.nth_active_partial
        ]

    @staticmethod
    def _find_loudness_level_for_dynamic_level(
        loudness_range: typing.Tuple[float], nth_vibration: float, dynamic_curve: int
    ) -> float:
        if dynamic_curve == -1:
            nth_vibration = abs(nth_vibration - 1)
        area = loudness_range[1] - loudness_range[0]
        return loudness_range[0] + (area * nth_vibration)

    @staticmethod
    def _loudness_percentage_to_loudness_level(loudness_percentage: float) -> int:
        return int((sc_constants.N_LOUDNESS_LEVELS - 1) * loudness_percentage)

    @staticmethod
    def _find_loudness_level_of_vibration(
        partial: classes.Partial,
        absolute_position_on_timeline: float,
        nth_vibration: float,
        dynamic_curve: int,  # -1, 0, 1
    ) -> int:
        loudness_range = PartialsToVibrationsConverter._find_loudness_range_depending_on_spectrality(
            partial, absolute_position_on_timeline
        )

        if dynamic_curve != 0:
            loudness_percentage = PartialsToVibrationsConverter._find_loudness_level_for_dynamic_level(
                loudness_range, nth_vibration, dynamic_curve
            )
        else:
            loudness_percentage = random.uniform(*loudness_range)
            # loudness_percentage = loudness_range[1]

        return PartialsToVibrationsConverter._loudness_percentage_to_loudness_level(
            loudness_percentage
        )

    @staticmethod
    def _find_amplitude_of_vibration(
        partial: classes.Partial,
        absolute_position_on_timeline: float,
        nth_vibration: float,
        dynamic_curve: int,  # -1, 0, 1
    ) -> float:
        loudness_level = PartialsToVibrationsConverter._find_loudness_level_of_vibration(
            partial, absolute_position_on_timeline, nth_vibration, dynamic_curve
        )
        amplitude = sc_constants.LOUDNESS_CONVERTER[partial.loudspeaker.name][
            loudness_level
        ].convert(partial.pitch.frequency)
        return amplitude

    # ######################################################## #
    #               calculation of time and rhythm             #
    # ######################################################## #

    @staticmethod
    def _find_absolute_position_on_timeline(
        nth_cycle: int, absolute_time: numbers.Number
    ) -> float:
        """Return value between 0 to 1 where 0 is the absolute start.

        Helper method to identify the position of an event (to gain
        knowledge about the current values of different global Tendency and
        Envelope objects).
        """

        absolute_time += sc_constants.ABSOLUTE_START_TIME_PER_GROUP[nth_cycle]
        absolute_time %= sc_constants.DURATION
        return absolute_time / sc_constants.DURATION

    @staticmethod
    def _how_many_phases_for_minimal_duration(
        pitch: pitches.JustIntonationPitch,
    ) -> int:
        duration_of_one_phase = 1 / pitch.frequency
        return math.ceil(
            sc_constants.MINIMAL_DURATION_OF_ONE_SOUND.value_at(0)
            / duration_of_one_phase
        )

    @staticmethod
    def _find_rhythm_of_vibrations(
        partial: classes.Partial, n_phases: int, absolute_time: float,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:
        n_phases_for_minimal_duration = PartialsToVibrationsConverter._how_many_phases_for_minimal_duration(
            partial.pitch
        )
        n_minimal_duration_packages = int(n_phases // n_phases_for_minimal_duration)
        n_remaining_phases = int(n_phases % n_phases_for_minimal_duration)
        n_phases_per_vibration = [
            n_phases_for_minimal_duration for _ in range(n_minimal_duration_packages)
        ]

        if n_phases_per_vibration:
            n_phases_per_vibration[0] += n_remaining_phases
        else:
            n_phases_per_vibration.append(n_remaining_phases)

        is_package_vibrating = [
            random.random() < sc_constants.ACTIVITY_RANGE[-1]
            for _ in range(n_minimal_duration_packages)
        ]

        remaining_vibration_parts = n_phases - sum(n_phases_per_vibration)
        if remaining_vibration_parts > 0:
            n_phases_per_vibration.append(remaining_vibration_parts)
            is_package_vibrating.append(False)

        rhythm = basic.SequentialEvent([])
        n_vibrations = 0
        for n_phases, is_vibrating in zip(n_phases_per_vibration, is_package_vibrating):
            if rhythm and rhythm[-1].is_vibrating == is_vibrating:
                rhythm[-1].duration += n_phases
            else:
                se = basic.SimpleEvent(n_phases)
                se.is_vibrating = is_vibrating
                rhythm.append(se)
                if is_vibrating:
                    n_vibrations += 1

        return rhythm, n_vibrations

    # ######################################################## #
    #               generation of vibrations                   #
    # ######################################################## #

    @staticmethod
    def make_vibration(
        partial: classes.Partial,
        n_phases: int,
        absolute_position_on_timeline: float,
        nth_vibration: float,
        dynamic_curve: int,  # -1, 0, 1
    ) -> classes.Vibration:
        """Generate vibration from partial data.

        :param n_phases: integer how many phases of the partial shall be played.
        :param absolute_position_on_timeline: number between 0 and 1 that indicate
            the absolute position on the timeline of the complete composition
        :param nth_vibration: number between 0 and 1 that indicate the position
            of the vibration in the current partial.
        :param is_rising: whether the loudness curve shall rise (cresc.) of if it
            should be static
        """
        amplitude = PartialsToVibrationsConverter._find_amplitude_of_vibration(
            partial, absolute_position_on_timeline, nth_vibration, dynamic_curve
        )
        duration = n_phases * partial.period_duration
        return classes.Vibration(partial.pitch, duration, amplitude)

    @staticmethod
    def _make_vibrations(
        partial: classes.Partial,
        n_phases: int,
        absolute_time: float,
        dynamic_curve: int,
    ) -> basic.SequentialEvent[classes.Vibration]:
        duration_of_one_phase = partial.period_duration
        rhythm, n_vibrations = PartialsToVibrationsConverter._find_rhythm_of_vibrations(
            partial, n_phases, absolute_time
        )
        nth_vibration = 0
        vibrations = basic.SequentialEvent([])
        for absolute_phases, part in zip(rhythm.absolute_times, rhythm):
            relative_absolute_time = absolute_time + (
                absolute_phases * duration_of_one_phase
            )
            absolute_position_on_timeline = PartialsToVibrationsConverter._find_absolute_position_on_timeline(
                partial.nth_cycle, relative_absolute_time
            )
            if part.is_vibrating:
                vibrations.append(
                    PartialsToVibrationsConverter.make_vibration(
                        partial,
                        part.duration,
                        absolute_position_on_timeline,
                        nth_vibration / n_vibrations,
                        dynamic_curve,
                    )
                )
                nth_vibration += 1
            else:
                duration = duration_of_one_phase * part.duration
                vibrations.append(basic.SimpleEvent(duration))

        return vibrations

    def _convert_partial_to_vibrations(
        self, absolute_time: float, partial: classes.Partial,
    ) -> basic.SequentialEvent[classes.Vibration]:
        vibrations = basic.SequentialEvent([])

        n_phases_per_part = (partial.attack, partial.sustain, partial.release)
        n_added_phases = tools.accumulate_from_zero(n_phases_per_part)

        for n_phases, n_added_phases, curve_shape in zip(
            n_phases_per_part, n_added_phases, (1, 0, -1)
        ):
            relative_absolute_time = absolute_time + (
                n_added_phases * partial.period_duration
            )
            vibrations.extend(
                self._make_vibrations(
                    partial, n_phases, relative_absolute_time, curve_shape
                )
            )

        return vibrations

    # ######################################################## #
    #                    public method                         #
    # ######################################################## #

    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SequentialEvent[classes.Vibration]:
        new_sequential_event = basic.SequentialEvent([])

        for absolute_time, partial in zip(
            event_to_convert.absolute_times, event_to_convert
        ):

            # one partial to many vibrations
            if isinstance(partial, classes.Partial):
                new_sequential_event.extend(
                    self._convert_partial_to_vibrations(absolute_time, partial)
                )

            # rest to rest
            else:
                new_sequential_event.append(basic.SimpleEvent(partial.duration))

        return new_sequential_event
