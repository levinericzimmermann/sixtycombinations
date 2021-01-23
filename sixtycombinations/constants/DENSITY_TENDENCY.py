import expenvelope

from sixtycombinations.classes import Tendency

DENSITY_TENDENCY = Tendency(
    # where 0 represents the lowest density
    # and 1 represents the highest density
    expenvelope.Envelope.from_points((0, 0), (1, 0)),
    expenvelope.Envelope.from_points((0, 1), (1, 1)),
)
