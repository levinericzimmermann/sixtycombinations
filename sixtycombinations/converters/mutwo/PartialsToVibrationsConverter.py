import math
import numpy as np
import random

from mutwo import converters
from mutwo.events import basic
from mutwo.parameters import pitches

from sixtycombinations import classes
from sixtycombinations import constants as sc_constants  # sixtycombinations_c

ConvertableEvent = basic.SequentialEvent[classes.Partial]

random.seed(sc_constants.RANDOM_SEED)


class PartialsToVibrationsConverter(converters.abc.MutwoEventConverter):
    @staticmethod
    def make_vibration(
        partial: classes.Partial, loudness_level: int, n_phases: int
    ) -> classes.Vibration:
        amplitude = sc_constants.LOUDNESS_CONVERTER[partial.loudspeaker.name][
            loudness_level
        ].convert(partial.pitch.frequency)
        duration = n_phases * (1 / partial.pitch.frequency)
        return classes.Vibration(partial.pitch, duration, amplitude)

    @staticmethod
    def _how_many_phases_for_minimal_duration(
        pitch: pitches.JustIntonationPitch,
    ) -> int:
        duration_of_one_phase = 1 / pitch.frequency
        return math.ceil(
            sc_constants.MINIMAL_DURATION_OF_ONE_SOUND / duration_of_one_phase
        )

    @staticmethod
    def _make_rising_vibrations(
        partial: classes.Partial, n_phases: int
    ) -> basic.SequentialEvent[classes.Vibration]:
        # (1) finde heraus wie viele phasen du mindestens zusammen haben
        #     musst um die erwartete mindestdauer zu erfuellen.
        # (2) finde heraus wie viele von diesen mindestdauer-phasen du hast
        #     (und mache wahrscheinlich eine, die eine phase oder so mehr hat)
        # (3) gehe jede von diesen mindestdauer-objekten durch und frage ob sie
        #     klingen oder nicht, abhaengig von der gegenwaertigen wahrscheinlichkeit.
        #     die wahrscheinlichkeit faengt mit der niedrigsten ACTIVITY_LEVELS_RANGE[0]
        #     an und endet mit ACTIVITY_LEVELS_RANGE[1].
        # (4) gehe am ende jede von diesen Mindestdauer-Objekten durch und gebe denen
        #     jeweils eine steigende Lautheit von Minima zu Maxima
        # (5) wenn der ton ein connection_tone zur benachbarten harmonie ist, fange
        #     bei der wahrscheinlichkeit von der mitte zwischen maxima und minima und
        #     und fange auch bei der lautheit bei der mitte an.
        duration_of_one_phase = 1 / partial.pitch.frequency
        n_phases_for_minimal_duration = PartialsToVibrationsConverter._how_many_phases_for_minimal_duration(
            partial.pitch
        )
        n_minimal_duration_packages = int(n_phases // n_phases_for_minimal_duration)
        n_remaining_phases = n_phases % n_phases_for_minimal_duration
        n_phases_per_vibration = [
            n_phases_for_minimal_duration for _ in range(n_minimal_duration_packages)
        ]
        if n_phases_per_vibration:
            n_phases_per_vibration[0] += n_remaining_phases
        else:
            n_phases_per_vibration.append(n_remaining_phases)
        is_package_vibrating = tuple(
            random.random() < likelihood
            for likelihood in np.linspace(
                *sc_constants.ACTIVITY_RANGE, n_minimal_duration_packages, dtype=float
            )
        )
        n_vibrating_packages = len(
            tuple(filter(lambda is_vibrating: is_vibrating, is_package_vibrating))
        )
        loudness_level_per_sounding_package = (
            int(round(loudness_level))
            for loudness_level in np.linspace(
                0, sc_constants.N_LOUDNESS_LEVELS - 1, n_vibrating_packages, dtype=float
            )
        )
        vibrations = basic.SequentialEvent([])
        for n_phases, is_vibrating in zip(n_phases_per_vibration, is_package_vibrating):
            if is_vibrating:
                loudness_level = next(loudness_level_per_sounding_package)
                vibrations.append(
                    PartialsToVibrationsConverter.make_vibration(
                        partial, loudness_level, n_phases
                    )
                )
            else:
                duration = duration_of_one_phase * n_phases
                vibrations.append(basic.SimpleEvent(duration))
        return vibrations

    @staticmethod
    def _make_steady_vibrations(
        partial: classes.Partial, n_phases: int
    ) -> basic.SequentialEvent[classes.Vibration]:
        # (1) finde heraus wie viele phasen du mindestens zusammen haben
        #     musst um die erwartete mindestdauer zu erfuellen.
        # (2) finde heraus wie viele von diesen mindestdauer-phasen du hast
        #     (und mache wahrscheinlich eine, die eine phase oder so mehr hat)
        # (3) gehe einfach jeder von den mindestdauer phasen durch mit max vol
        #     und max activity (ganz einfach fuer ersten versuch, kann danach
        #     noch verbessert werden)
        duration_of_one_phase = 1 / partial.pitch.frequency
        n_phases_for_minimal_duration = PartialsToVibrationsConverter._how_many_phases_for_minimal_duration(
            partial.pitch
        )
        n_minimal_duration_packages = int(n_phases // n_phases_for_minimal_duration)
        n_remaining_phases = int(n_phases % n_phases_for_minimal_duration)
        n_phases_per_vibration = [
            n_phases_for_minimal_duration for _ in range(n_minimal_duration_packages)
        ]
        n_phases_per_vibration[0] += n_remaining_phases
        remaining_vibration_parts = n_phases - sum(n_phases_per_vibration)
        is_remaining_vibration_parts_already_used = False
        is_package_vibrating = tuple(
            random.random() < sc_constants.ACTIVITY_RANGE[-1]
            for _ in range(n_minimal_duration_packages)
        )
        vibrations = basic.SequentialEvent([])
        for n_phases, is_vibrating in zip(n_phases_per_vibration, is_package_vibrating):
            if is_vibrating:
                vibrations.append(
                    PartialsToVibrationsConverter.make_vibration(
                        partial, sc_constants.N_LOUDNESS_LEVELS - 1, n_phases
                    )
                )
            else:
                if not is_remaining_vibration_parts_already_used:
                    n_phases += remaining_vibration_parts
                    is_remaining_vibration_parts_already_used = True

                duration = duration_of_one_phase * n_phases
                vibrations.append(basic.SimpleEvent(duration))

        if not is_remaining_vibration_parts_already_used:
            duration = duration_of_one_phase * remaining_vibration_parts
            vibrations.append(basic.SimpleEvent(duration))

        return vibrations

    def _convert_partial_to_vibrations(
        self, partial: classes.Partial,
    ) -> basic.SequentialEvent[classes.Vibration]:
        vibrations = basic.SequentialEvent([])

        # (1) make attack
        vibrations.extend(self._make_rising_vibrations(partial, partial.attack))
        # (2) make sustain
        vibrations.extend(self._make_steady_vibrations(partial, partial.sustain))
        # (3) make release (inverse attack)
        vibrations.extend(
            reversed(self._make_rising_vibrations(partial, partial.release))
        )

        return vibrations

    def convert(
        self, event_to_convert: ConvertableEvent
    ) -> basic.SequentialEvent[classes.Vibration]:
        new_sequential_event = basic.SequentialEvent([])

        for partial in event_to_convert:

            # one partial to many vibrations
            if isinstance(partial, classes.Partial):
                new_sequential_event.extend(
                    self._convert_partial_to_vibrations(partial)
                )

            # rest to rest
            else:
                new_sequential_event.append(basic.SimpleEvent(partial.duration))

        return new_sequential_event
