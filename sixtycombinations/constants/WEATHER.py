import math
import random

import expenvelope
import yamm

from mutwo.parameters import pitches

from sixtycombinations import classes
from sixtycombinations.constants import DURATION

random.seed(100)


def make_repeating_sine(duration: float = 0.025, period=1):
    factor = period / duration

    def repsine(time: float) -> float:
        return math.sin(math.pi * (factor * (time % duration)))

    return repsine


STATES = (
    classes.State(
        "default",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 2), (1, 2)),
                expenvelope.Envelope.from_points((0, 3.2), (1, 3.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 1.8), (1, 1.8)),
                expenvelope.Envelope.from_points((0, 2.8), (1, 2.8)),
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
                # expenvelope.Envelope.from_points((0, 40), (1, 40)),
                # expenvelope.Envelope.from_points((0, 950), (1, 950)),
                expenvelope.Envelope.from_points((0, 11), (1, 11)),
                expenvelope.Envelope.from_points((0, 12900), (1, 12900)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_function(make_repeating_sine()),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.25), (1, 0.25)),
                expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.34), (1, 0.34)),
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
                    expenvelope.Envelope.from_points((0, 0.285), (1, 0.285)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 0.91), (1, 0.91),),
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
                    expenvelope.Envelope.from_points((0, 0.0008), (1, 0.0008)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.008), (1, 0.008),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
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
        },
        lambda: random.uniform(130, 220),
        lambda: 30,
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
                # expenvelope.Envelope.from_points((0, 8), (1, 8)),
                # expenvelope.Envelope.from_points((0, 9000), (1, 9000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.7), (1, 0.7)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                expenvelope.Envelope.from_points((0, 0.77), (1, 0.77)),
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
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
                    # filtered noise
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
        },
        lambda: 70,
        lambda: 15,
        0,
        0,
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
                # expenvelope.Envelope.from_points((0, 40), (1, 40)),
                # expenvelope.Envelope.from_points((0, 950), (1, 950)),
                expenvelope.Envelope.from_points((0, 82), (1, 82)),
                expenvelope.Envelope.from_points((0, 12000), (1, 12000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.6), (1, 0.6)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
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
            "bandwidth": expenvelope.Envelope.from_points((0, 20.91), (1, 20.91),),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                expenvelope.Envelope.from_points((0, 0.27), (1, 0.27)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, 11), (1, 11),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.002), (1, 0.002)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.03), (1, 0.03),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "density0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
                expenvelope.Envelope.from_points((0, 0.45), (1, 0.45)),
            ),
            "density1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.25), (1, 0.25)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.225), (1, 0.225)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.02), (1, 0.02)),
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
            ),
        },
        lambda: 100,
        lambda: 40,
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
                # expenvelope.Envelope.from_points((0, 40), (1, 40)),
                # expenvelope.Envelope.from_points((0, 950), (1, 950)),
                expenvelope.Envelope.from_points((0, 42), (1, 42)),
                expenvelope.Envelope.from_points((0, 9000), (1, 9000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
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
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 40.91), (1, 40.91),),
            "filter_frequency": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.001), (1, 0.001)),
                expenvelope.Envelope.from_points((0, 0.12), (1, 0.12)),
            ),
            "filter_q": expenvelope.Envelope.from_points((0, 12), (1, 12),),
            "activate_rest": classes.DynamicChoice(
                (False, True),
                (
                    # no rest
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                    # rest
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5),),
            # ################################################## #
            #         attributes for synthesizer:                #
            # ################################################## #
            "shall_play_octaves0": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves1": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "shall_play_octaves2": classes.DynamicChoice(
                (True, False),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0), (1, 0)),
                    # filtered noise
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
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0), (1, 0)),
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
            ),
        },
        lambda: 100,
        lambda: 40,
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
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
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
                    expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                ),
            ),
            "rest_duration": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5),),
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
                expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
            ),
            "density2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
            ),
            "volume_range0": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
            ),
            "volume_range1": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
            ),
            "volume_range2": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
            ),
        },
        lambda: 110,
        lambda: 60,
        0,
        0,
    ),
)

CHAIN = yamm.Chain(
    {
        ("default",): {"damped": 1, "explosion": 1, "xenakis": 1},
        ("explosion",): {"default": 1},
        ("damped",): {"default": 3, "very_damped": 1, "explosion": 1},
        ("very_damped",): {"damped": 1},
        ("xenakis",): {"default": 1},
    }
)
CHAIN.make_deterministic_map()

WEATHER = classes.Weather("xenakis", STATES, CHAIN, DURATION, seed=150)
