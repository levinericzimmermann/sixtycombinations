import math

import expenvelope

from mutwo.parameters import pitches

from sixtycombinations import classes

# The following constants / tendencies keep mostly the same throughout the
# complete composition (only soft modulations for variety are applied, but
# generally a satisfying range has been found for the complete composition)


ATTACK_DURATION_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 1.3), (1, 1.3)),
    expenvelope.Envelope.from_points((0, 3.2), (1, 3.2)),
)
RELEASE_DURATION_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 1.8), (1, 1.8)),
    expenvelope.Envelope.from_points((0, 2.8), (1, 2.8)),
)


GLISSANDO_START_PITCH_CURVE = classes.DynamicChoice(
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
)
"""Curve which defines the probability of each glissando start pitch interval."""


GLISSANDO_END_PITCH_CURVE = classes.DynamicChoice(
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
)
"""Curve which defines the probability of each glissando end pitch interval."""


GLISSANDO_START_DURATION_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
    expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
)


GLISSANDO_END_DURATION_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
)

MINIMAL_PHASES_PER_SOUND_TENDENCY = classes.Tendency(
    # expenvelope.Envelope.from_points((0, 40), (1, 40)),
    # expenvelope.Envelope.from_points((0, 950), (1, 950)),
    expenvelope.Envelope.from_points((0, 8), (1, 8)),
    expenvelope.Envelope.from_points((0, 9000), (1, 9000)),
    # expenvelope.Envelope.from_points((0, 250), (1, 250)),
    # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
)

# ###############################################################################
# TENDENCIES FOR A HIGH LEVEL STATE
# Here I can differentiate between a more full or rich sound versus a more
# nuanced, differentiated, quiet sound.
# For building the rich sound:
#   - low spectrality
#   - narrow and high density and loudness tendency
# For building the nuanced sound:
#   - high spectrality
#   - wide density and loudness tendency
#
# The most interesting results happen when the sound is generally nuanced,
# but the spectrality is constantly moving, so that the listener can experience
# both: the richness of all available frequencies and the actual harmonic
# situation of three main pitches (with their more quiet overtones).
#
# I can think of 3 different situations:
#   (1) short & sudden rich "sonic explosions"
#   (2) longer periods with a moving spectrality and wide ranges of tendencies
#       (most interesting listening experience, tendencies may vary in a
#        controlled range)
#   (3) a damped, quiet, low-frequency-emphasising, dark sound situation with a
#       constant, rather high, spectrality


def make_repeating_sine(duration: float = 0.025, period=1):
    factor = period / duration

    def repsine(time: float) -> float:
        return math.sin(math.pi * (factor * (time % duration)))

    return repsine


SPECTRALITY = expenvelope.Envelope.from_function(make_repeating_sine())


DENSITY_TENDENCY = classes.Tendency(
    # where 0 represents the lowest density
    # and 1 represents the highest density
    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
    expenvelope.Envelope.from_points((0, 0.95), (1, 0.95)),
)


LOUDNESS_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
    expenvelope.Envelope.from_points((0, 1), (1, 1)),
)


SYNTHESIZER_CURVE = classes.DynamicChoice(
    # 1 -> sine
    # 2 -> filtered noise
    (1, 2),
    (
        # sine
        expenvelope.Envelope.from_points((0, 1), (1, 1)),
        # filtered noise
        expenvelope.Envelope.from_points((0, 0.285), (1, 0.285)),
    ),
)


BANDWIDTH = expenvelope.Envelope.from_points((0, 0.91), (1, 0.91),)
"""Curve for bandwidth of resonance filter for filtered noise instrument."""


# There are two effects for the filter that I wanna use:
#   (1) damping higher frequencies (making longer parts with an emphasis
#       on bass)
#   (2) short filter sweeps where only high frequencies are dominant

FILTER_FREQUENCY = expenvelope.Envelope.from_points((0, 0.985), (1, 0.985),)
FILTER_Q = expenvelope.Envelope.from_points((0, -16), (1, -16),)
