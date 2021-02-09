import expenvelope

from sixtycombinations.classes import Tendency

GLISSANDO_START_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 0.03), (1, 0.03)),
    expenvelope.Envelope.from_points((0, 0.45), (1, 0.4)),
)
