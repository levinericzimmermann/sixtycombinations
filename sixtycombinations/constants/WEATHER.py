import math

import expenvelope
import yamm

from mutwo.parameters import pitches

from sixtycombinations import classes
from sixtycombinations.constants import DURATION


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
                expenvelope.Envelope.from_points((0, 1.3), (1, 1.3)),
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
                expenvelope.Envelope.from_points((0, 7), (1, 7)),
                expenvelope.Envelope.from_points((0, 7000), (1, 7000)),
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
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
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
            "filter_frequency": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5),),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
        },
        lambda: 35,
        lambda: 15,
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
                expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
                expenvelope.Envelope.from_points((0, 0.65), (1, 0.65)),
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
            "filter_frequency": expenvelope.Envelope.from_points((0, 0.5), (1, 0.5),),
            "filter_q": expenvelope.Envelope.from_points((0, -16), (1, -16),),
        },
        lambda: 15,
        lambda: 4,
        0,
        0,
    ),
    classes.State(
        "damped",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 3.3), (1, 3.3)),
                expenvelope.Envelope.from_points((0, 4.2), (1, 4.2)),
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
                expenvelope.Envelope.from_points((0, 302), (1, 302)),
                expenvelope.Envelope.from_points((0, 20000), (1, 20000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0), (1, 0)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.05), (1, 0.05)),
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
                    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 47.91), (1, 47.91),),
            "filter_frequency": expenvelope.Envelope.from_points((0, 0.1), (1, 0.1),),
            "filter_q": expenvelope.Envelope.from_points((0, 5), (1, 5),),
        },
        lambda: 120,
        lambda: 15,
        0,
        0,
    ),
    classes.State(
        "very_damped",
        {
            "attack_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 2.3), (1, 2.3)),
                expenvelope.Envelope.from_points((0, 4.2), (1, 4.2)),
            ),
            "release_duration": classes.Tendency(
                expenvelope.Envelope.from_points((0, 2.8), (1, 2.8)),
                expenvelope.Envelope.from_points((0, 4.8), (1, 4.8)),
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
                expenvelope.Envelope.from_points((0, 32), (1, 42)),
                expenvelope.Envelope.from_points((0, 14000), (1, 14000)),
                # expenvelope.Envelope.from_points((0, 250), (1, 250)),
                # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
            ),
            "spectrality": expenvelope.Envelope.from_points((0, 0.8), (1, 0.8)),
            "density": classes.Tendency(
                # where 0 represents the lowest density
                # and 1 represents the highest density
                expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "loudness": classes.Tendency(
                expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                expenvelope.Envelope.from_points((0, 1), (1, 1)),
            ),
            "synthesizer": classes.DynamicChoice(
                # 1 -> sine
                # 2 -> filtered noise
                (1, 2),
                (
                    # sine
                    expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
                    # filtered noise
                    expenvelope.Envelope.from_points((0, 1), (1, 1)),
                ),
            ),
            "bandwidth": expenvelope.Envelope.from_points((0, 27.91), (1, 27.91),),
            "filter_frequency": expenvelope.Envelope.from_points((0, 0.15), (1, 0.15),),
            "filter_q": expenvelope.Envelope.from_points((0, -6), (1, -6),),
        },
        lambda: 10,
        lambda: 1,
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
                expenvelope.Envelope.from_points((0, 14000), (1, 14000)),
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
                expenvelope.Envelope.from_points((0, 0.9), (1, 0.9)),
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
            "bandwidth": expenvelope.Envelope.from_points((0, 17.91), (1, 17.91),),
            "filter_frequency": expenvelope.Envelope.from_points((0, 0.89), (1, 0.89),),
            "filter_q": expenvelope.Envelope.from_points((0, 5), (1, 5),),
        },
        lambda: 180,
        lambda: 15,
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

WEATHER = classes.Weather("damped", STATES, CHAIN, DURATION, seed=150)
