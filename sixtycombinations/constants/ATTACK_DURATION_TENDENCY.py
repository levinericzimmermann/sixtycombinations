import expenvelope

from sixtycombinations.classes import Tendency

ATTACK_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 1.3), (1, 1.3)),
    expenvelope.Envelope.from_points((0, 3.2), (1, 3.2)),
)
