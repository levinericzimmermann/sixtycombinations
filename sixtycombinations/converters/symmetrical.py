import functools
import itertools
import math
import numbers
import operator
import random
import typing

import expenvelope

from mutwo import converters
from mutwo.events import basic
from mutwo.events import music
from mutwo.parameters import pitches
from mutwo.utilities import tools

from mu.utils import infit

from sixtycombinations import classes
from sixtycombinations import constants as sc_constants

ConvertableEvent = basic.SequentialEvent[classes.Partial]

random.seed(sc_constants.RANDOM_SEED)


class PartialsToVibrationsConverter(converters.abc.Converter):
    def __init__(
        self, metricity_range: tuple = (0.1, 1), apply_frequency_response: bool = False
    ):
        self.activity_levels = tuple(
            infit.ActivityLevel(nth_level) for nth_level in range(11)
        )
        self.metricity_range = metricity_range
        self._apply_frequency_response = apply_frequency_response

    # ######################################################## #
    #               general static methods                     #
    # ######################################################## #

    @staticmethod
    def _add_rests(
        nested_vibrations: basic.SimultaneousEvent[
            basic.SequentialEvent[classes.Vibration]
        ],
    ) -> basic.SimultaneousEvent[basic.SequentialEvent[classes.Vibration]]:
        for absolute_time, rest in zip(
            sc_constants.WEATHER.rests.absolute_times, sc_constants.WEATHER.rests
        ):
            if rest.is_rest:
                nested_vibrations.squash_in(absolute_time, rest)

    @staticmethod
    def _cut_vibrations(
        nth_cycle: int, vibrations: basic.SequentialEvent[classes.Vibration],
    ) -> basic.SimultaneousEvent[basic.SequentialEvent[classes.Vibration]]:
        absolute_start_time = sc_constants.ABSOLUTE_START_TIME_PER_GROUP[nth_cycle]

        end_point = sc_constants.DURATION - absolute_start_time
        first_part = vibrations.cut_out(0, end_point, mutate=False)
        if absolute_start_time > 0:
            first_part.insert(0, basic.SimpleEvent(absolute_start_time))

        vibrations_duration = vibrations.duration
        if vibrations_duration > end_point:
            second_part = vibrations.cut_out(
                end_point, vibrations_duration, mutate=False
            )
        else:
            second_part = basic.SequentialEvent([])

        difference = sc_constants.DURATION - second_part.duration
        second_part.append(basic.SimpleEvent(difference))

        return basic.SimultaneousEvent([first_part, second_part])
        # return basic.SimultaneousEvent([first_part])

    @staticmethod
    def _remove_too_short_vibrations(
        vibrations: basic.SequentialEvent[classes.Vibration],
    ) -> None:
        for absolute_time, vibration in zip(vibrations.absolute_times, vibrations):
            if hasattr(vibration, "pitch"):
                frequency = vibration.pitch.frequency
                absolute_position_on_timeline = absolute_time / sc_constants.DURATION
                if absolute_position_on_timeline < 1:
                    minimal_number_of_phases = PartialsToVibrationsConverter._get_minimal_number_of_phases(
                        frequency, absolute_position_on_timeline
                    )
                    minimal_duration = (1 / frequency) * minimal_number_of_phases
                    if vibration.duration < minimal_duration:
                        vibration.pitch = None
                elif absolute_position_on_timeline == 1:
                    vibration.pitch = None
                else:
                    raise NotImplementedError()

    @staticmethod
    def _find_position_in_frequency_range(frequency: float) -> float:
        max_factor = math.log(
            sc_constants.REAL_FREQUENCY_RANGE[1] / sc_constants.REAL_FREQUENCY_RANGE[0],
            2,
        )
        current_factor = math.log(frequency / sc_constants.REAL_FREQUENCY_RANGE[0], 2)
        return current_factor / max_factor

    @staticmethod
    def _find_linear_position_in_frequency_range(frequency: float) -> float:
        difference = (
            sc_constants.REAL_FREQUENCY_RANGE[1] - sc_constants.REAL_FREQUENCY_RANGE[0]
        )
        return (frequency - sc_constants.REAL_FREQUENCY_RANGE[0]) / difference

    @staticmethod
    def _adjust_bandwidth_depending_by_vibration_pitch(
        bandwidth: float, pitch: pitches.JustIntonationPitch
    ) -> float:
        return bandwidth * (2 ** pitch.octave)

    @staticmethod
    def _adjust_range_by_dynamic_curve(
        tendency_range: typing.Tuple[float], nth_vibration: float, dynamic_curve: int
    ) -> float:
        if dynamic_curve == -1:
            nth_vibration = abs(nth_vibration - 1)
        area = tendency_range[1] - tendency_range[0]
        return tendency_range[0] + (area * nth_vibration)

    @staticmethod
    def _adjust_range_by_spectrality(
        partial: classes.Partial,
        tendency_range: typing.Tuple[float],
        absolute_position_on_timeline: float,
    ) -> typing.Tuple[float]:
        # current_spectrality = sc_constants.SPECTRALITY.value_at(
        #     absolute_position_on_timeline
        # )
        current_spectrality = sc_constants.WEATHER.get_value_of_at(
            "spectrality", absolute_position_on_timeline
        )
        equal_range_distribution = classes.EqualRangeDistribution(
            *tendency_range,
            len(sc_constants.RING_POSITION_TO_LOUDSPEAKER[partial.nth_cycle])
        )
        return tuple(reversed(equal_range_distribution(abs(current_spectrality - 1))))[
            partial.nth_active_partial
        ]

    @staticmethod
    def _adjust_range_by_filter(
        partial: classes.Partial,
        tendency_range: typing.Tuple[float],
        absolute_position_on_timeline: float,
    ) -> typing.Tuple[float]:
        position_in_frequency_range = PartialsToVibrationsConverter._find_position_in_frequency_range(
            partial.pitch.frequency
        )

        # current_filter_frequency = sc_constants.FILTER_FREQUENCY.value_at(
        #     absolute_position_on_timeline
        # )
        current_filter_frequency_range = sc_constants.WEATHER.get_range_of_at(
            "filter_frequency", absolute_position_on_timeline
        )
        # current_filter_quality = sc_constants.FILTER_Q.value_at(
        #     absolute_position_on_timeline
        # )
        current_filter_quality = sc_constants.WEATHER.get_value_of_at(
            "filter_q", absolute_position_on_timeline
        )

        if current_filter_quality <= -15:
            return tendency_range

        filter_envelope = expenvelope.Envelope.from_points(
            (0, 0, current_filter_quality),
            (current_filter_frequency_range[0], 1, 0),
            (current_filter_frequency_range[1], 1, -current_filter_quality),
            (1, 0, 0),
        )
        factor = filter_envelope.value_at(position_in_frequency_range)

        area = tendency_range[1] - tendency_range[0]

        return (tendency_range[0], tendency_range[0] + (area * factor))

    @staticmethod
    def _adjust_tendency_range(
        partial: classes.Partial,
        tendency_range: typing.Tuple[float],
        absolute_position_on_timeline: float,
    ) -> typing.Tuple[float]:
        range_adjusted_by_filter = PartialsToVibrationsConverter._adjust_range_by_filter(
            partial, tendency_range, absolute_position_on_timeline
        )
        range_adjusted_by_spectrality = PartialsToVibrationsConverter._adjust_range_by_spectrality(
            partial, range_adjusted_by_filter, absolute_position_on_timeline
        )
        return range_adjusted_by_spectrality

    @staticmethod
    def _find_likelihood(
        partial: classes.Partial,
        absolute_position_on_timeline: float,
        absolute_position_on_partial: float,
        dynamic_curve: int,
    ) -> float:
        density_range = PartialsToVibrationsConverter._adjust_tendency_range(
            partial,
            # sc_constants.DENSITY_TENDENCY.range_at(absolute_position_on_timeline),
            sc_constants.WEATHER.get_range_of_at(
                "density", absolute_position_on_timeline
            ),
            absolute_position_on_timeline,
        )

        if PartialsToVibrationsConverter._test_if_dynamic_curve_shall_be_generated(
            partial, dynamic_curve
        ):
            likelihood = PartialsToVibrationsConverter._adjust_range_by_dynamic_curve(
                density_range, absolute_position_on_partial, dynamic_curve,
            )

        else:
            likelihood = density_range[1]

        return likelihood

    @staticmethod
    def _test_if_dynamic_curve_shall_be_generated(
        partial: classes.Partial, dynamic_curve: int
    ) -> bool:
        return any(
            (
                dynamic_curve == 1
                and not partial.is_connection_pitch_to_previous_harmony,
                dynamic_curve == -1 and not partial.is_connection_pitch_to_next_harmony,
            )
        )

    # ######################################################## #
    #           calculation of loudness / amplitude            #
    # ######################################################## #

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
        loudness_range = PartialsToVibrationsConverter._adjust_tendency_range(
            partial,
            # sc_constants.LOUDNESS_TENDENCY.range_at(absolute_position_on_timeline),
            sc_constants.WEATHER.get_range_of_at(
                "loudness", absolute_position_on_timeline
            ),
            absolute_position_on_timeline,
        )

        if PartialsToVibrationsConverter._test_if_dynamic_curve_shall_be_generated(
            partial, dynamic_curve
        ):
            loudness_percentage = PartialsToVibrationsConverter._adjust_range_by_dynamic_curve(
                loudness_range, nth_vibration, dynamic_curve
            )
        else:
            loudness_range_value = loudness_range[1] - loudness_range[0]
            loudness_percentage = random.uniform(
                loudness_range[0] + (loudness_range_value * 0.7), loudness_range[1]
            )
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
        apply_frequency_response: bool,
    ) -> float:
        loudness_level = PartialsToVibrationsConverter._find_loudness_level_of_vibration(
            partial, absolute_position_on_timeline, nth_vibration, dynamic_curve
        )

        if apply_frequency_response:
            loudness_converter = sc_constants.LOUDNESS_CONVERTER_WITH_FREQUENCY_RESPONSE
        else:
            loudness_converter = (
                sc_constants.LOUDNESS_CONVERTER_WITHOUT_FREQUENCY_RESPONSE
            )

        amplitude = loudness_converter[partial.loudspeaker.name][
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
    def _get_minimal_number_of_phases_of_partial(
        partial: classes.Partial, absolute_time: float
    ) -> int:
        absolute_position_on_timeline = PartialsToVibrationsConverter._find_absolute_position_on_timeline(
            partial.nth_cycle, absolute_time
        )
        return PartialsToVibrationsConverter._get_minimal_number_of_phases(
            partial.pitch.frequency, absolute_position_on_timeline
        )

    @staticmethod
    def _get_minimal_number_of_phases(
        frequency: float, absolute_position_on_timeline: float
    ) -> int:

        # n_min_phases_range = sc_constants.MINIMAL_PHASES_PER_SOUND_TENDENCY.range_at(
        #     absolute_time
        # )
        n_min_phases_range = sc_constants.WEATHER.get_range_of_at(
            "minimal_phases_per_sound", absolute_position_on_timeline
        )

        minimal_number_of_phases = math.ceil(
            n_min_phases_range[0]
            + (
                (n_min_phases_range[1] - n_min_phases_range[0])
                # use linear (and not logarithmic) interpolation
                * PartialsToVibrationsConverter._find_linear_position_in_frequency_range(
                    frequency
                )
            )
        )

        return minimal_number_of_phases

    # ##################### #
    # activity level rhythm #
    # ##################### #

    def _decide_which_package_is_vibrating(
        self,
        partial: classes.Partial,
        package_duration_in_seconds: float,
        n_packages: int,
        absolute_time: float,
        dynamic_curve: int,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:

        is_package_vibrating = []

        for nth_package in range(n_packages):
            current_absolute_time = (
                nth_package * package_duration_in_seconds
            ) + absolute_time

            absolute_position_on_timeline = PartialsToVibrationsConverter._find_absolute_position_on_timeline(
                partial.nth_cycle, current_absolute_time
            )

            likelihood = PartialsToVibrationsConverter._find_likelihood(
                partial,
                absolute_position_on_timeline,
                nth_package / n_packages,
                dynamic_curve,
            )

            is_vibrating = next(self.activity_levels[int(likelihood * 10)])
            is_package_vibrating.append(is_vibrating)

        return is_package_vibrating

    def _find_vibrating_packages(
        self,
        partial: classes.Partial,
        n_phases: int,
        absolute_time: float,
        dynamic_curve: int,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:
        """Rhythm is based on activity levels."""
        n_phases_per_package = PartialsToVibrationsConverter._get_minimal_number_of_phases_of_partial(
            partial, absolute_time
        )
        n_packages = int(n_phases // n_phases_per_package)
        n_remaining_phases = int(n_phases % n_phases_per_package)
        n_phases_per_vibration = [n_phases_per_package for _ in range(n_packages)]

        if n_phases_per_vibration:
            n_phases_per_vibration[0] += n_remaining_phases
        else:
            n_phases_per_vibration.append(n_remaining_phases)

        is_package_vibrating = self._decide_which_package_is_vibrating(
            partial,
            partial.period_duration * n_phases_per_package,
            n_packages,
            absolute_time,
            dynamic_curve,
        )

        remaining_vibration_parts = n_phases - sum(n_phases_per_vibration)
        if remaining_vibration_parts > 0:
            n_phases_per_vibration.append(remaining_vibration_parts)
            is_package_vibrating.append(False)

        return n_phases_per_vibration, is_package_vibrating

    def _find_activity_level_rhythm_of_vibrations(
        self, partial: classes.Partial, absolute_time: float, dynamic_curve: int,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:
        """Rhythm is based on activity levels."""

        # for attack, dynamic_curve  == -1
        # for sustain, dynamic_curve == 0
        # for release, dynamic_curve == +1
        n_phases = (partial.sustain, partial.release, partial.attack)[dynamic_curve]

        n_phases_per_vibration, is_package_vibrating = self._find_vibrating_packages(
            partial, n_phases, absolute_time, dynamic_curve
        )

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

    # ##################### #
    #   stochastic rhythm   #
    # ##################### #

    @staticmethod
    def _find_likelihood_for_new_event(
        nth_beat: int,
        n_beats: int,
        last_state: bool,
        partial: classes.Partial,
        absolute_time: float,
        dynamic_curve: int,
        metricity: float,
    ) -> float:
        absolute_position_on_timeline = PartialsToVibrationsConverter._find_absolute_position_on_timeline(
            partial.nth_cycle, absolute_time
        )

        density_based_likelihood = PartialsToVibrationsConverter._find_likelihood(
            partial, absolute_position_on_timeline, nth_beat / n_beats, dynamic_curve,
        )

        # to decide if the next sound shall be a rest make the inverse density likelihood
        if last_state is True:
            density_based_likelihood = abs(1 - density_based_likelihood)

        # return metricity * density_based_likelihood
        return (metricity + density_based_likelihood) / 2

    def _initialise_start_state_of_stochastic_rhythm(
        self,
        partial: classes.Partial,
        absolute_time: float,
        dynamic_curve: int,
        beat: basic.SimpleEvent,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:
        likelihood_for_new_event = PartialsToVibrationsConverter._find_likelihood_for_new_event(
            0, 1, False, partial, absolute_time, dynamic_curve, 1
        )

        simple_event = basic.SimpleEvent(beat.duration)
        simple_event.is_vibrating = self._shall_new_event_happen(
            likelihood_for_new_event
        )
        rhythm = basic.SequentialEvent([simple_event])

        return rhythm

    @staticmethod
    def _is_last_event_long_enough(
        partial: classes.Partial,
        period_duration: float,
        absolute_time: float,
        rhythm: basic.SequentialEvent[basic.SimpleEvent],
    ) -> bool:
        duration_of_last_event_in_periods = rhythm[-1].duration / period_duration
        minimal_number_of_phases = PartialsToVibrationsConverter._get_minimal_number_of_phases_of_partial(
            partial, absolute_time
        )
        return minimal_number_of_phases <= duration_of_last_event_in_periods

    def _make_metricity_cycle(
        self, indispensability_per_beat: typing.Tuple[int],
    ) -> typing.Tuple[float]:
        max_indispensability_per_beat = max(indispensability_per_beat)
        if max_indispensability_per_beat > 0:
            metricity_per_beat = tuple(
                map(
                    lambda value: tools.scale(
                        value,
                        0,
                        max_indispensability_per_beat,
                        self.metricity_range[0],
                        self.metricity_range[1],
                    ),
                    indispensability_per_beat,
                )
            )
        else:
            metricity_per_beat = (self.metricity_range[1],)
        return itertools.cycle(metricity_per_beat)

    def _shall_new_event_happen(self, likelihood_for_new_event: float) -> bool:
        # return random.random() < likelihood_for_new_event
        return next(self.activity_levels[int(likelihood_for_new_event * 10)])

    def _process_beat(
        self,
        partial: classes.Partial,
        period_duration: float,
        dynamic_curve: int,
        metricity_cycle: itertools.cycle,
        nth_beat: int,
        n_beats: int,
        beat: basic.SimpleEvent,
        rhythm: basic.SequentialEvent[basic.SimpleEvent],
        absolute_time: float,
        added_time: float,
        n_vibrations: int,
    ) -> None:
        current_absolute_time = added_time + absolute_time
        last_state = rhythm[-1].is_vibrating
        metricity = next(metricity_cycle)
        likelihood_for_new_event = PartialsToVibrationsConverter._find_likelihood_for_new_event(
            nth_beat,
            n_beats,
            last_state,
            partial,
            current_absolute_time,
            dynamic_curve,
            metricity,
        )

        if last_state:
            likelihood_for_new_event *= int(
                PartialsToVibrationsConverter._is_last_event_long_enough(
                    partial, period_duration, current_absolute_time, rhythm
                )
            )

        make_new_event = self._shall_new_event_happen(likelihood_for_new_event)
        if make_new_event:
            simple_event = basic.SimpleEvent(beat.duration)
            simple_event.is_vibrating = not rhythm[-1].is_vibrating
            rhythm.append(simple_event)

            if simple_event.is_vibrating:
                n_vibrations += 1
        else:
            rhythm[-1].duration += beat.duration

        return rhythm, n_vibrations

    def _iterate_through_cycles(
        self,
        partial: classes.Partial,
        rhythmical_data: typing.Tuple[typing.Any],
        absolute_time: float,
        dynamic_curve: int,
    ) -> basic.SequentialEvent[basic.SimpleEvent]:

        (
            n_repetitions,
            n_periods_per_beat,
            rhythm_cycle,
            indispensability_per_beat,
        ) = rhythmical_data

        period_duration = partial.period_duration

        repeated_rhythm_cycle = functools.reduce(
            operator.add,
            (rhythm_cycle.destructive_copy() for _ in range(n_repetitions)),
        )

        metricity_cycle = self._make_metricity_cycle(indispensability_per_beat)

        n_beats_per_cycle = len(rhythm_cycle)
        n_beats = n_beats_per_cycle * n_repetitions

        rhythm = self._initialise_start_state_of_stochastic_rhythm(
            partial, absolute_time, dynamic_curve, repeated_rhythm_cycle[0]
        )
        n_vibrations = int(rhythm[0].is_vibrating)

        for nth_beat, added_time, beat in zip(
            range(n_beats),
            repeated_rhythm_cycle[1:].absolute_times,
            repeated_rhythm_cycle[1:],
        ):
            rhythm, n_vibrations = self._process_beat(
                partial,
                period_duration,
                dynamic_curve,
                metricity_cycle,
                nth_beat,
                n_beats,
                beat,
                rhythm,
                absolute_time,
                added_time,
                n_vibrations,
            )

        rhythm.set_parameter(
            "duration", lambda duration: int(duration / period_duration)
        )

        return rhythm, n_vibrations

    @staticmethod
    def _add_remaining_phases_to_stochastic_rhythm(
        rhythmical_data: typing.Tuple[typing.Any],
        rhythm: basic.SequentialEvent[basic.SimpleEvent],
        partial: classes.Partial,
        dynamic_curve: int,
    ) -> None:
        n_phases = (partial.sustain, partial.release, partial.attack)[dynamic_curve]
        remaining_phases = n_phases - (
            rhythmical_data[0] * rhythmical_data[1] * len(rhythmical_data[2])
        )
        se = basic.SimpleEvent(remaining_phases * partial.period_duration)
        se.is_vibrating = False
        rhythm.append(se)

    def _find_stochastic_rhythm_of_vibrations(
        self, partial: classes.Partial, absolute_time: float, dynamic_curve: int
    ) -> basic.SequentialEvent[basic.SimpleEvent]:
        """Rhythm is based on Barlows rhythmic model (based on metricity)."""

        rhythmical_data = partial.rhythmical_data_per_state[dynamic_curve + 1]

        rhythm, n_vibrations = self._iterate_through_cycles(
            partial, rhythmical_data, absolute_time, dynamic_curve
        )

        PartialsToVibrationsConverter._add_remaining_phases_to_stochastic_rhythm(
            rhythmical_data, rhythm, partial, dynamic_curve
        )

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
        apply_frequency_response: bool,
    ) -> classes.Vibration:
        """Generate vibration from partial data.

        :param n_phases: integer how many phases of the partial shall be played.
        :param absolute_position_on_timeline: number between 0 and 1 that indicate
            the absolute position on the timeline of the complete composition
        :param nth_vibration: number between 0 and 1 that indicate the position
            of the vibration in the current partial.
        :param dynamic_curve: 1 for cresc, -1 for decresc, 0 for static curve
        """
        amplitude = PartialsToVibrationsConverter._find_amplitude_of_vibration(
            partial,
            absolute_position_on_timeline,
            nth_vibration,
            dynamic_curve,
            apply_frequency_response,
        )
        duration = n_phases * partial.period_duration
        # attack_duration = sc_constants.ATTACK_DURATION_TENDENCY.value_at(
        #     absolute_position_on_timeline
        # )
        attack_duration = sc_constants.WEATHER.get_value_of_at(
            "attack_duration", absolute_position_on_timeline
        )
        # release_duration = sc_constants.RELEASE_DURATION_TENDENCY.value_at(
        #     absolute_position_on_timeline
        # )
        release_duration = sc_constants.WEATHER.get_value_of_at(
            "release_duration", absolute_position_on_timeline
        )
        # don't allow subtractive synthesis for very low frequencies (experience
        # showed that this does lead to satisfying musical results)
        if partial.nth_cycle == 0 and partial.nth_partial < 2:
            instrument = 1
        else:
            # instrument = sc_constants.SYNTHESIZER_CURVE.gamble_at(
            #     absolute_position_on_timeline
            # )
            instrument = sc_constants.WEATHER.get_value_of_at(
                "synthesizer", absolute_position_on_timeline
            )
        # bandwidth = PartialsToVibrationsConverter._adjust_bandwidth_depending_by_vibration_pitch(
        #     sc_constants.BANDWIDTH.value_at(absolute_position_on_timeline),
        #     partial.pitch,
        # )
        bandwidth = sc_constants.WEATHER.get_value_of_at(
            "bandwidth", absolute_position_on_timeline
        )
        # glissando_start_pitch = sc_constants.GLISSANDO_START_PITCH_CURVE.gamble_at(
        #     absolute_position_on_timeline
        # )
        glissando_start_pitch = sc_constants.WEATHER.get_value_of_at(
            "glissando_start_pitch", absolute_position_on_timeline
        )
        # glissando_end_pitch = sc_constants.GLISSANDO_END_PITCH_CURVE.gamble_at(
        #     absolute_position_on_timeline
        # )
        glissando_end_pitch = sc_constants.WEATHER.get_value_of_at(
            "glissando_end_pitch", absolute_position_on_timeline
        )
        # glissando_start_duration = sc_constants.GLISSANDO_START_DURATION_TENDENCY.value_at(
        #     absolute_position_on_timeline
        # )
        glissando_start_duration = sc_constants.WEATHER.get_value_of_at(
            "glissando_start_duration", absolute_position_on_timeline
        )
        # glissando_end_duration = sc_constants.GLISSANDO_END_DURATION_TENDENCY.value_at(
        #     absolute_position_on_timeline
        # )
        glissando_end_duration = sc_constants.WEATHER.get_value_of_at(
            "glissando_end_duration", absolute_position_on_timeline
        )
        return classes.Vibration(
            partial.pitch,
            duration,
            amplitude,
            attack_duration,
            release_duration,
            instrument,
            bandwidth,
            partial.pitch + glissando_start_pitch,
            partial.pitch + glissando_end_pitch,
            glissando_start_duration,
            glissando_end_duration,
        )

    def _make_vibrations(
        self, partial: classes.Partial, absolute_time: float, dynamic_curve: int,
    ) -> basic.SequentialEvent[classes.Vibration]:
        duration_of_one_phase = partial.period_duration
        (rhythm, n_vibrations,) = self._find_activity_level_rhythm_of_vibrations(
            partial, absolute_time, dynamic_curve
        )
        # (rhythm, n_vibrations,) = self._find_stochastic_rhythm_of_vibrations(
        #     partial, absolute_time, dynamic_curve
        # )
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
                        self._apply_frequency_response,
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

        for n_added_phases, curve_shape in zip(n_added_phases, (1, 0, -1)):
            relative_absolute_time = absolute_time + (
                n_added_phases * partial.period_duration
            )
            vibrations.extend(
                self._make_vibrations(partial, relative_absolute_time, curve_shape)
            )

        return vibrations

    # ######################################################## #
    #                    public method                         #
    # ######################################################## #

    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SimultaneousEvent[basic.SequentialEvent[classes.Vibration]]:
        new_sequential_event = basic.SequentialEvent([])

        nth_cycle = 0

        for absolute_time, partial in zip(
            event_to_convert.absolute_times, event_to_convert
        ):

            # one partial to many vibrations
            if isinstance(partial, classes.Partial):
                new_sequential_event.extend(
                    self._convert_partial_to_vibrations(absolute_time, partial)
                )
                nth_cycle = partial.nth_cycle

            # rest to rest
            else:
                new_sequential_event.append(basic.SimpleEvent(partial.duration))

        cut_out_event = PartialsToVibrationsConverter._cut_vibrations(
            nth_cycle, new_sequential_event
        )

        # PartialsToVibrationsConverter._add_rests(cut_out_event)
        # [
        #     PartialsToVibrationsConverter._remove_too_short_vibrations(vibrations)
        #     for vibrations in cut_out_event
        # ]

        return cut_out_event


class PartialsToNoteLikesConverter(PartialsToVibrationsConverter):
    def __init__(self, metricity_range: tuple = (0.1, 1)):
        self.activity_levels = tuple(
            infit.ActivityLevel(nth_level) for nth_level in range(11)
        )
        self.metricity_range = metricity_range

    def _convert_partial_to_note_likes(
        self, absolute_time: float, partial: classes.Partial
    ):
        note_likes = basic.SequentialEvent([])
        # pitch = partial.pitch.move_to_closest_register(
        #     pitches.JustIntonationPitch("16/1"), mutate=False
        # )
        pitch = partial.pitch
        """
        attack, sustain, release = (
            partial.period_duration * n_periods
            for n_periods in (partial.attack, partial.sustain, partial.release)
        )
        while note_likes.duration < sustain:
            note_likes.append(
                music.NoteLike(
                    [pitch], random.uniform(0.5, 2), random.uniform(0.2, 0.5)
                )
            )

        difference = note_likes.duration - sustain
        note_likes.duration -= difference

        note_likes.insert(0, basic.SimpleEvent(attack))
        note_likes.append(basic.SimpleEvent(release))
        """

        while note_likes.duration < partial.duration:
            note_likes.append(
                music.NoteLike(
                    [pitch], random.uniform(0.5, 2), random.uniform(0.1, 0.2)
                )
            )

        difference = note_likes.duration - partial.duration
        note_likes.duration -= difference

        return note_likes

    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SimultaneousEvent[basic.SequentialEvent[music.NoteLike]]:
        new_sequential_event = basic.SequentialEvent([])

        nth_cycle = 0

        for absolute_time, partial in zip(
            event_to_convert.absolute_times, event_to_convert
        ):

            # one partial to many NoteLike
            if isinstance(partial, classes.Partial) and partial.nth_partial in (1,):
                new_sequential_event.extend(
                    self._convert_partial_to_note_likes(absolute_time, partial)
                )
                nth_cycle = partial.nth_cycle

            # rest to rest
            else:
                new_sequential_event.append(basic.SimpleEvent(partial.duration))

        # cut_out_event = PartialsToVibrationsConverter._cut_vibrations(
        #     nth_cycle, new_sequential_event
        # )[0]

        # return basic.SimultaneousEvent([cut_out_event])


        cut_out_event = PartialsToVibrationsConverter._cut_vibrations(
            nth_cycle, new_sequential_event
        )

        return cut_out_event
