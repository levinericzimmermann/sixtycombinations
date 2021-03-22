"""Definition of rhythmical grids for ISiS rendering."""

import operator

import expenvelope
from mutwo.events import basic
from mutwo.generators import edwards

from sixtycombinations.constants import DURATION
from sixtycombinations.constants import NESTED_PARTIALS

ISIS_RHYTHMICAL_GRID_PER_CYCLE = []

MIN_DISTANCE = 0.2  # seconds

for cycle in NESTED_PARTIALS:
    beat_and_weight_pairs = []

    for loudspeaker in cycle:

        for a_or_b in loudspeaker:

            for partial in a_or_b:

                if (
                    hasattr(partial, "rhythmical_data_per_state")
                    and partial.nth_partial == 1
                ):

                    absolute_start_time_per_state = (
                        partial.absolute_start_time_per_state
                    )
                    rhythmical_data_per_state = partial.rhythmical_data_per_state
                    for (
                        nth_state,
                        absolute_start_time_of_current_state,
                        rhythmical_data,
                    ) in zip(
                        range(len(rhythmical_data_per_state)),
                        absolute_start_time_per_state,
                        rhythmical_data_per_state,
                    ):

                        n_repetitions, n_periods, rhythm, _ = rhythmical_data
                        rhythm = basic.SequentialEvent(
                            rhythm * n_repetitions
                        ).destructive_copy()

                        if nth_state == 0:
                            envelope_points = ((0, 0), (rhythm.duration, 10))

                        elif nth_state == 1:
                            envelope_points = ((0, 10), (rhythm.duration, 10))

                        elif nth_state == 2:
                            envelope_points = ((0, 10), (rhythm.duration, 0))

                        else:
                            raise NotImplementedError()

                        weight_envelope = expenvelope.Envelope.from_points(
                            *envelope_points
                        )

                        for relative_start_time in rhythm.absolute_times:
                            beat_and_weight_pairs.append(
                                (
                                    (
                                        relative_start_time
                                        + absolute_start_time_of_current_state
                                    )
                                    % DURATION,
                                    round(
                                        weight_envelope.value_at(relative_start_time)
                                    ),
                                )
                            )

    activity_level = edwards.ActivityLevel()
    absolute_beats = sorted(
        set(
            absolute_time
            for absolute_time, weight in sorted(
                beat_and_weight_pairs, key=operator.itemgetter(0)
            )
            if activity_level(weight)
        )
    )

    filtered_absolute_beats = [absolute_beats[0]]
    for absolute_beat in absolute_beats:
        if (absolute_beat - filtered_absolute_beats[-1]) >= MIN_DISTANCE:
            filtered_absolute_beats.append(absolute_beat)

    rhythmical_grid = basic.SequentialEvent(
        [
            basic.SimpleEvent(b - a)
            for a, b in zip(filtered_absolute_beats, filtered_absolute_beats[1:])
        ]
    )

    ISIS_RHYTHMICAL_GRID_PER_CYCLE.append(rhythmical_grid)
