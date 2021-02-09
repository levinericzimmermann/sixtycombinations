import expenvelope

from sixtycombinations.classes import Tendency

GLISSANDO_END_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 0.08), (1, 0.08)),
    expenvelope.Envelope.from_points((0, 0.3), (1, 0.3)),
)
