import random

import expenvelope
import yamm

from mu.utils import infit

from mutwo.parameters import pitches

from sixtycombinations import classes
from sixtycombinations.constants import DURATION

random.seed(100)


STATES = (
    classes.State(
        "default",
        {
            "attack_duration": classes.Tendency(
                classes.ContinousEnvelope(
                    0, DURATION, classes.Triangle(1.8, 2.2), infit.Gaussian(5, 1, 5)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0, DURATION, classes.Triangle(2.9, 3.4), infit.Gaussian(7, 1, 10)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "release_duration": classes.Tendency(
                classes.ContinousEnvelope(
                    0, DURATION, classes.Sine(1, 2.3), infit.Gaussian(3, 0.1, 5)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0, DURATION, classes.Sine(2.4, 3.4), infit.Gaussian(4, 0.2, 10)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (0.5, 0.01), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (0.5, 0.2), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 11), (1, 11)),
                expenvelope.Envelope.from_points((0, 13900), (1, 13900)),
            ),
            "spectrality": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Sine(0, 1),
                        classes.Triangle(0, 0.8),
                        classes.Sine(0, 1),
                        classes.Sine(0.2, 0.7),
                        classes.Triangle(0, 1),
                    )
                ),
                infit.Cycle((20, 5, 15, 25, 5, 7)),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.25), (1, 0.25)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "loudness": classes.Tendency(
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle((classes.Sine(0.25, 0.4), classes.Sine(0.28, 0.45),)),
                    infit.Cycle((20, 30, 20)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle((classes.Sine(0.68, 0.79), classes.Sine(0.7, 0.85),)),
                    infit.Cycle((20, 20, 30)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    classes.ContinousEnvelope(
                        0,
                        DURATION,
                        infit.Cycle(
                            (
                                classes.Sine(0.2, 0.3),
                                classes.Triangle(0.2, 0.5),
                                classes.Triangle(0.2, 0.3),
                            )
                        ),
                        infit.Gaussian(20, 3, seed=33),
                    )
                    .scale(0, 1, mutate=False)
                    .to_discrete_envelope(),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Sine(0.81, 1.3), classes.Triangle(0.7, 1.8),)),
                infit.Cycle((13, 4, 10)),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
                ),
            ),
            "rest_duration": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Sine(0.008, 0.05), classes.Sine(0.004, 0.07))),
                infit.Gaussian(5, 1),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.07), (1, 0.07)),
            "bandwidth_singer0": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Choice(
                    (
                        classes.Triangle(4, 13),
                        classes.Triangle(11, 15),
                        classes.Triangle(2, 5),
                        classes.Triangle(10, 12),
                    ),
                    seed=341234,
                ),
                infit.Gaussian(9, 1, seed=11113),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer1": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Choice(
                    (
                        classes.Triangle(5, 8),
                        classes.Triangle(1, 5),
                        classes.Triangle(5, 9),
                    ),
                    seed=1234,
                ),
                infit.Gaussian(7, 2, seed=11113),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer2": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Choice(
                    (classes.Triangle(2.8, 5.2), classes.Triangle(1, 3)), seed=3
                ),
                infit.Gaussian(6, 1, seed=11113),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 0.75), (1, 0.75)),
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
        },
        lambda: random.uniform(117, 182),
        lambda: random.uniform(35, 45),
        0,
        0,
    ),
    classes.State(
        "calm_default",
        {
            "attack_duration": classes.Tendency(
                classes.ContinousEnvelope(
                    0, DURATION, classes.Triangle(2.8, 3.2), infit.Gaussian(5, 1, 5)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0, DURATION, classes.Triangle(3.9, 4.4), infit.Gaussian(7, 1, 10)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "release_duration": classes.Tendency(
                classes.ContinousEnvelope(
                    0, DURATION, classes.Sine(2, 3.3), infit.Gaussian(3, 0.1, 5)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0, DURATION, classes.Sine(3.4, 4.4), infit.Gaussian(4, 0.2, 10)
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (0.5, 0.01), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (0.5, 0.2), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 27), (1, 27)),
                expenvelope.Envelope.from_points((0, 15900), (1, 15900)),
            ),
            "spectrality": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Sine(0.45, 1),
                        classes.Triangle(0.4, 1),
                        classes.Sine(0.5, 1),
                        classes.Sine(0.7, 1),
                        classes.Triangle(0.35, 1),
                    )
                ),
                infit.Cycle((20, 30, 28, 18, 19, 25)),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.91)),
            ),
            "loudness": classes.Tendency(
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle(
                        (
                            classes.Sine(0.12, 0.2),
                            classes.Sine(0.18, 0.3),
                            classes.Triangle(0.09, 0.19),
                        )
                    ),
                    infit.Cycle((30, 30, 20, 18)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle((classes.Sine(0.58, 0.64), classes.Sine(0.4, 0.5),)),
                    infit.Cycle((20, 20, 30)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Sine(14, 20.3), classes.Triangle(15, 32),)),
                infit.Uniform(10, 20, seed=123454321),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "rest_duration": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Sine(0.01, 0.11),
                        classes.Sine(0.01, 0.085),
                        classes.Triangle(0.05, 0.13),
                    )
                ),
                infit.Uniform(5, 8),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.45)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.35), (1, 0.35)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.03), (1, 0.04)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 6), (1, 6)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 4), (1, 5)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 3), (1, 3)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2),
                (
                    expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
        },
        lambda: random.uniform(120, 190),
        lambda: 46,
        0,
        0,
    ),
    classes.State(
        "explosion",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 2.2), (1, 2.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
                expenvelope.Envelope.from_points((0, 2.2), (1, 2.1)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 9), (1, 9)),
                expenvelope.Envelope.from_points((0, 4050), (1, 4050)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.54), (1, 0.54)),
                expenvelope.Envelope.from_points((0, 0.79), (1, 0.79)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 0.95), (1, 0.985)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 5.51), (1, 4.21),),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.35), (1, 0.35)),
                ),
            ),
            "rest_duration": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Sine(0.4, 0.6),)),
                infit.Uniform(5, 8),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            "bandwidth_singer0": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Triangle(1, 9),
                        classes.Triangle(6, 14),
                        classes.Triangle(10, 12),
                    )
                ),
                infit.Uniform(2, 4),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer1": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Triangle(6, 8),
                        classes.Sine(4, 12),
                        classes.Triangle(1, 9),
                    )
                ),
                infit.Uniform(2, 5),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer2": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(3, 6), classes.Sine(1, 7),)),
                infit.Uniform(1, 3, seed=442),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
                expenvelope.Envelope.from_points((0, 2), (1, 2)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                ),
            ),
        },
        lambda: random.uniform(82, 98),
        lambda: 20,
        4,
        -4,
    ),
    classes.State(
        "extreme_explosion",  # more dense and brutal version of explosion
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 8), (1, 8)),
                expenvelope.Envelope.from_points((0, 4050), (1, 4050)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.78), (1, 0.78)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.68), (1, 0.67)),
                expenvelope.Envelope.from_points((0, 0.88), (1, 0.88)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 0.95), (1, 0.985)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(4, 12), classes.Sine(3, 8),)),
                infit.Uniform(5, 9, seed=442),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.24), (1, 0.24)),
                ),
            ),
            "rest_duration": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(0.3, 0.6), classes.Sine(0.4, 0.6),)),
                infit.Uniform(1, 3, seed=442),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.75), (1, 0.75)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.85), (1, 0.85)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            "bandwidth_singer0": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Triangle(1, 15),
                        classes.Triangle(6, 14),
                        classes.Triangle(10, 12),
                    )
                ),
                infit.Uniform(2, 4),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer1": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Triangle(6, 9),
                        classes.Sine(4, 12),
                        classes.Triangle(1, 9),
                    )
                ),
                infit.Uniform(2, 5),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer2": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(3, 6), classes.Sine(1, 7),)),
                infit.Uniform(1, 3, seed=442),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
                expenvelope.Envelope.from_points((0, 2), (1, 2)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
                ),
            ),
        },
        lambda: random.uniform(79, 98),
        lambda: 15,
        4,
        -4,
    ),
    classes.State(
        "damped",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.3), (1, 3.3)),
                expenvelope.Envelope.from_points((0, 5.2), (1, 5.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.8), (1, 3.8)),
                expenvelope.Envelope.from_points((0, 5.8), (1, 5.8)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 1.01), (1, 1.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 98), (1, 98)),
                expenvelope.Envelope.from_points((0, 12000), (1, 12000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.92), (1, 0.92)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.77), (0.5, 0.6), (1, 0.72)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.31), (0.5, 0.2), (1, 0.32)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Sine(15, 24.19),
                        classes.Triangle(20, 32.19),
                        classes.Triangle(14, 29),
                    )
                ),
                infit.Uniform(4, 14),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle(
                        (classes.Triangle(0.19, 0.28), classes.Sine(0.19, 0.28),)
                    ),
                    infit.Uniform(13, 19, seed=100),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "filter_q": classes.ContinousEnvelope(
                0, DURATION, classes.Triangle(10, 12), infit.Uniform(10, 30),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points(
                (0, 0.03), (0.5, 0.04), (1, 0.03),
            ),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.22), (1, 0.25)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.09), (1, 0.09)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.325), (1, 0.325)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.24), (1, 0.24)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 4), (1, 4)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 2), (1, 2)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
        },
        lambda: random.uniform(97, 105),
        lambda: 62.85,
        0,
        0,
    ),
    classes.State(
        "alternative_damped",  # noisy version with a dense bass singer
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3), (1, 3)),
                expenvelope.Envelope.from_points((0, 5.2), (1, 5.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.1), (1, 3.1)),
                expenvelope.Envelope.from_points((0, 5.2), (1, 5.2)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 1.01), (1, 1.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 98), (1, 98)),
                expenvelope.Envelope.from_points((0, 24000), (1, 24000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.62), (1, 0.62)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(40, 185.19), classes.Triangle(66, 123),)),
                infit.Uniform(4, 14),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Cycle(
                        (classes.Triangle(0.24, 0.32), classes.Sine(0.23, 0.31),)
                    ),
                    infit.Uniform(13, 19, seed=100),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "filter_q": classes.ContinousEnvelope(
                0, DURATION, classes.Triangle(9, 11), infit.Uniform(10, 30),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                ),
            ),
            "rest_duration": classes.ContinousEnvelope(
                0, DURATION, classes.Triangle(0.008, 0.04), infit.Gaussian(20, 5)
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                expenvelope.Envelope.from_points((0, 0.55), (1, 0.55)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.09), (1, 0.99)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.125), (1, 0.125)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.42), (1, 0.42)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "bandwidth_singer0": classes.ContinousEnvelope(
                0, DURATION, classes.Triangle(2, 13), infit.Gaussian(10, 6)
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 2), (1, 2)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.32), (1, 0.3)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
        },
        lambda: random.uniform(87, 103),
        lambda: 68.85,
        0,
        0,
    ),
    classes.State(
        "very_damped",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.3), (1, 3.3)),
                expenvelope.Envelope.from_points((0, 5.2), (1, 5.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.8), (1, 3.8)),
                expenvelope.Envelope.from_points((0, 5.8), (1, 5.8)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 1.01), (1, 1.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 42), (1, 42)),
                expenvelope.Envelope.from_points((0, 9000), (1, 9000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                expenvelope.Envelope.from_points((0, 0.84), (1, 0.85)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle(
                    (
                        classes.Sine(43, 52.19),
                        classes.Triangle(30, 50.19),
                        classes.Triangle(9, 23),
                    )
                ),
                infit.Uniform(20, 39),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                expenvelope.Envelope.from_points((0, 0.12), (1, 0.12)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, 13), (1, 13),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.7), (1, 0.8)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.1), (1, 0.1),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # no
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.25), (1, 0.25)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.18), (1, 0.18)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.0001), (1, 0.0001)),
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 6), (1, 6)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 3), (1, 3)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
        },
        lambda: 65,
        lambda: 10,
        0,
        0,
    ),
    classes.State(
        "xenakis",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.8)),
                expenvelope.Envelope.from_points((0, 1.8), (1, 1.8)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.4), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.6)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 1.01), (1, 1.01)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                # expenvelope.Envelope.from_points((0, 40), (1, 40)),
                # expenvelope.Envelope.from_points((0, 950), (1, 950)),
                expenvelope.Envelope.from_points((0, 100), (1, 100)),
                expenvelope.Envelope.from_points((0, 12000), (1, 12000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 17.91), (1, 17.91),),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.68), (1, 0.68)),
                expenvelope.Envelope.from_points((0, 0.999), (1, 0.999)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, 14), (1, 14),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.005), (1, 0.005),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.0000001), (1, 0.0000001)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.000001), (1, 0.0001)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 3), (1, 3)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 3), (1, 3)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 4), (1, 4)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.38), (1, 0.38)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    expenvelope.Envelope.from_points((0, 0.25), (1, 0.25)),
                ),
            ),
        },
        lambda: random.uniform(110, 130),
        lambda: 70,
        0,
        0,
    ),
    classes.State(
        "calm_xenakis",  # aka birds ;)
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.8)),
                expenvelope.Envelope.from_points((0, 1.8), (1, 1.8)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.4), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.4)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.3)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("8/9"),
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                    pitches.JustIntonationPitch("9/8"),
                ),
                (
                    # 8/9
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 0.45), (1, 0.45)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 9/8
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.35), (1, 0.35)),
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 70), (1, 70)),
                expenvelope.Envelope.from_points((0, 8000), (1, 8000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    infit.Choice((classes.Triangle(0.6, 0.8), classes.Sine(0.7, 0.8),)),
                    infit.Uniform(10, 20),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": classes.ContinousEnvelope(
                0,
                DURATION,
                infit.Cycle((classes.Triangle(20, 70), classes.Triangle(40, 60),)),
                infit.Uniform(3, 10),
            )
            .scale(0, 1, mutate=False)
            .to_discrete_envelope(),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.67)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, 14), (1, 14),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.1), (1, 0.1),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.005), (1, 0.005)),
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.38), (1, 0.38)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1, 2, 4),
                (
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
        },
        lambda: random.uniform(100, 120),
        lambda: 72,
        0,
        0,
    ),
    classes.State(
        "static",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 4.9), (1, 4.9)),
                expenvelope.Envelope.from_points((0, 7.2), (1, 7.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 5), (1, 5)),
                expenvelope.Envelope.from_points((0, 8), (1, 8)),
            ),
            "glissando_start_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                ),
                (
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 3.2), (1, 3.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                ),
            ),
            "glissando_end_pitch": classes.DynamicChoice(
                (
                    pitches.JustIntonationPitch("15/16"),
                    pitches.JustIntonationPitch("24/25"),
                    pitches.JustIntonationPitch("1/1"),
                    pitches.JustIntonationPitch("25/24"),
                    pitches.JustIntonationPitch("16/15"),
                ),
                (
                    # 15/16
                    expenvelope.Envelope.from_points((0, 0.14), (1, 0.14)),
                    # 24/25
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 1/1
                    expenvelope.Envelope.from_points((0, 3.2), (1, 3.2)),
                    # 25/24
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # 16/15
                    expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                ),
            ),
            "glissando_start_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
            ),
            "glissando_end_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
            ),
            "minimal_phases_per_sound": classes.Tendency(
                expenvelope.Envelope.from_points((0, 60), (1, 60)),
                expenvelope.Envelope.from_points((0, 27050), (1, 27050)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    classes.Triangle(0.57, 0.65),
                    infit.Cycle((15, 20, 18, 30)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
                classes.ContinousEnvelope(
                    0,
                    DURATION,
                    classes.Triangle(0.5725, 0.6525),
                    infit.Cycle((15, 20, 18, 30)),
                )
                .scale(0, 1, mutate=False)
                .to_discrete_envelope(),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 0.81), (1, 0.81),),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.99), (1, 0.99)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.005), (1, 0.005),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # no
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # no
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # yes
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # no
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.75), (1, 0.75)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.75), (1, 0.75)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.06), (1, 0.06)),
            ),
            # ################################################## #
            #         attributes for isis:                       #
            # ################################################## #
            "density_singer0": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density_singer1": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density_singer2": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "bandwidth_singer0": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "bandwidth_singer1": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "bandwidth_singer2": expenvelope.Envelope.from_points((0, 1), (1, 1)),
            "volume_range_singer0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range_singer1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
            ),
            "volume_range_singer2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
            ),
            "isis_rhythmical_division": classes.DynamicChoice(
                (1,), (expenvelope.Envelope.from_points((0, 1), (1, 1)),),
            ),
        },
        lambda: random.uniform(225, 265),
        lambda: 32,
        0,
        0,
    ),
)

CHAIN = yamm.Chain(
    {
        ("default",): {"damped": 2, "explosion": 2, "xenakis": 1},
        ("explosion",): {"default": 1, "static": 2, "xenakis": 1},
        ("damped",): {"default": 3, "very_damped": 1, "explosion": 1},
        ("very_damped",): {"damped": 1},
        ("xenakis",): {"default": 2, "explosion": 1},
        ("static",): {"default": 1, "xenakis": 1},
    }
)
CHAIN.make_deterministic_map()

LOOKUP = classes.Lookup(
    {
        "default": infit.Cycle(("default", "calm_default", "default")),
        "explosion": infit.Cycle(("explosion", "explosion", "extreme_explosion")),
        # "explosion": infit.Cycle(("extreme_explosion",)),
        "damped": infit.Cycle(("damped", "alternative_damped", "damped")),
        "very_damped": infit.Value("very_damped"),
        "xenakis": infit.Cycle(("xenakis", "calm_xenakis")),
        "static": infit.Value("static"),
    }
)

WEATHER = classes.Weather("xenakis", STATES, CHAIN, LOOKUP, DURATION, seed=150)
# WEATHER = classes.Weather("explosion", STATES, CHAIN, LOOKUP, DURATION, seed=150)
