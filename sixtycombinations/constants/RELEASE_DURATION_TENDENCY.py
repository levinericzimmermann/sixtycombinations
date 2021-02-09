import expenvelope

from sixtycombinations.classes import Tendency

RELEASE_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 1.8), (1, 1.8)),
    expenvelope.Envelope.from_points((0, 2.8), (1, 2.8)),
)
