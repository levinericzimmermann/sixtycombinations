import expenvelope

from sixtycombinations.classes import Tendency

LOUDNESS_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 0), (1, 0)),
    expenvelope.Envelope.from_points((0, 1), (1, 1)),
)
