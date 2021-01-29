import expenvelope

from sixtycombinations.classes import Tendency

RELEASE_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 0.37), (1, 0.38)),
    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
)
