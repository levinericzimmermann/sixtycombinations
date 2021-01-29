import expenvelope

# SPECTRALITY = expenvelope.Envelope.from_points(
#     (0, 1),
#     (0.05, 0),
#     (0.07, 1),
#     (0.1, 0),
#     (0.12, 1),
#     (0.15, 0.5),
#     (0.2, 1),
#     (0.4, 1),
#     (0.5, 0),
#     (1, 1),
# )

# SPECTRALITY = expenvelope.Envelope.from_points(
#     (0, 0.5),
#     (1, 0.5),
# )


import math


def make_repeating_sine(duration: float = 0.025, period=1):
    factor = period / duration

    def repsine(time: float) -> float:
        return math.sin(math.pi * (factor * (time % duration)))

    return repsine


SPECTRALITY = expenvelope.Envelope.from_function(make_repeating_sine())
