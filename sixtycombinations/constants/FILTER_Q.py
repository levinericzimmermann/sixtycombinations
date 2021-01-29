"""Definition of filter quality.

Expected values are in the range (-15, 15) where 15 makes the strongest
filter and -15 the weakest filter.
"""

import expenvelope

FILTER_Q = expenvelope.Envelope.from_points((0, -15), (1, -15),)
# FILTER_Q = expenvelope.Envelope.from_points((0, 15), (0.1, 0), (0.11, -15), (1, 15))
