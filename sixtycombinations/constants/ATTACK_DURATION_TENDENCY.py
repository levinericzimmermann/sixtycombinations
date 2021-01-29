import expenvelope

from sixtycombinations.classes import Tendency

ATTACK_DURATION_TENDENCY = Tendency(
    expenvelope.Envelope.from_points((0, 0.375), (1, 0.375)),
    expenvelope.Envelope.from_points((0, 0.4), (1, 0.4)),
)
